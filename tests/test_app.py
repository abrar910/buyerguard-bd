"""
test_app.py - Integration and route tests for BuyerGuard BD Flask application
Validates routes, template rendering, search queries, database counts,
disclaimers, and 404 error states.
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
    """Test landing page renders with branding, search form, and synthetic disclaimer."""
    response = client.get("/")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "BuyerGuard" in html
    assert "Check Before You Buy" in html
    assert "DEMO ONLY" in html
    assert "PLOT-1001" in html


def test_dashboard_statistics(client):
    """Test dashboard displays real calculated statistics matching database."""
    response = client.get("/dashboard")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    plots = get_all_plots()
    assert len(plots) >= 20
    assert "Total Demo Plots" in html
    assert str(len(plots)) in html
    assert "Duplicate Sale Conflicts" in html


def test_search_known_plot(client):
    """Test searching for known plot returns 200 and displays matching plot card."""
    response = client.get("/search?q=PLOT-1001")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "PLOT-1001" in html
    assert "DEMO-MOUZA-01" in html
    assert "View Details" in html


def test_search_unknown_plot_not_found_state(client):
    """Test searching for unknown plot displays clean not-found message."""
    response = client.get("/search?q=NONEXISTENT_PLOT_9999")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "No Demonstration Records Found" in html
    assert "Try searching for these available demo plots" in html


def test_clean_plot_detail(client):
    """Test plot detail page renders clean scenario (PLOT-1001) without false warnings."""
    response = client.get("/plots/PLOT-1001")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Plot Record: PLOT-1001" in html
    assert "No Simulated Inconsistencies Detected" in html
    assert "Citizen Pre-Purchase Checklist" in html


def test_missing_mutation_scenario(client):
    """Test PLOT-1002 correctly displays missing mutation warning."""
    response = client.get("/plots/PLOT-1002")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "PLOT-1002" in html
    assert "RULE_INCOMPLETE_RECORD" in html
    assert "Missing" in html


def test_missing_deed_scenario(client):
    """Test PLOT-1003 correctly displays missing deed reference warning."""
    response = client.get("/plots/PLOT-1003")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "PLOT-1003" in html
    assert "Primary Deed Reference" in html


def test_duplicate_sale_scenario(client):
    """Test PLOT-1004 correctly triggers duplicate sale conflict warning."""
    response = client.get("/plots/PLOT-1004")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "PLOT-1004" in html
    assert "RULE_DUP_SALE" in html
    assert "Potential Duplicate-Sale Inconsistency" in html


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
    """Test printable report route renders clean report with synthetic disclaimer."""
    response = client.get("/plots/PLOT-1001/report")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Verification Report" in html
    assert "SYNTHETIC DEMONSTRATION RECORD" in html
    assert "NOT AN OFFICIAL GOVERNMENT DOCUMENT" in html
    assert "PLOT-1001" in html


def test_standalone_checklist(client):
    """Test standalone citizen checklist route renders 7 verification tasks."""
    response = client.get("/checklist")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Interactive Citizen Pre-Purchase Land Checklist" in html
    assert "Original Title Deed (Dalil) Verification" in html
    assert "Mutation Khatian (Namjari)" in html


def test_health_endpoint(client):
    """Test health endpoint returns healthy status and database connection info."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"
    assert data["database"] == "connected"
    assert data["plot_count"] >= 20


def test_invalid_plot_returns_404(client):
    """Test accessing nonexistent plot ID returns 404 status."""
    response = client.get("/plots/PLOT-NONEXISTENT")
    assert response.status_code == 404
    html = response.get_data(as_text=True)
    assert "No demonstration record found" in html


def test_no_official_government_claims(client):
    """Ensure no page claims official government certification, ownership guarantee, or legal clearance."""
    pages = ["/", "/dashboard", "/plots/PLOT-1001", "/plots/PLOT-1004", "/plots/PLOT-1001/report", "/checklist"]
    forbidden_terms = [
        "Government Verified",
        "Legally Safe",
        "Fraud Confirmed",
        "Ownership Guaranteed",
        "Official Government Certificate",
    ]
    for page in pages:
        res = client.get(page)
        content = res.get_data(as_text=True)
        for term in forbidden_terms:
            assert term not in content, f"Forbidden term '{term}' found on {page}"
