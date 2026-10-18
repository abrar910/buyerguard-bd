"""
test_haq_shufa.py - Unit and Integration Tests for Haq Shufa Legal Guide & Evaluation Engine
BuyerGuard BD — Smart Land Pre-Purchase Verification Platform
"""

import re
import pytest
from app import app
from haq_shufa_engine import HaqShufaEngine


@pytest.fixture
def client():
    """Configure Flask test client with test mode."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_haq_shufa_route_renders_successfully(client):
    """Test /haq-shufa-guide GET renders legal guide, statutory links, and questionnaire in Bangla and English."""
    # Bangla default
    response = client.get("/haq-shufa-guide")
    assert response.status_code == 200
    html = response.get_data(as_text=True)

    assert '<html lang="bn">' in html
    assert "হক শুফা" in html
    assert "SAT Act" in html
    assert "NAT Act" in html
    assert "Muslim Personal Law" in html

    # Official verified statutory links to Laws of Bangladesh
    assert "http://bdlaws.minlaw.gov.bd/act-241/section-8698.html" in html
    assert "http://bdlaws.minlaw.gov.bd/act-231/section-8479.html" in html

    # English mode
    res_en = client.get("/haq-shufa-guide?lang=en")
    assert res_en.status_code == 200
    html_en = res_en.get_data(as_text=True)
    assert '<html lang="en">' in html_en
    assert "Haq Shufa Legal Guide" in html_en
    assert "Right of Pre-emption" in html_en
    assert "does not replace qualified legal advice" in html_en
    assert "Advocate" in html_en


def test_haq_shufa_navigation_presence(client):
    """Verify that Haq Shufa Legal Guide appears in navbar and footer navigation in both languages."""
    pages = ["/", "/dashboard", "/checklist", "/haq-shufa-guide"]
    for page in pages:
        # Default Bangla
        res = client.get(f"{page}?lang=bn")
        assert res.status_code == 200
        html = res.get_data(as_text=True)
        assert "হক শুফা" in html, f"Bangla nav link missing on {page}"

        # English mode
        res_en = client.get(f"{page}?lang=en")
        assert res_en.status_code == 200
        html_en = res_en.get_data(as_text=True)
        assert "Haq Shufa" in html_en, f"English nav link missing on {page}"




def test_haq_shufa_scenario_1_preload(client):
    """Test loading Synthetic Scenario 1 (Undivided Agricultural Inheritance) evaluates to Further Legal Review Required."""
    response = client.get("/haq-shufa-guide?scenario=DEMO-SHUFA-01")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert HaqShufaEngine.CATEGORY_REVIEW_REQUIRED in html
    assert "Section 96" in html


def test_haq_shufa_scenario_2_preload(client):
    """Test loading Synthetic Scenario 2 (Ambiguous Notice/Facts) evaluates to Relevant Facts Need Verification."""
    response = client.get("/haq-shufa-guide?scenario=DEMO-SHUFA-02")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert HaqShufaEngine.CATEGORY_FACTS_NEEDED in html


def test_haq_shufa_scenario_3_preload(client):
    """Test loading Synthetic Scenario 3 (Partitioned Sole Holding) evaluates to No Risk Indicator Found."""
    response = client.get("/haq-shufa-guide?scenario=DEMO-SHUFA-03")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert HaqShufaEngine.CATEGORY_NO_RISK_FOUND in html


def test_haq_shufa_post_form_evaluation(client):
    """Test submitting questionnaire via POST form generates evaluation."""
    payload = {
        "property_type": "agricultural",
        "co_ownership": "inheritance_undivided",
        "partition_status": "unpartitioned_no_deed",
        "transfer_scope": "undivided_share_stranger",
        "notice_status": "no_notice_served",
        "easement_status": "independent",
    }
    response = client.post("/haq-shufa-guide", data=payload)
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert HaqShufaEngine.CATEGORY_REVIEW_REQUIRED in html
    assert "Section 96" in html


def test_haq_shufa_api_evaluation(client):
    """Test /api/haq-shufa/evaluate endpoint returns structured JSON."""
    payload = {
        "property_type": "non_agricultural",
        "co_ownership": "purchase_undivided",
        "partition_status": "unpartitioned_no_deed",
        "transfer_scope": "undivided_share_stranger",
        "notice_status": "no_notice_served",
        "easement_status": "independent",
    }
    response = client.post("/api/haq-shufa/evaluate", json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data["category"] == HaqShufaEngine.CATEGORY_REVIEW_REQUIRED
    assert data["badge_color"] == "danger"
    assert len(data["findings"]) > 0
    assert "educational_disclaimer" in data


def test_haq_shufa_engine_unit_tests():
    """Direct unit tests for HaqShufaEngine classification logic."""
    # 1. Review required scenario
    res1 = HaqShufaEngine.evaluate({
        "property_type": "agricultural",
        "co_ownership": "inheritance_undivided",
        "partition_status": "unpartitioned_no_deed",
        "transfer_scope": "undivided_share_stranger",
        "notice_status": "no_notice_served",
    })
    assert res1["category"] == HaqShufaEngine.CATEGORY_REVIEW_REQUIRED
    assert res1["badge_color"] == "danger"

    # 2. Missing facts scenario
    res2 = HaqShufaEngine.evaluate({
        "property_type": "unsure",
        "co_ownership": "unsure",
        "partition_status": "unknown_partition",
        "transfer_scope": "unsure",
        "notice_status": "unknown_notice",
    })
    assert res2["category"] == HaqShufaEngine.CATEGORY_FACTS_NEEDED
    assert res2["badge_color"] == "warning"

    # 3. No risk indicator scenario
    res3 = HaqShufaEngine.evaluate({
        "property_type": "agricultural",
        "co_ownership": "sole_ownership",
        "partition_status": "formal_registered_partition",
        "transfer_scope": "entire_demarcated_holding",
        "notice_status": "not_applicable_sole",
        "easement_status": "independent",
    })
    assert res3["category"] == HaqShufaEngine.CATEGORY_NO_RISK_FOUND
    assert res3["badge_color"] == "success"


def test_haq_shufa_no_forbidden_government_claims(client):
    """Ensure Haq Shufa guide never claims official certification, guaranteed ownership, or legal clearance."""
    response = client.get("/haq-shufa-guide")
    assert response.status_code == 200
    content = response.get_data(as_text=True)

    forbidden_terms = [
        "Government Verified",
        "Legally Safe",
        "Fraud Confirmed",
        "Ownership Guaranteed",
        "Official Government Certificate",
    ]
    for term in forbidden_terms:
        assert term not in content, f"Forbidden term '{term}' found on /haq-shufa-guide"


def test_entire_site_has_bengali_primary_language(client):
    """Verify that all user-facing website pages set lang='bn' and have Bengali as primary language."""
    bengali_pattern = re.compile(r'[\u0980-\u09ff]')
    pages_to_check = [
        "/",
        "/dashboard",
        "/checklist",
        "/haq-shufa-guide",
        "/haq-shufa-guide?scenario=DEMO-SHUFA-01",
        "/haq-shufa-guide?scenario=DEMO-SHUFA-02",
        "/haq-shufa-guide?scenario=DEMO-SHUFA-03",
        "/search?q=PLOT-1001",
        "/search?q=PLOT-1004",
        "/search?q=NONEXISTENT_PLOT_9999",
        "/plots/PLOT-1001",
        "/plots/PLOT-1004",
        "/plots/PLOT-1001/report",
    ]

    for page in pages_to_check:
        res = client.get(page)
        assert res.status_code == 200
        html = res.get_data(as_text=True)
        assert '<html lang="bn">' in html, f"Document language lang='bn' missing on {page}"
        matches = bengali_pattern.findall(html)
        assert len(matches) >= 50, f"Expected primary Bengali content on {page}, found only {len(matches)} characters"


def test_bengali_headings_and_disclaimers(client):
    """Verify key translated headings, navigation, and synthetic disclaimers appear in Bangla."""
    # Home
    res_home = client.get("/")
    html_home = res_home.get_data(as_text=True)
    assert "জমি কেনার আগেই যাচাই করুন" in html_home
    assert "রেকর্ড যাচাই করুন" in html_home

    # Dashboard
    res_dash = client.get("/dashboard")
    html_dash = res_dash.get_data(as_text=True)
    assert "কাল্পনিক ভূমি রেকর্ড ড্যাশবোর্ড" in html_dash
    assert "মোট ডেমো প্লট" in html_dash
    assert "দ্বৈত-বিক্রয় বিরোধ" in html_dash

    # Plot details & Warnings
    res_plot4 = client.get("/plots/PLOT-1004")
    html_plot4 = res_plot4.get_data(as_text=True)
    assert "দ্বৈত-বিক্রয়ের সম্ভাব্য অসঙ্গতি" in html_plot4
    assert "করণীয় যাচাইকরণ পদক্ষেপ" in html_plot4

    # Checklist
    res_chk = client.get("/checklist")
    html_chk = res_chk.get_data(as_text=True)
    assert "নাগরিক প্রাক-ক্রয় জমি যাচাইকরণ চেকলিস্ট" in html_chk
    assert "মূল দলিল বালাম তল্লাশি" in html_chk

    # Haq Shufa
    res_shufa = client.get("/haq-shufa-guide")
    html_shufa = res_shufa.get_data(as_text=True)
    assert "হক শুফা আইনগত সহায়িকা" in html_shufa
    assert "অগ্রক্রয়াধিকার" in html_shufa
