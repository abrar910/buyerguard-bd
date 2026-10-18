"""
test_app.py - Integration and route tests for BuyerGuard BD Flask application
Validates routes, template rendering, search queries, database counts,
disclaimers, 404 error states, language toggle, and bilingual translations.
"""

import pytest
from app import app
from database import get_all_plots, init_db
from seed_data import seed_database


@pytest.fixture
def client():
    """Configure Flask test client with test mode."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        with app.app_context():
            init_db()
            seed_database()
        yield client


def test_landing_page(client):
    """Test landing page renders with branding, search form, and synthetic disclaimer in default Bangla & English."""
    # Default is Bangla
    response = client.get("/")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert '<html lang="bn">' in html
    assert "BuyerGuard" in html
    assert "জমি ক্রয়ের পূর্বে সতর্ক হোন" in html or "যাচাই" in html
    assert "কাল্পনিক" in html or "ডেমো" in html
    assert "PLOT-1001" in html

    # English mode
    res_en = client.get("/?lang=en")
    assert res_en.status_code == 200
    html_en = res_en.get_data(as_text=True)
    assert '<html lang="en">' in html_en
    assert "Check Before You Buy" in html_en
    assert "synthetic" in html_en.lower()


def test_dashboard_statistics(client):
    """Test dashboard displays real calculated statistics matching database in both languages."""
    # Bangla default
    response = client.get("/dashboard?lang=bn")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    plots = get_all_plots()
    assert len(plots) >= 20
    assert "মোট ডেমো প্লট" in html
    assert str(len(plots)) in html
    assert "দ্বৈত" in html


    # English mode
    res_en = client.get("/dashboard?lang=en")
    assert res_en.status_code == 200
    html_en = res_en.get_data(as_text=True)
    assert "Total Demo Plots" in html_en
    assert "Duplicate Sale Conflicts" in html_en


def test_search_known_plot(client):
    """Test searching for known plot returns 200 and displays matching plot card."""
    # Bangla default
    response = client.get("/search?q=PLOT-1001")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "PLOT-1001" in html
    assert "DEMO-MOUZA-01" in html
    assert "বিস্তারিত" in html

    # English mode
    res_en = client.get("/search?q=PLOT-1001&lang=en")
    assert res_en.status_code == 200
    html_en = res_en.get_data(as_text=True)
    assert "View Details" in html_en


def test_search_unknown_plot_not_found_state(client):
    """Test searching for unknown plot displays clean not-found message in Bangla and English."""
    # Bangla default
    response = client.get("/search?q=NONEXISTENT_PLOT_9999")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "কোনো প্রদর্শনী রেকর্ড পাওয়া যায়নি" in html or "কোনো প্রদর্শনী রেকর্ড" in html
    assert "উপলব্ধ কিছু ডেমো প্লট নম্বর" in html or "ডেমো প্লট" in html

    # English mode
    res_en = client.get("/search?q=NONEXISTENT_PLOT_9999&lang=en")
    assert res_en.status_code == 200
    html_en = res_en.get_data(as_text=True)
    assert "No Demonstration Records Found" in html_en
    assert "Try searching for these available demo plots" in html_en


def test_clean_plot_detail(client):
    """Test plot detail page renders clean scenario (PLOT-1001) with safe wording in both languages."""
    # Bangla default
    response = client.get("/plots/PLOT-1001")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "PLOT-1001" in html
    assert "ডেমো ডেটায় কোনো সতর্কতামূলক নির্দেশক সনাক্ত হয়নি" in html or "কোনো অসঙ্গতি" in html
    assert "নাগরিক প্রাক-ক্রয় চেকলিস্ট" in html or "চেকলিস্ট" in html

    # English mode
    res_en = client.get("/plots/PLOT-1001?lang=en")
    assert res_en.status_code == 200
    html_en = res_en.get_data(as_text=True)
    assert "Plot Record: PLOT-1001" in html_en
    assert "No Warning Indicators Detected in Demo Data" in html_en
    assert "Citizen Pre-Purchase Checklist" in html_en


def test_missing_mutation_scenario(client):
    """Test PLOT-1002 correctly displays missing mutation warning."""
    response = client.get("/plots/PLOT-1002")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "PLOT-1002" in html
    assert "RULE_INCOMPLETE_RECORD" in html
    assert "নামজারি" in html

    res_en = client.get("/plots/PLOT-1002?lang=en")
    html_en = res_en.get_data(as_text=True)
    assert "Missing" in html_en or "Mutation" in html_en


def test_missing_deed_scenario(client):
    """Test PLOT-1003 correctly displays missing deed reference warning."""
    response = client.get("/plots/PLOT-1003")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "PLOT-1003" in html
    assert "RULE_INCOMPLETE_RECORD" in html
    assert "দলিল" in html

    res_en = client.get("/plots/PLOT-1003?lang=en")
    html_en = res_en.get_data(as_text=True)
    assert "Primary Deed Reference" in html_en or "Deed" in html_en


def test_duplicate_sale_scenario(client):
    """Test PLOT-1004 correctly triggers duplicate sale conflict warning."""
    response = client.get("/plots/PLOT-1004")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "PLOT-1004" in html
    assert "RULE_DUP_SALE" in html
    assert "দ্বৈত-বিক্রয়ের বিরোধ" in html or "দ্বৈত" in html

    res_en = client.get("/plots/PLOT-1004?lang=en")
    html_en = res_en.get_data(as_text=True)
    assert "Potential Duplicate-Sale Inconsistency" in html_en or "Duplicate-Sale" in html_en


def test_mismatch_reference_scenario(client):
    """Test PLOT-1005 triggers reference mismatch warning."""
    response = client.get("/plots/PLOT-1005")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "PLOT-1005" in html
    assert "RULE_REF_MISMATCH" in html


def test_unknown_case_scenario(client):
    """Test PLOT-1006 triggers unknown case warning."""
    response = client.get("/plots/PLOT-1006")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "PLOT-1006" in html
    assert "RULE_UNKNOWN_CASE" in html


def test_unknown_khas_scenario(client):
    """Test PLOT-1007 triggers unknown khas warning."""
    response = client.get("/plots/PLOT-1007")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "PLOT-1007" in html
    assert "RULE_UNKNOWN_KHAS" in html


def test_multi_warning_scenario(client):
    """Test PLOT-1008 triggers multiple warnings."""
    response = client.get("/plots/PLOT-1008")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "PLOT-1008" in html
    assert "RULE_INCOMPLETE_RECORD" in html
    assert "RULE_UNKNOWN_CASE" in html
    assert "RULE_UNKNOWN_KHAS" in html


def test_printable_report(client):
    """Test printable report route renders clean report with synthetic disclaimer in both languages."""
    # Bangla
    response = client.get("/plots/PLOT-1001/report")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "যাচাইকরণ প্রতিবেদন" in html
    assert "কাল্পনিক প্রদর্শনী রেকর্ড" in html
    assert "PLOT-1001" in html

    # English
    res_en = client.get("/plots/PLOT-1001/report?lang=en")
    assert res_en.status_code == 200
    html_en = res_en.get_data(as_text=True)
    assert "Verification" in html_en
    assert "SYNTHETIC DEMONSTRATION RECORD" in html_en
    assert "NOT AN OFFICIAL GOVERNMENT DOCUMENT" in html_en


def test_standalone_checklist(client):
    """Test standalone citizen checklist route renders 7 verification tasks in both languages."""
    # Bangla default
    response = client.get("/checklist")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "নাগরিক প্রাক-ক্রয়" in html
    assert "মূল দলিল বালাম তল্লাশি" in html

    # English
    res_en = client.get("/checklist?lang=en")
    assert res_en.status_code == 200
    html_en = res_en.get_data(as_text=True)
    assert "Citizen Pre-Purchase" in html_en
    assert "Original Title Deed" in html_en


def test_health_endpoint(client):
    """Test health endpoint returns healthy status and database connection info."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"
    assert data["database"] == "connected"
    assert data["plot_count"] >= 20


def test_invalid_plot_returns_404(client):
    """Test accessing nonexistent plot ID returns 404 status with Bangla message."""
    response = client.get("/plots/PLOT-NONEXISTENT")
    assert response.status_code == 404
    html = response.get_data(as_text=True)
    assert "কোনো প্রদর্শনী রেকর্ড" in html or "পাওয়া যায়নি" in html
    assert '<html lang="bn">' in html


def test_custom_404_page(client):
    """Test accessing unknown URL renders Bangla custom 404 template."""
    response = client.get("/unknown-path-for-testing")
    assert response.status_code == 404
    html = response.get_data(as_text=True)
    assert '<html lang="bn">' in html
    assert "অনুরোধকৃত পৃষ্ঠা" in html or "পাওয়া যায়নি" in html
    assert "হোম" in html


def test_language_toggle_and_persistence(client):
    """Test /set-language switches language, redirects, and persists in session."""
    # 1. Switch to English
    resp = client.get("/set-language?lang=en&next=/dashboard")
    assert resp.status_code == 302
    assert resp.location == "/dashboard"

    # Follow redirect or make subsequent request
    dash_resp = client.get("/dashboard")
    dash_html = dash_resp.get_data(as_text=True)
    assert '<html lang="en">' in dash_html
    assert "Synthetic Land Records Dashboard" in dash_html

    # Check that another page stays in English
    home_resp = client.get("/")
    home_html = home_resp.get_data(as_text=True)
    assert '<html lang="en">' in home_html
    assert "Check Before You Buy" in home_html

    # 2. Switch back to Bangla
    resp2 = client.get("/set-language?lang=bn&next=/")
    assert resp2.status_code == 302
    assert resp2.location == "/"

    home_resp2 = client.get("/")
    home_html2 = home_resp2.get_data(as_text=True)
    assert '<html lang="bn">' in home_html2
    assert "জমি ক্রয়ের পূর্বে সতর্ক হোন" in home_html2 or "যাচাই" in home_html2


def test_no_official_government_claims(client):
    """Ensure no page claims official government certification, ownership guarantee, or legal clearance."""
    pages = ["/", "/dashboard", "/plots/PLOT-1001", "/plots/PLOT-1004", "/plots/PLOT-1001/report", "/checklist"]
    forbidden_terms = [
        "Government Verified",
        "Legally Safe",
        "Fraud Confirmed",
        "Ownership Guaranteed",
        "Official Government Certificate",
        "Clean Title",
    ]
    for page in pages:
        res = client.get(page)
        content = res.get_data(as_text=True)
        for term in forbidden_terms:
            assert term not in content, f"Forbidden term '{term}' found on {page}"


def test_custom_404_page_bilingual(client):
    """Test 404 error page renders properly in both Bangla and English."""
    # Bangla 404
    res_bn = client.get("/nonexistent-route-xyz?lang=bn")
    assert res_bn.status_code == 404
    html_bn = res_bn.get_data(as_text=True)
    assert '<html lang="bn">' in html_bn
    assert "অনুরোধকৃত পৃষ্ঠা" in html_bn or "পাওয়া যায়নি" in html_bn

    # English 404
    res_en = client.get("/nonexistent-route-xyz?lang=en")
    assert res_en.status_code == 404
    html_en = res_en.get_data(as_text=True)
    assert '<html lang="en">' in html_en
    assert "Page or Record Not Found" in html_en or "Not Found" in html_en


def test_plot_detail_responsive_tables_and_safe_disclaimers(client):
    """Test plot detail transaction history table readability and safe disclaimer presence."""
    res = client.get("/plots/PLOT-1004?lang=bn")
    assert res.status_code == 200
    html = res.get_data(as_text=True)
    assert "min-width: 620px" in html
    assert "text-break" in html
    assert "কাল্পনিক প্রদর্শনী" in html or "সতর্কবার্তা" in html
