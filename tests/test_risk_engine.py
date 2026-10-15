"""
test_risk_engine.py - Unit tests for BuyerGuard BD explainable risk engine
Verifies all 5 rules, completeness calculations, edge cases, and legitimate chains.
"""

import pytest
from risk_engine import RiskEngine


def test_clean_plot_evaluation():
    """Verify that a complete plot with consistent active transactions yields no warnings."""
    plot = {
        "plot_id": "PLOT-TEST-CLEAN",
        "demo_district": "Demo District A",
        "demo_upazila": "Demo Upazila 01",
        "demo_mouza_code": "DEMO-MOUZA-01",
        "khatian_ref": "KH-TEST-001",
        "deed_ref": "DEED-TEST-001",
        "mutation_status": "Mutated (Namjari Complete)",
        "case_info_status": "No Active Litigation Reported in Demo Records",
        "khas_acquisition_status": "Not Marked as Khas / Non-Acquired",
    }
    txs = [
        {
            "plot_id": "PLOT-TEST-CLEAN",
            "transaction_ref": "TX-01",
            "deed_ref": "DEED-TEST-001",
            "transaction_type": "Sale",
            "transaction_date": "2022-01-01",
            "record_status": "Active",
            "conflict_group_id": None,
        }
    ]

    result = RiskEngine.evaluate_plot(plot, txs)
    assert result["has_warnings"] is False
    assert result["warning_count"] == 0
    assert result["overall_status"] == "No Demo Flags Detected"
    assert result["completeness"]["percentage"] == 100
    assert result["completeness"]["is_complete"] is True
    assert result["has_duplicate_conflict"] is False


def test_missing_mutation_warning():
    """Rule 2: Missing mutation status triggers incomplete record warning."""
    plot = {
        "plot_id": "PLOT-TEST-NOMUT",
        "demo_district": "Demo District A",
        "demo_upazila": "Demo Upazila 01",
        "demo_mouza_code": "DEMO-MOUZA-01",
        "khatian_ref": "KH-TEST-002",
        "deed_ref": "DEED-TEST-002",
        "mutation_status": "Missing",
        "case_info_status": "No Active Litigation Reported in Demo Records",
        "khas_acquisition_status": "Not Marked as Khas / Non-Acquired",
    }
    result = RiskEngine.evaluate_plot(plot, [])
    assert result["has_warnings"] is True
    rule_ids = [w["rule_id"] for w in result["warnings"]]
    assert "RULE_INCOMPLETE_RECORD" in rule_ids
    assert result["has_missing_info"] is True


def test_missing_deed_ref_warning():
    """Rule 2: Missing deed reference triggers incomplete record warning."""
    plot = {
        "plot_id": "PLOT-TEST-NODEED",
        "demo_district": "Demo District A",
        "demo_upazila": "Demo Upazila 01",
        "demo_mouza_code": "DEMO-MOUZA-01",
        "khatian_ref": "KH-TEST-003",
        "deed_ref": None,
        "mutation_status": "Mutated (Namjari Complete)",
        "case_info_status": "No Active Litigation Reported in Demo Records",
        "khas_acquisition_status": "Not Marked as Khas / Non-Acquired",
    }
    result = RiskEngine.evaluate_plot(plot, [])
    assert result["has_warnings"] is True
    rule_ids = [w["rule_id"] for w in result["warnings"]]
    assert "RULE_INCOMPLETE_RECORD" in rule_ids


def test_duplicate_sale_conflict_warning():
    """Rule 1: Multiple active sales with distinct deed references trigger duplicate sale warning."""
    plot = {
        "plot_id": "PLOT-TEST-DUP",
        "demo_district": "Demo District B",
        "demo_upazila": "Demo Upazila 03",
        "demo_mouza_code": "DEMO-MOUZA-03",
        "khatian_ref": "KH-TEST-004",
        "deed_ref": "DEED-TEST-A",
        "mutation_status": "Mutated (Namjari Complete)",
        "case_info_status": "No Active Litigation Reported in Demo Records",
        "khas_acquisition_status": "Not Marked as Khas / Non-Acquired",
    }
    txs = [
        {
            "plot_id": "PLOT-TEST-DUP",
            "transaction_ref": "TX-DUP-01",
            "deed_ref": "DEED-TEST-A",
            "transaction_type": "Sale",
            "transaction_date": "2023-01-01",
            "record_status": "Active",
            "conflict_group_id": "CONF-TEST",
        },
        {
            "plot_id": "PLOT-TEST-DUP",
            "transaction_ref": "TX-DUP-02",
            "deed_ref": "DEED-TEST-B",
            "transaction_type": "Simulated Duplicate Sale",
            "transaction_date": "2023-03-01",
            "record_status": "Active",
            "conflict_group_id": "CONF-TEST",
        },
    ]

    result = RiskEngine.evaluate_plot(plot, txs)
    assert result["has_duplicate_conflict"] is True
    rule_ids = [w["rule_id"] for w in result["warnings"]]
    assert "RULE_DUP_SALE" in rule_ids
    assert result["overall_status"] == "Potential Inconsistency"
    assert result["status_badge"] == "danger"


def test_legitimate_historical_chain_does_not_trigger_duplicate_sale():
    """Multiple chronological transactions with superseded older status must NOT trigger duplicate sale."""
    plot = {
        "plot_id": "PLOT-TEST-HIST",
        "demo_district": "Demo District A",
        "demo_upazila": "Demo Upazila 01",
        "demo_mouza_code": "DEMO-MOUZA-01",
        "khatian_ref": "KH-TEST-005",
        "deed_ref": "DEED-CURRENT",
        "mutation_status": "Mutated (Namjari Complete)",
        "case_info_status": "No Active Litigation Reported in Demo Records",
        "khas_acquisition_status": "Not Marked as Khas / Non-Acquired",
    }
    txs = [
        {
            "plot_id": "PLOT-TEST-HIST",
            "transaction_ref": "TX-HIST-01",
            "deed_ref": "DEED-OLD-1",
            "transaction_type": "Inheritance",
            "transaction_date": "2010-01-01",
            "record_status": "Superseded",
            "conflict_group_id": None,
        },
        {
            "plot_id": "PLOT-TEST-HIST",
            "transaction_ref": "TX-HIST-02",
            "deed_ref": "DEED-OLD-2",
            "transaction_type": "Gift",
            "transaction_date": "2016-01-01",
            "record_status": "Superseded",
            "conflict_group_id": None,
        },
        {
            "plot_id": "PLOT-TEST-HIST",
            "transaction_ref": "TX-ACTUAL",
            "deed_ref": "DEED-CURRENT",
            "transaction_type": "Sale",
            "transaction_date": "2022-01-01",
            "record_status": "Active",
            "conflict_group_id": None,
        },
    ]

    result = RiskEngine.evaluate_plot(plot, txs)
    assert result["has_duplicate_conflict"] is False
    assert "RULE_DUP_SALE" not in [w["rule_id"] for w in result["warnings"]]


def test_superseded_conflict_marker_does_not_trigger_duplicate_sale():
    """A historical conflict marker is not an active duplicate-sale finding."""
    plot = {
        "plot_id": "PLOT-TEST-HIST-CONFLICT",
        "demo_district": "Demo District A",
        "demo_upazila": "Demo Upazila 01",
        "demo_mouza_code": "DEMO-MOUZA-01",
        "khatian_ref": "KH-TEST-005B",
        "deed_ref": "DEED-CURRENT",
        "mutation_status": "Mutated (Namjari Complete)",
        "case_info_status": "No Active Litigation Reported in Demo Records",
        "khas_acquisition_status": "Not Marked as Khas / Non-Acquired",
    }
    transactions = [
        {
            "plot_id": plot["plot_id"],
            "transaction_ref": "TX-HIST-CONFLICT",
            "deed_ref": "DEED-OLD-CONFLICT",
            "transaction_type": "Sale",
            "transaction_date": "2010-01-01",
            "record_status": "Superseded",
            "conflict_group_id": "CONF-HISTORICAL",
        },
        {
            "plot_id": plot["plot_id"],
            "transaction_ref": "TX-CURRENT",
            "deed_ref": "DEED-CURRENT",
            "transaction_type": "Sale",
            "transaction_date": "2022-01-01",
            "record_status": "Active",
            "conflict_group_id": None,
        },
    ]

    result = RiskEngine.evaluate_plot(plot, transactions)
    assert result["has_duplicate_conflict"] is False
    assert "RULE_DUP_SALE" not in [w["rule_id"] for w in result["warnings"]]


def test_inconsistent_reference_warning():
    """Rule 3: Master deed contradicts active transaction deed reference."""
    plot = {
        "plot_id": "PLOT-TEST-MISMATCH",
        "demo_district": "Demo District B",
        "demo_upazila": "Demo Upazila 03",
        "demo_mouza_code": "DEMO-MOUZA-03",
        "khatian_ref": "KH-TEST-006",
        "deed_ref": "DEED-OFFICIAL-123",
        "mutation_status": "Mutated (Namjari Complete)",
        "case_info_status": "No Active Litigation Reported in Demo Records",
        "khas_acquisition_status": "Not Marked as Khas / Non-Acquired",
    }
    txs = [
        {
            "plot_id": "PLOT-TEST-MISMATCH",
            "transaction_ref": "TX-01",
            "deed_ref": "DEED-DIFFERENT-456",
            "transaction_type": "Sale",
            "transaction_date": "2021-01-01",
            "record_status": "Active",
            "conflict_group_id": None,
        }
    ]

    result = RiskEngine.evaluate_plot(plot, txs)
    rule_ids = [w["rule_id"] for w in result["warnings"]]
    assert "RULE_REF_MISMATCH" in rule_ids


def test_unknown_case_and_khas_warnings():
    """Rule 4 and 5: Unknown litigation or khas status trigger cautionary information warnings."""
    plot = {
        "plot_id": "PLOT-TEST-UNVERIFIED",
        "demo_district": "Demo District C",
        "demo_upazila": "Demo Upazila 05",
        "demo_mouza_code": "DEMO-MOUZA-05",
        "khatian_ref": "KH-TEST-007",
        "deed_ref": "DEED-TEST-007",
        "mutation_status": "Mutated (Namjari Complete)",
        "case_info_status": "Unknown / Pending Court Verification",
        "khas_acquisition_status": "Unknown / Pending Land Office Vetting",
    }
    result = RiskEngine.evaluate_plot(plot, [])
    rule_ids = [w["rule_id"] for w in result["warnings"]]
    assert "RULE_UNKNOWN_CASE" in rule_ids
    assert "RULE_UNKNOWN_KHAS" in rule_ids
