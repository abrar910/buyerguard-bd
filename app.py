"""
app.py - Flask Application for BuyerGuard BD
Smart Land Pre-Purchase Verification Platform
LandTech Innovation Hackathon 2026 Prototype
"""

import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, abort, jsonify

from database import (
    init_db,
    get_all_plots,
    get_plot_by_id,
    get_transactions_for_plot,
    search_plots,
)
from seed_data import seed_database
from risk_engine import RiskEngine

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "buyerguard-bd-hackathon-2026-secret")


# Auto-initialize database on application launch
with app.app_context():
    init_db()
    existing_plots = get_all_plots()
    if not existing_plots:
        seed_database()


@app.context_processor
def inject_global_data():
    """Inject common template variables such as current year and demo banner text."""
    return {
        "current_year": datetime.now().year,
        "app_name": "BuyerGuard BD",
        "tagline": "Check Before You Buy",
        "demo_disclaimer": "DEMO ONLY — All records are synthetic. This application is not connected to official land-record systems.",
    }


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
        assessment = RiskEngine.evaluate_plot(plot, txs)
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
    query = request.args.get("q", "").strip()
    if not query:
        return redirect(url_for("dashboard"))

    raw_results = search_plots(query)
    results = []
    for plot in raw_results:
        txs = get_transactions_for_plot(plot["plot_id"])
        assessment = RiskEngine.evaluate_plot(plot, txs)
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
    plot = get_plot_by_id(plot_id)
    if not plot:
        return render_template(
            "404.html",
            resource_name=f"Plot '{plot_id}'",
            message=f"No demonstration record found for identifier '{plot_id}'. Try searching PLOT-1001, PLOT-1002, or PLOT-1004.",
        ), 404

    txs = get_transactions_for_plot(plot["plot_id"])
    assessment = RiskEngine.evaluate_plot(plot, txs)

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
    plot = get_plot_by_id(plot_id)
    if not plot:
        abort(404)

    txs = get_transactions_for_plot(plot["plot_id"])
    assessment = RiskEngine.evaluate_plot(plot, txs)
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
    Interactive standalone Pre-Purchase Verification Checklist for citizens,
    explaining essential verification stages under Bangladesh land practice.
    """
    return render_template("checklist.html")


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
    return render_template(
        "404.html",
        resource_name="Requested Page",
        message="The page or synthetic land record you requested could not be located in the demonstration system.",
    ), 404


@app.errorhandler(500)
def internal_error(error):
    """Graceful 500 handler without leaking internal tracebacks."""
    return render_template(
        "404.html",
        resource_name="System Error",
        message="An unexpected condition occurred within the demonstration application. Please return to the dashboard.",
    ), 500


if __name__ == "__main__":
    # Run the local development server. Production uses wsgi.py with Gunicorn.
    port = int(os.environ.get("PORT", 5000))
    host = os.environ.get("HOST", "127.0.0.1")
    debug = os.environ.get("FLASK_DEBUG", "0").strip().lower() in {"1", "true", "yes"}
    app.run(host=host, port=port, debug=debug, use_reloader=debug)
