"""
risk_engine.py - Explainable Risk and Anomaly Detection Engine
BuyerGuard BD — Smart Land Pre-Purchase Verification Platform

Deterministic, rule-based inspection of synthetic land records.
Outputs clear, human-understandable warnings with explicit next steps.
Never produces legal guarantees or claims of official government clearance.
"""

from typing import Dict, Any, List, Optional


class RiskEngine:
    """
    Deterministic rule engine that inspects synthetic land plot data and
    associated transaction histories to detect simulated inconsistencies,
    missing records, and potential double-selling conflicts.
    """

    @classmethod
    def evaluate_plot(
        cls, plot: Dict[str, Any], transactions: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Evaluate a single plot record and its transactions.
        Returns a structured assessment dictionary.
        """
        txs = transactions or []
        warnings: List[Dict[str, Any]] = []

        # 1. Rule: Incomplete Record Check
        incomplete_warning = cls._check_incomplete_record(plot)
        if incomplete_warning:
            warnings.append(incomplete_warning)

        # 2. Rule: Potential Duplicate-Sale Inconsistency
        dup_sale_warning = cls._check_duplicate_sale(plot, txs)
        if dup_sale_warning:
            warnings.append(dup_sale_warning)

        # 3. Rule: Inconsistent Reference Check
        ref_warning = cls._check_reference_mismatch(plot, txs)
        if ref_warning:
            warnings.append(ref_warning)

        # 4. Rule: Unknown Case Information
        case_warning = cls._check_case_info(plot)
        if case_warning:
            warnings.append(case_warning)

        # 5. Rule: Unknown Khas or Acquisition Information
        khas_warning = cls._check_khas_acquisition(plot)
        if khas_warning:
            warnings.append(khas_warning)

        # Completeness calculation
        completeness = cls._calculate_completeness(plot)

        # Determine overall status badge
        has_high = any(w["severity"] == "High" for w in warnings)
        has_medium = any(w["severity"] == "Medium" for w in warnings)
        has_info = any(w["severity"] == "Info" for w in warnings)

        if has_high:
            overall_status = "Potential Inconsistency"
            status_badge = "danger"
        elif has_medium or completeness["missing_count"] > 0:
            overall_status = "Review Needed"
            status_badge = "warning"
        elif has_info:
            overall_status = "Information Incomplete"
            status_badge = "info"
        else:
            overall_status = "No Demo Flags Detected"
            status_badge = "success"

        return {
            "plot_id": plot.get("plot_id"),
            "overall_status": overall_status,
            "status_badge": status_badge,
            "has_warnings": len(warnings) > 0,
            "warning_count": len(warnings),
            "warnings": warnings,
            "completeness": completeness,
            "has_duplicate_conflict": any(w["rule_id"] == "RULE_DUP_SALE" for w in warnings),
            "has_missing_info": completeness["missing_count"] > 0,
        }

    @staticmethod
    def _is_empty_or_placeholder(value: Any) -> bool:
        """Check if a field value is missing, None, or a placeholder."""
        if value is None:
            return True
        val_str = str(value).strip().lower()
        placeholders = {
            "",
            "none",
            "null",
            "not provided",
            "missing",
            "not available",
            "unknown",
            "n/a",
            "not available in demo data",
        }
        return val_str in placeholders

    @classmethod
    def _calculate_completeness(cls, plot: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate plot record completeness percentage and identify missing items."""
        tracked_fields = [
            ("plot_id", "Plot Identifier"),
            ("demo_district", "Demo District"),
            ("demo_upazila", "Demo Upazila"),
            ("demo_mouza_code", "Demo Mouza Code"),
            ("khatian_ref", "Khatian Reference"),
            ("deed_ref", "Deed Reference"),
            ("mutation_status", "Mutation Status"),
            ("case_info_status", "Case Verification Status"),
            ("khas_acquisition_status", "Khas/Acquisition Status"),
        ]

        total = len(tracked_fields)
        missing_fields = []
        present_count = 0

        for key, label in tracked_fields:
            val = plot.get(key)
            if cls._is_empty_or_placeholder(val):
                missing_fields.append({"key": key, "label": label})
            else:
                present_count += 1

        percent = int(round((present_count / total) * 100))

        return {
            "percentage": percent,
            "present_count": present_count,
            "total_count": total,
            "missing_count": len(missing_fields),
            "missing_fields": missing_fields,
            "is_complete": len(missing_fields) == 0,
        }

    @classmethod
    def _check_incomplete_record(cls, plot: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Rule 2: Identify missing essential deed, mutation, or khatian data."""
        missing = []
        if cls._is_empty_or_placeholder(plot.get("deed_ref")):
            missing.append("Primary Deed Reference")
        if cls._is_empty_or_placeholder(plot.get("mutation_status")):
            missing.append("Mutation Status")
        if cls._is_empty_or_placeholder(plot.get("khatian_ref")):
            missing.append("Khatian Reference")

        if missing:
            missing_str = ", ".join(missing)
            return {
                "rule_id": "RULE_INCOMPLETE_RECORD",
                "title": "Incomplete Synthetic Plot Record",
                "severity": "Medium",
                "badge_class": "warning",
                "affected_field": missing_str,
                "explanation": (
                    f"The demonstration record is missing key documentation elements: {missing_str}. "
                    "In real-world pre-purchase diligence, missing mutation or deed numbers prevents "
                    "verifying chain of title."
                ),
                "recommended_action": (
                    "Request original deed and mutation khatian copies from the seller before proceeding. "
                    "Cross-check records at the relevant AC (Land) office."
                ),
            }
        return None

    @classmethod
    def _check_duplicate_sale(
        cls, plot: Dict[str, Any], transactions: List[Dict[str, Any]]
    ) -> Optional[Dict[str, Any]]:
        """
        Rule 1: Detect intentionally simulated situation in which the same plot
        has multiple conflicting active sale claims with different deed references.
        Legitimate chronological transactions (e.g., 'Superseded' or past history)
        do not trigger this rule.
        """
        if not transactions:
            return None

        # Filter active sales / transfers
        active_sales = [
            tx
            for tx in transactions
            if str(tx.get("record_status", "")).strip().lower() == "active"
            and str(tx.get("transaction_type", "")).strip().lower()
            in {"sale", "purchase", "transfer", "simulated duplicate sale"}
        ]

        # Condition 1: Multiple active sales with distinct deed references
        active_deeds = {
            tx.get("deed_ref")
            for tx in active_sales
            if tx.get("deed_ref") and not cls._is_empty_or_placeholder(tx.get("deed_ref"))
        }

        # Condition 2: Explicit conflict group marker in synthetic dataset
        conflict_groups = {
            tx.get("conflict_group_id")
            for tx in active_sales
            if tx.get("conflict_group_id") and not cls._is_empty_or_placeholder(tx.get("conflict_group_id"))
        }

        if len(active_deeds) > 1 or len(conflict_groups) > 0:
            deeds_display = ", ".join(sorted(str(d) for d in active_deeds)) if active_deeds else "Conflicting records"
            return {
                "rule_id": "RULE_DUP_SALE",
                "title": "Potential Duplicate-Sale Inconsistency Detected",
                "severity": "High",
                "badge_class": "danger",
                "affected_field": f"Active Deed Claims ({deeds_display})",
                "explanation": (
                    f"Synthetic records exhibit conflicting active sale entries ({deeds_display}) for plot "
                    f"'{plot.get('plot_id')}'. This simulated anomaly highlights the risk of double-selling "
                    "or parallel conveyances where two parties claim active ownership."
                ),
                "recommended_action": (
                    "Urgent follow-up required. Conduct an exhaustive search in Sub-Registry office volumes "
                    "(Balam books) and verify mutation ledger records with the Assistant Commissioner (Land)."
                ),
            }

        return None

    @classmethod
    def _check_reference_mismatch(
        cls, plot: Dict[str, Any], transactions: List[Dict[str, Any]]
    ) -> Optional[Dict[str, Any]]:
        """
        Rule 3: Identify deliberately conflicting demo references across related records.
        E.g. plot's registered deed_ref contradicts the deed_ref of the latest active transaction.
        """
        plot_deed = (plot.get("deed_ref") or "").strip()
        if not plot_deed or cls._is_empty_or_placeholder(plot_deed):
            return None

        # Look at active transactions
        active_txs = [
            tx for tx in transactions if str(tx.get("record_status", "")).strip().lower() == "active"
        ]

        mismatched_txs = []
        for tx in active_txs:
            tx_deed = (tx.get("deed_ref") or "").strip()
            if tx_deed and not cls._is_empty_or_placeholder(tx_deed):
                if tx_deed.upper() != plot_deed.upper():
                    mismatched_txs.append(tx_deed)

        if mismatched_txs:
            mismatch_list = ", ".join(set(mismatched_txs))
            return {
                "rule_id": "RULE_REF_MISMATCH",
                "title": "Cross-Record Reference Inconsistency",
                "severity": "Medium",
                "badge_class": "warning",
                "affected_field": f"Plot Deed ({plot_deed}) vs Transaction Deed ({mismatch_list})",
                "explanation": (
                    f"The plot master record lists primary deed '{plot_deed}', whereas active transfer "
                    f"record lists '{mismatch_list}'. Such discrepancies in deed indexing indicate potential "
                    "clerical errors, unlinked partitions, or conflicting claims."
                ),
                "recommended_action": (
                    "Request certified true copies of both deed references from the Sub-Registry office to "
                    "verify correct schedule, boundary (Chouhaddi), and plot demarcation."
                ),
            }

        return None

    @classmethod
    def _check_case_info(cls, plot: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Rule 4: If case-related information is unavailable, advise verification.
        Does NOT infer that a court case exists.
        """
        val = plot.get("case_info_status")
        val_lower = str(val or "").strip().lower()

        if cls._is_empty_or_placeholder(val) or "unknown" in val_lower or "pending" in val_lower or "unverified" in val_lower:
            return {
                "rule_id": "RULE_UNKNOWN_CASE",
                "title": "Litigation / Case Record Unverified in Demo Data",
                "severity": "Info",
                "badge_class": "info",
                "affected_field": "Case Information Status",
                "explanation": (
                    "Civil court litigation or partition dispute records for this plot are marked as "
                    f"'{val or 'Unknown'}' in synthetic data. Missing case history does not guarantee that the "
                    "plot is free from litigation."
                ),
                "recommended_action": (
                    "Perform a local inquiry and search records at the Senior Assistant Judge Court / "
                    "Joint District Judge Court having local jurisdiction."
                ),
            }
        return None

    @classmethod
    def _check_khas_acquisition(cls, plot: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Rule 5: If khas or government acquisition info is unavailable, advise verification.
        Does NOT imply that plot is government-owned, acquired, or free from acquisition.
        """
        val = plot.get("khas_acquisition_status")
        val_lower = str(val or "").strip().lower()

        if cls._is_empty_or_placeholder(val) or "unknown" in val_lower or "pending" in val_lower or "unverified" in val_lower:
            return {
                "rule_id": "RULE_UNKNOWN_KHAS",
                "title": "Khas / Government Acquisition Status Unverified",
                "severity": "Info",
                "badge_class": "info",
                "affected_field": "Khas / Acquisition Status",
                "explanation": (
                    "Information regarding potential Khas (government vested/abandoned) or pending acquisition "
                    f"notices is marked as '{val or 'Unknown'}' in demo records. This demo data cannot confirm "
                    "whether state acquisition proceedings have begun."
                ),
                "recommended_action": (
                    "Consult the Upazila Land Office (AC Land) and Deputy Commissioner (DC) Land Acquisition "
                    "section to ensure no section 4 notice or vesting declaration applies."
                ),
            }
        return None
