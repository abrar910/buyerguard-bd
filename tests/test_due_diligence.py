"""
test_due_diligence.py - Automated Tests for BuyerGuard BD 7-Step Verification,
Complete Land Details, City Survey Risk Scoring, and UI Corrections.
"""

import pytest
from app import app
from database import get_plot_by_id, get_transactions_for_plot
from risk_engine import RiskEngine
from due_diligence_engine import DueDiligenceEngine, DiligenceStatus


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# 1. All seven checks execute for a valid Plot ID
def test_all_seven_checks_execute_for_valid_plot():
    plot = get_plot_by_id("PLOT-1001")
    assert plot is not None
    txs = get_transactions_for_plot("PLOT-1001")
    result = DueDiligenceEngine.run_all_checks(plot, txs, lang="bn")

    assert result["total_checks"] == 7
    assert len(result["checks"]) == 7
    expected_ids = [
        "step_1_deed_registry",
        "step_2_mutation",
        "step_3_title_chain",
        "step_4_partition_share",
        "step_5_litigation",
        "step_6_government_interest",
        "step_7_legal_readiness",
    ]
    actual_ids = [c["check_id"] for c in result["checks"]]
    assert actual_ids == expected_ids
    for c in result["checks"]:
        assert "status" in c
        assert "title" in c
        assert "explanation" in c
        assert "recommended_action" in c
        assert c["status"] in {
            DiligenceStatus.PASS,
            DiligenceStatus.WARNING,
            DiligenceStatus.NEEDS_REVIEW,
            DiligenceStatus.INSUFFICIENT_DATA,
            DiligenceStatus.NOT_APPLICABLE,
        }


# 2. Missing plot IDs return existing appropriate 404 not-found behaviour
def test_missing_plot_id_returns_404(client):
    res = client.get("/plots/PLOT-DOES-NOT-EXIST-999")
    assert res.status_code == 404
    html = res.get_data(as_text=True)
    assert "PLOT-DOES-NOT-EXIST-999" in html


# 3. Missing identifiers result in warnings or insufficient-data statuses
def test_missing_identifiers_status():
    plot_missing_deed = {
        "plot_id": "PLOT-TEST-NO-DEED",
        "demo_district": "District X",
        "demo_upazila": "Upazila Y",
        "demo_mouza_code": "MOUZA-01",
        "deed_ref": None,
        "khatian_ref": "KH-999",
        "mutation_status": "Missing",
        "case_info_status": "No Active Litigation Reported in Demo Records",
        "khas_acquisition_status": "Not Marked as Khas / Non-Acquired",
    }
    result = DueDiligenceEngine.run_all_checks(plot_missing_deed, [], lang="bn")
    step1 = next(c for c in result["checks"] if c["check_id"] == "step_1_deed_registry")
    step2 = next(c for c in result["checks"] if c["check_id"] == "step_2_mutation")

    assert step1["status"] == DiligenceStatus.INSUFFICIENT_DATA
    assert step2["status"] == DiligenceStatus.INSUFFICIENT_DATA


# 4. Conflicting transaction/deed references are detected
def test_conflicting_deed_and_transactions_detected():
    plot = get_plot_by_id("PLOT-1004")
    assert plot is not None
    txs = get_transactions_for_plot("PLOT-1004")
    result = DueDiligenceEngine.run_all_checks(plot, txs, lang="bn")

    step1 = next(c for c in result["checks"] if c["check_id"] == "step_1_deed_registry")
    step3 = next(c for c in result["checks"] if c["check_id"] == "step_3_title_chain")

    assert step1["status"] == DiligenceStatus.WARNING or step3["status"] == DiligenceStatus.WARNING
    assert step3["conflicts"] is not None


# 5. Mutation status is interpreted correctly
def test_mutation_status_interpretation():
    # Mutated
    plot_complete = {
        "plot_id": "P-1",
        "khatian_ref": "KH-123",
        "mutation_status": "Mutated (Namjari Complete)",
    }
    r1 = DueDiligenceEngine._check_step_2_mutation(plot_complete, [], is_bn=True)
    assert r1["status"] == DiligenceStatus.PASS

    # Pending
    plot_pending = {
        "plot_id": "P-2",
        "khatian_ref": "KH-124",
        "mutation_status": "Pending Mutation Application",
    }
    r2 = DueDiligenceEngine._check_step_2_mutation(plot_pending, [], is_bn=True)
    assert r2["status"] == DiligenceStatus.NEEDS_REVIEW

    # Missing
    plot_missing = {
        "plot_id": "P-3",
        "khatian_ref": "KH-125",
        "mutation_status": "Missing",
    }
    r3 = DueDiligenceEngine._check_step_2_mutation(plot_missing, [], is_bn=True)
    assert r3["status"] == DiligenceStatus.INSUFFICIENT_DATA


# 6. Incomplete historical title chains are not falsely passed
def test_incomplete_historical_title_chain_not_falsely_passed():
    plot = {"plot_id": "P-NO-TX", "deed_ref": "DEED-001"}
    r = DueDiligenceEngine._check_step_3_title_chain(plot, [], is_bn=True)
    assert r["status"] == DiligenceStatus.INSUFFICIENT_DATA
    assert r["status"] != DiligenceStatus.PASS


# 7. Missing partition data is handled correctly
def test_partition_data_handling():
    # Sole ownership -> NOT_APPLICABLE
    plot_sole = {
        "ownership_source": "ক্রয় সূত্রে",
        "partition_deed_status": "একক স্বত্ব - বণ্টন প্রযোজ্য নয়",
    }
    r_sole = DueDiligenceEngine._check_step_4_partition(plot_sole, [], is_bn=True)
    assert r_sole["status"] == DiligenceStatus.NOT_APPLICABLE

    # Unpartitioned joint inheritance -> WARNING
    plot_unpart = {
        "ownership_source": "ওয়ারিশ সূত্রে",
        "partition_deed_status": "অবণ্টনকৃত যৌথ সম্পত্তি",
    }
    r_unpart = DueDiligenceEngine._check_step_4_partition(plot_unpart, [], is_bn=True)
    assert r_unpart["status"] == DiligenceStatus.WARNING

    # Registered partition deed -> PASS
    plot_part = {
        "ownership_source": "ওয়ারিশ সূত্রে",
        "partition_deed_status": "রেজিস্ট্রিকৃত আপস-বণ্টননামা বিদ্যমান (দলিল নং ৪৫৮৭)",
    }
    r_part = DueDiligenceEngine._check_step_4_partition(plot_part, [], is_bn=True)
    assert r_part["status"] == DiligenceStatus.PASS


# 8. Recorded case warnings are detected
def test_recorded_case_warning_detected():
    plot_case = {
        "case_info_status": "Active Title Suit 42/2023 Reported",
        "case_details": "Title suit pending in Joint District Judge Court",
    }
    r_case = DueDiligenceEngine._check_step_5_litigation(plot_case, [], is_bn=True)
    assert r_case["status"] == DiligenceStatus.WARNING

    plot_clean = {
        "case_info_status": "No Active Litigation Reported in Demo Records",
        "case_details": "No case reported in available demo records",
    }
    r_clean = DueDiligenceEngine._check_step_5_litigation(plot_clean, [], is_bn=True)
    assert r_clean["status"] == DiligenceStatus.PASS
    assert "No case reported in available demo records" in r_clean["explanation"] or "ডেমো রেকর্ডে কোনো" in r_clean["explanation"]


# 9. Khas/acquisition warnings are detected
def test_khas_acquisition_warning_detected():
    plot_khas = {
        "khas_acquisition_status": "Warning Identified / Khas Schedule Inquiry",
        "gov_interest_details": "Warning Identified: Potential Khas schedule",
    }
    r_khas = DueDiligenceEngine._check_step_6_government_interest(plot_khas, [], is_bn=True)
    assert r_khas["status"] == DiligenceStatus.WARNING

    plot_clean = {
        "khas_acquisition_status": "Not Marked as Khas / Non-Acquired",
        "gov_interest_details": "No Warning Indicator in Available Demo Data",
    }
    r_clean = DueDiligenceEngine._check_step_6_government_interest(plot_clean, [], is_bn=True)
    assert r_clean["status"] == DiligenceStatus.PASS


# 10. Preliminary legal-review readiness identifies unresolved issues and includes advocate disclaimer
def test_preliminary_legal_review_readiness():
    plot = get_plot_by_id("PLOT-1004")
    txs = get_transactions_for_plot("PLOT-1004")
    result = DueDiligenceEngine.run_all_checks(plot, txs, lang="bn")
    step7 = result["checks"][6]

    assert step7["check_id"] == "step_7_legal_readiness"
    assert "আইনজীবী দ্বারা যাচাইকরণ এখনও আবশ্যক" in step7["title"] or "Advocate Review Still Required" in step7["title"]
    assert step7["readiness_outcome"] is not None


# 11. City Survey adds exactly one risk point
def test_city_survey_adds_exactly_one_point():
    plot_city = {
        "plot_id": "PLOT-TEST-CITY",
        "khatian_ref": "KH-101",
        "deed_ref": "DEED-101",
        "mutation_status": "Mutated (Namjari Complete)",
        "case_info_status": "No Active Litigation Reported in Demo Records",
        "khas_acquisition_status": "Not Marked as Khas / Non-Acquired",
        "survey_type": "City Survey",
    }
    res_city = RiskEngine.evaluate_plot(plot_city, [])
    assert res_city["city_survey_point_added"] is True
    assert any(w["rule_id"] == "RULE_CITY_SURVEY" for w in res_city["warnings"])

    # Non-city survey
    plot_rs = dict(plot_city)
    plot_rs["survey_type"] = "RS"
    res_rs = RiskEngine.evaluate_plot(plot_rs, [])
    assert res_rs["city_survey_point_added"] is False
    assert not any(w["rule_id"] == "RULE_CITY_SURVEY" for w in res_rs["warnings"])

    # Difference in score is exactly 1 point
    assert res_city["risk_score"] - res_rs["risk_score"] == 1


# 12. Repeated evaluations never accumulate duplicate points
def test_repeated_evaluations_never_accumulate_duplicate_points():
    plot = get_plot_by_id("PLOT-1009")
    txs = get_transactions_for_plot("PLOT-1009")

    res1 = RiskEngine.evaluate_plot(plot, txs)
    score1 = res1["risk_score"]
    count1 = res1["warning_count"]

    for _ in range(5):
        res_repeat = RiskEngine.evaluate_plot(plot, txs)
        assert res_repeat["risk_score"] == score1
        assert res_repeat["warning_count"] == count1


# 13. Different Plot IDs receive the correct separate results
def test_different_plots_receive_separate_results():
    p1 = get_plot_by_id("PLOT-1001")
    p4 = get_plot_by_id("PLOT-1004")
    p8 = get_plot_by_id("PLOT-1008")

    r1 = RiskEngine.evaluate_plot(p1, get_transactions_for_plot("PLOT-1001"))
    r4 = RiskEngine.evaluate_plot(p4, get_transactions_for_plot("PLOT-1004"))
    r8 = RiskEngine.evaluate_plot(p8, get_transactions_for_plot("PLOT-1008"))

    assert r1["plot_id"] == "PLOT-1001"
    assert r4["plot_id"] == "PLOT-1004"
    assert r8["plot_id"] == "PLOT-1008"

    assert r1["has_warnings"] is False
    assert r4["has_duplicate_conflict"] is True
    assert r8["has_missing_info"] is True
    assert r1["risk_score"] != r4["risk_score"]


# 14. Bangla and English labels work
def test_bangla_and_english_labels():
    plot = get_plot_by_id("PLOT-1001")
    txs = get_transactions_for_plot("PLOT-1001")

    res_bn = DueDiligenceEngine.run_all_checks(plot, txs, lang="bn")
    res_en = DueDiligenceEngine.run_all_checks(plot, txs, lang="en")

    assert "যাচাইকরণ ফলাফল" in res_bn["summary_title"]
    assert "Verification Results" in res_en["summary_title"]


# 15. Printable reports contain the new fields and verification results
def test_printable_reports_contain_new_fields_and_results(client):
    res = client.get("/plots/PLOT-1001/report")
    assert res.status_code == 200
    html = res.get_data(as_text=True)

    # Check for Sections A through G fields in report
    assert "খতিয়ান নম্বর" in html or "Khatian" in html
    assert "দাগ নম্বর" in html or "Dag Number" in html
    assert "মৌজার নাম" in html or "Mouza Name" in html
    assert "জে.এল. নম্বর" in html or "J.L. Number" in html
    assert "দলিল নম্বর" in html or "Deed" in html
    assert "নামজারি" in html or "Mutation" in html
    assert "জরিপের ধরন" in html or "Survey Type" in html
    assert "মালিকানা অর্জনের উৎস" in html or "Source of Ownership" in html
    assert "৭-দফা স্বয়ংক্রিয় প্রাক-ক্রয় যাচাইকরণ ফলাফল" in html or "Automated 7-Step" in html


# 16. The footer no longer contains the four specified technology badges
def test_footer_no_technology_badges(client):
    res = client.get("/")
    assert res.status_code == 200
    html = res.get_data(as_text=True)

    # Badges must not appear
    assert "Python 3.11" not in html
    assert "Deterministic Rules" not in html
    # BuyerGuard BD and disclaimer must remain
    assert "BuyerGuard BD" in html
    assert "শিক্ষামূলক" in html or "ডেমো" in html or "Educational" in html


# 17. Existing features and routes continue to work
def test_all_routes_work(client):
    for route in ["/", "/dashboard", "/search?q=PLOT-1001", "/plots/PLOT-1001", "/checklist", "/haq-shufa-guide", "/health"]:
        res = client.get(route)
        assert res.status_code == 200, f"Route {route} failed with {res.status_code}"
