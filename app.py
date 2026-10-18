"""
app.py - Flask Application for BuyerGuard BD
Smart Land Pre-Purchase Verification Platform
LandTech Innovation Hackathon 2026 Prototype
"""

import os
import secrets
from urllib.parse import parse_qsl, unquote, urlencode, urlsplit, urlunsplit
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, abort, jsonify, session, g

from database import (
    init_db,
    get_all_plots,
    get_plot_by_id,
    get_transactions_for_plot,
    search_plots,
)
from seed_data import seed_database
from risk_engine import RiskEngine
from haq_shufa_engine import HaqShufaEngine
from translations import t, get_checklist_items, get_roadmap_items

app = Flask(__name__)


def _configured_secret_key(environ=None):
    """Resolve a session secret without a predictable production fallback."""
    environ = os.environ if environ is None else environ
    environment = (environ.get("APP_ENV") or environ.get("FLASK_ENV") or "development").strip().lower()
    secret_key = environ.get("SECRET_KEY", "").strip()
    if environment in {"production", "prod"}:
        if not secret_key or secret_key == "replace-with-a-long-random-value":
            raise RuntimeError("SECRET_KEY must be explicitly configured in production; replace the example value.")
        if len(secret_key) < 32:
            raise RuntimeError("SECRET_KEY must contain at least 32 characters in production.")
        return secret_key

    # Local development gets a per-process key; automated tests override it with
    # a stable test-only value in their fixture.
    return secret_key or secrets.token_hex(32)


app.config["SECRET_KEY"] = _configured_secret_key()


def _safe_internal_destination(candidate):
    """Return a safe root-relative destination, or None for malformed/external URLs."""
    if not isinstance(candidate, str) or not candidate or candidate != candidate.strip():
        return None
    if any(ord(char) < 32 or ord(char) == 127 for char in candidate) or "\\" in candidate:
        return None
    try:
        parts = urlsplit(candidate)
    except ValueError:
        return None
    decoded_path = unquote(parts.path)
    # Only root-relative paths are accepted. This avoids scheme-relative URLs,
    # host confusion, and open redirects while retaining internal query strings.
    if (parts.scheme or parts.netloc or not parts.path.startswith("/") or parts.path.startswith("//")
            or decoded_path.startswith("//") or "\\" in decoded_path
            or any(ord(char) < 32 or ord(char) == 127 for char in decoded_path)):
        return None
    return parts


# Auto-initialize database on application launch
with app.app_context():
    init_db()
    existing_plots = get_all_plots()
    if not existing_plots:
        seed_database()


@app.before_request
def handle_language():
    """Detect and persist language preference across requests. Defaults to Bangla ('bn')."""
    lang_param = request.args.get("lang")
    if lang_param in ("bn", "en"):
        session["lang"] = lang_param
    g.lang = session.get("lang", "bn")


@app.context_processor
def inject_global_data():
    """Inject common template variables and translation helpers."""
    lang = getattr(g, "lang", session.get("lang", "bn"))
    return {
        "current_year": datetime.now().year,
        "app_name": "BuyerGuard BD",
        "current_lang": lang,
        "other_lang": "en" if lang == "bn" else "bn",
        "other_lang_name": "English" if lang == "bn" else "বাংলা",
        "t": lambda key, default=None: t(key, lang, default),
        "tagline": t("app_tagline", lang),
        "tagline_short": t("tagline_short", lang),
        "demo_disclaimer": t("banner_text", lang),
        "checklist_items": get_checklist_items(lang),
        "roadmap_items": get_roadmap_items(lang),
    }


@app.route("/set-language")
def set_language():
    """
    Toggle or set language preference ('bn' or 'en') and redirect back to
    the equivalent current page.
    """
    lang = request.args.get("lang", "bn")
    if lang not in ("bn", "en"):
        lang = "bn"
    session["lang"] = lang

    next_url = request.args.get("next")
    destination = _safe_internal_destination(next_url) if next_url is not None else None
    if next_url is None:
        destination = _safe_internal_destination(request.referrer)
    if destination is None:
        return redirect(url_for("index"))

    # Remove any lang query parameter so it cannot override the newly stored
    # language on the redirected request.
    query = urlencode([(key, value) for key, value in parse_qsl(destination.query, keep_blank_values=True)
                       if key != "lang"])
    target = urlunsplit(("", "", destination.path, query, destination.fragment))
    return redirect(target)


@app.route("/")
def index():
    """Landing page featuring search, quick demo plot shortcuts, and feature highlights."""
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    """
    Dashboard displaying real statistics computed from the SQLite database
    and the deterministic Risk Engine.
    """
    lang = getattr(g, "lang", "bn")
    plots = get_all_plots()
    status_filter = request.args.get("status", "").strip()
    mutation_filter = request.args.get("mutation", "").strip()

    evaluated_plots = []
    total_plots = len(plots)
    plots_review_needed = 0
    incomplete_records = 0
    duplicate_sale_conflicts = 0
    clean_plots_count = 0

    for plot in plots:
        txs = get_transactions_for_plot(plot["plot_id"])
        assessment = RiskEngine.evaluate_plot(plot, txs, lang=lang)
        plot_item = {
            "plot": plot,
            "assessment": assessment,
            "tx_count": len(txs),
        }

        # Track statistics
        if assessment["has_warnings"]:
            plots_review_needed += 1
        else:
            clean_plots_count += 1

        if assessment["has_missing_info"]:
            incomplete_records += 1

        if assessment["has_duplicate_conflict"]:
            duplicate_sale_conflicts += 1

        # Apply filtering
        matches_status = True
        if status_filter:
            matches_status = assessment["overall_status"].lower() == status_filter.lower()

        matches_mutation = True
        if mutation_filter:
            plot_mutation = (plot.get("mutation_status") or "").lower()
            if mutation_filter == "mutated":
                matches_mutation = "mutated" in plot_mutation
            elif mutation_filter == "missing":
                matches_mutation = "missing" in plot_mutation or not plot_mutation
            elif mutation_filter == "pending":
                matches_mutation = "pending" in plot_mutation

        if matches_status and matches_mutation:
            evaluated_plots.append(plot_item)

    stats = {
        "total_plots": total_plots,
        "plots_review_needed": plots_review_needed,
        "incomplete_records": incomplete_records,
        "duplicate_sale_conflicts": duplicate_sale_conflicts,
        "clean_plots_count": clean_plots_count,
    }

    return render_template(
        "dashboard.html",
        stats=stats,
        plots=evaluated_plots,
        selected_status=status_filter,
        selected_mutation=mutation_filter,
    )


@app.route("/search")
def search():
    """
    Search plots by Plot ID, Khatian reference, Deed reference, or Mouza code.
    Normalizes input and evaluates all matching results through the risk engine.
    """
    lang = getattr(g, "lang", "bn")
    query = request.args.get("q", "").strip()
    if not query:
        return redirect(url_for("dashboard"))

    raw_results = search_plots(query)
    results = []
    for plot in raw_results:
        txs = get_transactions_for_plot(plot["plot_id"])
        assessment = RiskEngine.evaluate_plot(plot, txs, lang=lang)
        results.append({
            "plot": plot,
            "assessment": assessment,
            "tx_count": len(txs),
        })

    return render_template(
        "search_results.html",
        query=query,
        results=results,
        count=len(results),
    )


@app.route("/plots/<plot_id>")
def plot_detail(plot_id: str):
    """
    Display comprehensive synthetic plot details, transaction chain,
    completeness breakdown, explainable warnings, and pre-purchase checklist.
    """
    lang = getattr(g, "lang", "bn")
    plot = get_plot_by_id(plot_id)
    if not plot:
        is_bn = (lang != "en")
        res_name = f"প্লট '{plot_id}'" if is_bn else f"Plot '{plot_id}'"
        msg = (
            f"'{plot_id}' নম্বরের কোনো প্রদর্শনী রেকর্ড পাওয়া যায়নি (No demonstration record found)। PLOT-1001, PLOT-1002 বা PLOT-1004 দিয়ে অনুসন্ধান করে দেখতে পারেন।"
            if is_bn else
            f"No demonstration record found for plot '{plot_id}'. Try searching for PLOT-1001, PLOT-1002, or PLOT-1004."
        )
        return render_template(
            "404.html",
            resource_name=res_name,
            message=msg,
        ), 404

    txs = get_transactions_for_plot(plot["plot_id"])
    assessment = RiskEngine.evaluate_plot(plot, txs, lang=lang)

    return render_template(
        "plot_detail.html",
        plot=plot,
        transactions=txs,
        assessment=assessment,
    )


@app.route("/plots/<plot_id>/report")
def plot_report(plot_id: str):
    """
    Printable Pre-Purchase Verification Summary Report.
    Uses dedicated print CSS, displays synthetic disclaimer, plot details,
    warnings, and checklist status.
    """
    lang = getattr(g, "lang", "bn")
    plot = get_plot_by_id(plot_id)
    if not plot:
        abort(404)

    txs = get_transactions_for_plot(plot["plot_id"])
    assessment = RiskEngine.evaluate_plot(plot, txs, lang=lang)
    generated_at = datetime.now().strftime("%B %d, %Y - %I:%M %p")

    return render_template(
        "report.html",
        plot=plot,
        transactions=txs,
        assessment=assessment,
        generated_at=generated_at,
    )


@app.route("/checklist")
def standalone_checklist():
    """
    Automated Pre-Purchase Verification Checklist for citizens.
    Automatically evaluates the 7 due-diligence checks against a selected
    demo plot from the database, eliminating contradictory manual checkboxes.
    """
    lang = getattr(g, "lang", "bn")
    plots = get_all_plots()
    selected_plot_id = request.args.get("plot", "").strip() or "PLOT-1001"

    selected_plot = get_plot_by_id(selected_plot_id) or (plots[0] if plots else None)
    assessment = None
    txs = []
    if selected_plot:
        txs = get_transactions_for_plot(selected_plot["plot_id"])
        assessment = RiskEngine.evaluate_plot(selected_plot, txs, lang=lang)

    return render_template(
        "checklist.html",
        plots=plots,
        selected_plot=selected_plot,
        assessment=assessment,
        transactions=txs,
    )


@app.route("/haq-shufa-guide", methods=["GET", "POST"])
def haq_shufa_guide():
    """
    Haq Shufa Legal Guide & Interactive Pre-Purchase Assessment.
    Provides educational information on pre-emption rights in Bangladesh
    under SAT Act 1950 (s.96), NAT Act 1949 (s.24), and Muslim personal law.
    Supports both interactive client-side and server-side evaluation.
    """
    lang = getattr(g, "lang", "bn")
    scenarios = HaqShufaEngine.get_synthetic_scenarios(lang=lang)
    statutes = HaqShufaEngine.VERIFIED_STATUTES
    assessment = None
    form_data = {}

    if request.method == "POST":
        form_data = {
            "property_type": request.form.get("property_type", ""),
            "co_ownership": request.form.get("co_ownership", ""),
            "partition_status": request.form.get("partition_status", ""),
            "transfer_scope": request.form.get("transfer_scope", ""),
            "notice_status": request.form.get("notice_status", ""),
            "easement_status": request.form.get("easement_status", ""),
        }
        assessment = HaqShufaEngine.evaluate(form_data, lang=lang)
    elif request.args.get("scenario"):
        # Preload synthetic demonstration scenario
        scenario_id = request.args.get("scenario")
        selected = next((s for s in scenarios if s["id"] == scenario_id), None)
        if selected:
            form_data = selected["data"]
            assessment = HaqShufaEngine.evaluate(form_data, lang=lang)

    return render_template(
        "haq_shufa.html",
        scenarios=scenarios,
        statutes=statutes,
        assessment=assessment,
        form_data=form_data,
    )


@app.route("/api/haq-shufa/evaluate", methods=["POST"])
def api_haq_shufa_evaluate():
    """
    API endpoint for real-time assessment of Haq Shufa questionnaire inputs.
    Returns JSON evaluation containing informational category, factors, and guidance.
    """
    lang = getattr(g, "lang", "bn")
    data = request.get_json(silent=True) or request.form.to_dict()
    eval_lang = data.get("lang") or lang
    result = HaqShufaEngine.evaluate(data, lang=eval_lang)
    return jsonify(result), 200


@app.route("/health")
def health():
    """Health check endpoint confirming database status and active record count."""
    try:
        plots = get_all_plots()
        return jsonify({
            "status": "healthy",
            "app": "BuyerGuard BD",
            "database": "connected",
            "plot_count": len(plots),
            "timestamp": datetime.now().isoformat(),
        }), 200
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "error": str(e),
        }), 500


@app.errorhandler(404)
def not_found_error(error):
    """Graceful 404 handler."""
    lang = getattr(g, "lang", session.get("lang", "bn"))
    is_bn = (lang != "en")
    return render_template(
        "404.html",
        resource_name="অনুরোধকৃত পৃষ্ঠা পাওয়া যায়নি (Requested Page Not Found)" if is_bn else "Requested Page or Record Not Found",
        message=(
            "আপনার অনুরোধকৃত পৃষ্ঠা বা কাল্পনিক জমির রেকর্ডটি এই ডেমো সিস্টেমে খুঁজে পাওয়া যায়নি। অনুগ্রহ করে ড্যাশবোর্ডে ফিরে যান।"
            if is_bn else
            "The requested synthetic plot or page could not be located in the demonstration database. Please return to the dashboard."
        ),
    ), 404


@app.errorhandler(500)
def internal_error(error):
    """Graceful 500 handler without leaking internal tracebacks."""
    lang = getattr(g, "lang", session.get("lang", "bn"))
    is_bn = (lang != "en")
    return render_template(
        "404.html",
        resource_name="সিস্টেম ত্রুটি (System Error)" if is_bn else "Internal System Error",
        message=(
            "অ্যাপ্লিকেশনটিতে একটি অপ্রত্যাশিত সমস্যা দেখা দিয়েছে। অনুগ্রহ করে ড্যাশবোর্ডে ফিরে যান।"
            if is_bn else
            "An unexpected error occurred. Please try again later or return to the main dashboard."
        ),
    ), 500


if __name__ == "__main__":
    # Run the local development server. Production uses wsgi.py with Gunicorn.
    port = int(os.environ.get("PORT", 5000))
    host = os.environ.get("HOST", "127.0.0.1")
    debug = os.environ.get("FLASK_DEBUG", "0").strip().lower() in {"1", "true", "yes"}
    app.run(host=host, port=port, debug=debug, use_reloader=debug)
