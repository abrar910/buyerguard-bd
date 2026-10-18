"""
risk_engine.py - Explainable Risk and Anomaly Detection Engine
BuyerGuard BD — Smart Land Pre-Purchase Verification Platform

Deterministic, rule-based inspection of synthetic land records.
Outputs clear, human-understandable warnings with explicit next steps in both
Bangla and English. Never produces legal guarantees or claims of official government clearance.
"""

from typing import Dict, Any, List, Optional
from due_diligence_engine import DueDiligenceEngine


class RiskEngine:
    """
    Deterministic rule engine that inspects synthetic land plot data and
    associated transaction histories to detect simulated inconsistencies,
    missing records, and potential double-selling conflicts.
    """

    # Configurable risk points for City Survey screening
    CITY_SURVEY_RISK_POINTS: int = 1

    @classmethod
    def evaluate_plot(
        cls,
        plot: Dict[str, Any],
        transactions: Optional[List[Dict[str, Any]]] = None,
        lang: str = "bn",
    ) -> Dict[str, Any]:
        """
        Evaluate a single plot record and its transactions.
        Returns a structured assessment dictionary in the requested language.
        """
        txs = transactions or []
        warnings: List[Dict[str, Any]] = []
        is_bn = (lang != "en")

        # 1. Rule: Incomplete Record Check
        incomplete_warning = cls._check_incomplete_record(plot, lang=lang)
        if incomplete_warning:
            warnings.append(incomplete_warning)

        # 2. Rule: Potential Duplicate-Sale Inconsistency
        dup_sale_warning = cls._check_duplicate_sale(plot, txs, lang=lang)
        if dup_sale_warning:
            warnings.append(dup_sale_warning)

        # 3. Rule: Inconsistent Reference Check
        ref_warning = cls._check_reference_mismatch(plot, txs, lang=lang)
        if ref_warning:
            warnings.append(ref_warning)

        # 4. Rule: Unknown Case Information
        case_warning = cls._check_case_info(plot, lang=lang)
        if case_warning:
            warnings.append(case_warning)

        # 5. Rule: Unknown Khas or Acquisition Information
        khas_warning = cls._check_khas_acquisition(plot, lang=lang)
        if khas_warning:
            warnings.append(khas_warning)

        # 6. Rule: City Survey Screening Indicator (Adds exactly 1 risk point)
        city_survey_warning = cls._check_city_survey(plot, lang=lang)
        if city_survey_warning:
            warnings.append(city_survey_warning)

        # Completeness calculation
        completeness = cls._calculate_completeness(plot, lang=lang)

        # Calculate deterministic, idempotent risk score
        rule_weights = {
            "RULE_DUP_SALE": 3,
            "RULE_INCOMPLETE_RECORD": 2,
            "RULE_REF_MISMATCH": 2,
            "RULE_UNKNOWN_CASE": 1,
            "RULE_UNKNOWN_KHAS": 1,
            "RULE_CITY_SURVEY": cls.CITY_SURVEY_RISK_POINTS,
        }
        risk_score = sum(rule_weights.get(w["rule_id"], 1) for w in warnings)

        # Determine overall status badge
        has_high = any(w["severity"] == "High" for w in warnings)
        has_medium = any(w["severity"] == "Medium" for w in warnings)
        has_info = any(w["severity"] == "Info" for w in warnings)

        if has_high:
            overall_status = "Potential Inconsistency"
            overall_status_bn = "সম্ভাব্য অসঙ্গতি সনাক্ত"
            overall_status_en = "Potential Inconsistency Detected"
            status_badge = "danger"
        elif has_medium or completeness["missing_count"] > 0:
            overall_status = "Review Needed"
            overall_status_bn = "পর্যালোচনা প্রয়োজন"
            overall_status_en = "Review Recommended"
            status_badge = "warning"
        elif has_info:
            has_other_info = any(w["rule_id"] in {"RULE_UNKNOWN_CASE", "RULE_UNKNOWN_KHAS"} for w in warnings)
            if has_other_info:
                overall_status = "Information Incomplete"
                overall_status_bn = "তথ্য অপূর্ণাঙ্গ"
                overall_status_en = "Information Incomplete"
                status_badge = "info"
            else:
                overall_status = "City Survey Screening Indicator"
                overall_status_bn = "সিটি জরিপ স্ক্রীনিং সূচক"
                overall_status_en = "City Survey Screening Indicator"
                status_badge = "info"
        else:
            overall_status = "No Demo Flags Detected"
            overall_status_bn = "ডেমো ডেটায় কোনো অসঙ্গতি সনাক্ত হয়নি"
            overall_status_en = "No Warning Indicators Detected in Demo Data"
            status_badge = "success"

        overall_status_display = overall_status_bn if is_bn else overall_status_en

        # Execute automated 7-step due-diligence verification
        due_diligence = DueDiligenceEngine.run_all_checks(plot, txs, lang=lang)

        return {
            "plot_id": plot.get("plot_id"),
            "overall_status": overall_status,
            "overall_status_bn": overall_status_bn,
            "overall_status_en": overall_status_en,
            "overall_status_display": overall_status_display,
            "status_badge": status_badge,
            "has_warnings": len(warnings) > 0,
            "warning_count": len(warnings),
            "warnings": warnings,
            "risk_score": risk_score,
            "city_survey_point_added": any(w["rule_id"] == "RULE_CITY_SURVEY" for w in warnings),
            "has_city_survey_indicator": any(w["rule_id"] == "RULE_CITY_SURVEY" for w in warnings),
            "completeness": completeness,
            "has_duplicate_conflict": any(w["rule_id"] == "RULE_DUP_SALE" for w in warnings),
            "has_missing_info": completeness["missing_count"] > 0,
            "due_diligence": due_diligence,
            "lang": lang,
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
    def _calculate_completeness(cls, plot: Dict[str, Any], lang: str = "bn") -> Dict[str, Any]:
        """Calculate plot record completeness percentage and identify missing items."""
        is_bn = (lang != "en")
        tracked_fields = [
            ("plot_id", "প্লট নম্বর" if is_bn else "Plot Identifier"),
            ("demo_district", "জেলা" if is_bn else "District"),
            ("demo_upazila", "উপজেলা" if is_bn else "Upazila"),
            ("demo_mouza_code", "মৌজা কোড" if is_bn else "Mouza Code"),
            ("khatian_ref", "খতিয়ান নম্বর" if is_bn else "Khatian Reference"),
            ("deed_ref", "মূল দলিল নম্বর" if is_bn else "Primary Deed Reference"),
            ("mutation_status", "নামজারি স্ট্যাটাস" if is_bn else "Mutation Status (Namjari)"),
            ("case_info_status", "মামলা যাচাই স্ট্যাটাস" if is_bn else "Case Verification Status"),
            ("khas_acquisition_status", "খাস/অধিগ্রহণ স্ট্যাটাস" if is_bn else "Khas / Acquisition Status"),
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
    def _check_incomplete_record(cls, plot: Dict[str, Any], lang: str = "bn") -> Optional[Dict[str, Any]]:
        """Rule 2: Identify missing essential deed, mutation, or khatian data."""
        is_bn = (lang != "en")
        missing_bn = []
        missing_en = []

        if cls._is_empty_or_placeholder(plot.get("deed_ref")):
            missing_bn.append("মূল দলিল নম্বর")
            missing_en.append("Primary Deed Reference")
        if cls._is_empty_or_placeholder(plot.get("mutation_status")):
            missing_bn.append("নামজারি স্ট্যাটাস")
            missing_en.append("Mutation Status (Namjari)")
        if cls._is_empty_or_placeholder(plot.get("khatian_ref")):
            missing_bn.append("খতিয়ান নম্বর")
            missing_en.append("Khatian Reference")

        if missing_bn:
            missing_str_bn = ", ".join(missing_bn)
            missing_str_en = ", ".join(missing_en)
            title_bn = "অসম্পূর্ণ প্লট রেকর্ড"
            title_en = "Incomplete Synthetic Plot Record"

            explanation_bn = (
                f"এই প্রদর্শনী রেকর্ডে প্রয়োজনীয় তথ্যের ঘাটতি রয়েছে: {missing_str_bn}। "
                "বাস্তব জমি কেনার যাচাইকরণে নামজারি বা দলিলের তথ্যের ঘাটতি থাকলে মালিকানার ধারাবাহিকতা "
                "(Chain of Title) নিশ্চিত করা অসম্ভব হয়ে পড়ে।"
            )
            explanation_en = (
                f"Essential title attributes are missing from this demonstration record: {missing_str_en}. "
                "In real property conveyances, missing mutation or deed references prevents establishing a verifiable chain of title."
            )

            action_bn = (
                "লেনদেন করার পূর্বে বিক্রেতার কাছ থেকে মূল দলিল এবং নামজারি খতিয়ানের কপি তলব করুন। "
                "সংশ্লিষ্ট সহকারী কমিশনার (ভূমি) / এসি ল্যান্ড অফিসে রেকর্ড যাচাই করুন।"
            )
            action_en = (
                "Demand certified copies of the primary registered deed and mutation khatian from the seller before proceeding. "
                "Verify official records at the relevant AC (Land) office."
            )

            return {
                "rule_id": "RULE_INCOMPLETE_RECORD",
                "title": title_bn if is_bn else title_en,
                "title_bn": title_bn,
                "title_en": title_en,
                "severity": "Medium",
                "badge_class": "warning",
                "severity_display": "মাঝারি" if is_bn else "Medium",
                "affected_field": missing_str_bn if is_bn else missing_str_en,
                "explanation": explanation_bn if is_bn else explanation_en,
                "explanation_bn": explanation_bn,
                "explanation_en": explanation_en,
                "recommended_action": action_bn if is_bn else action_en,
                "recommended_action_bn": action_bn,
                "recommended_action_en": action_en,
            }
        return None

    @classmethod
    def _check_duplicate_sale(
        cls, plot: Dict[str, Any], transactions: List[Dict[str, Any]], lang: str = "bn"
    ) -> Optional[Dict[str, Any]]:
        """
        Rule 1: Detect intentionally simulated situation in which the same plot
        has multiple conflicting active sale claims with different deed references.
        Legitimate chronological transactions (e.g., 'Superseded' or past history)
        do not trigger this rule.
        """
        if not transactions:
            return None

        is_bn = (lang != "en")

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
            title_bn = "দ্বৈত-বিক্রয়ের সম্ভাব্য অসঙ্গতি"
            title_en = "Potential Duplicate-Sale Inconsistency"

            explanation_bn = (
                f"কাল্পনিক রেকর্ডে '{plot.get('plot_id')}' প্লটের জন্য একাধিক সক্রিয় বিক্রয় দাবি ({deeds_display}) দেখা যাচ্ছে। "
                "এই সিমুলেটেড অসঙ্গতিটি একই জমির ডাবল-সেলিং বা সমান্তরাল দলিলের ঝুঁকি নির্দেশ করে যেখানে একাধিক পক্ষ সক্রিয় মালিকানা দাবি করছে।"
            )
            explanation_en = (
                f"Synthetic records for plot '{plot.get('plot_id')}' contain multiple concurrent active conveyance claims ({deeds_display}). "
                "This simulated conflict indicates potential double-selling or parallel deed risks where multiple parties assert simultaneous title."
            )

            action_bn = (
                "জরুরি অনুসন্ধান প্রয়োজন। সাব-রেজিস্ট্রি অফিসের ভলিউম বালাম বইয়ে বিস্তারিত তল্লাশি (Search) দিন "
                "এবং সহকারী কমিশনার (ভূমি) অফিসে নামজারি রেজিস্টার যাচাই করুন।"
            )
            action_en = (
                "Immediate investigative action required. Conduct an exhaustive Volume (Balam) book search at the Sub-Registry office "
                "and verify the mutation register at the AC (Land) office to determine chronological priority."
            )

            affected_bn = f"সক্রিয় দলিলের দাবি ({deeds_display})"
            affected_en = f"Active Conveyance Claims ({deeds_display})"

            return {
                "rule_id": "RULE_DUP_SALE",
                "title": title_bn if is_bn else title_en,
                "title_bn": title_bn,
                "title_en": title_en,
                "severity": "High",
                "badge_class": "danger",
                "severity_display": "উচ্চ" if is_bn else "High",
                "affected_field": affected_bn if is_bn else affected_en,
                "explanation": explanation_bn if is_bn else explanation_en,
                "explanation_bn": explanation_bn,
                "explanation_en": explanation_en,
                "recommended_action": action_bn if is_bn else action_en,
                "recommended_action_bn": action_bn,
                "recommended_action_en": action_en,
            }

        return None

    @classmethod
    def _check_reference_mismatch(
        cls, plot: Dict[str, Any], transactions: List[Dict[str, Any]], lang: str = "bn"
    ) -> Optional[Dict[str, Any]]:
        """
        Rule 3: Identify deliberately conflicting demo references across related records.
        E.g. plot's registered deed_ref contradicts the deed_ref of the latest active transaction.
        """
        plot_deed = (plot.get("deed_ref") or "").strip()
        if not plot_deed or cls._is_empty_or_placeholder(plot_deed):
            return None

        is_bn = (lang != "en")

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
            title_bn = "দলিল রেফারেন্সে গরমিল"
            title_en = "Cross-Record Reference Inconsistency"

            explanation_bn = (
                f"প্লটের মূল নথিতে প্রাথমিক দলিল হিসেবে '{plot_deed}' উল্লেখ আছে, কিন্তু সক্রিয় হস্তান্তর রেকর্ডে '{mismatch_list}' উল্লেখ রয়েছে। "
                "দলিল তালিকার এই অসঙ্গতি অনিবন্ধিত বণ্টন, কেরানি সংক্রান্ত ভুল পোস্টিং বা বিরোধপূর্ণ দাবির ইঙ্গিত দেয়।"
            )
            explanation_en = (
                f"The plot master record cites '{plot_deed}' as primary deed, but an active conveyance transaction cites '{mismatch_list}'. "
                "Such discrepancies may indicate unrecorded partitions, clerical errors, or conflicting chain-of-title references."
            )

            action_bn = (
                "সঠিক তফসিল, চৌহদ্দি এবং জমির সীমানা নিশ্চিত করতে সাব-রেজিস্ট্রি অফিস থেকে উভয় দলিলের সার্টিফাইড নকল (Nokol) তুলুন।"
            )
            action_en = (
                "Obtain certified copies (Nokol) of both cited deed numbers from the Sub-Registry office to inspect parcel schedules and boundaries."
            )

            affected_bn = f"প্লট মূল দলিল ({plot_deed}) বনাম ট্রানজ্যাকশন দলিল ({mismatch_list})"
            affected_en = f"Plot Master Deed ({plot_deed}) vs Transaction Deed ({mismatch_list})"

            return {
                "rule_id": "RULE_REF_MISMATCH",
                "title": title_bn if is_bn else title_en,
                "title_bn": title_bn,
                "title_en": title_en,
                "severity": "Medium",
                "badge_class": "warning",
                "severity_display": "মাঝারি" if is_bn else "Medium",
                "affected_field": affected_bn if is_bn else affected_en,
                "explanation": explanation_bn if is_bn else explanation_en,
                "explanation_bn": explanation_bn,
                "explanation_en": explanation_en,
                "recommended_action": action_bn if is_bn else action_en,
                "recommended_action_bn": action_bn,
                "recommended_action_en": action_en,
            }

        return None

    @classmethod
    def _check_case_info(cls, plot: Dict[str, Any], lang: str = "bn") -> Optional[Dict[str, Any]]:
        """
        Rule 4: If case-related information is unavailable, advise verification.
        Does NOT infer that a court case exists.
        """
        val = plot.get("case_info_status")
        val_lower = str(val or "").strip().lower()

        if cls._is_empty_or_placeholder(val) or "unknown" in val_lower or "pending" in val_lower or "unverified" in val_lower:
            is_bn = (lang != "en")
            title_bn = "মামলা বা বিরোধের তথ্য অপ্রাপ্ত"
            title_en = "Litigation / Case Record Unverified"

            explanation_bn = (
                f"এই প্লটের দেওয়ানি আদালতের মামলা বা বাটোয়ারা বিরোধের তথ্য ডেমো রেকর্ডে '{val or 'অজ্ঞাত'}' হিসেবে চিহ্নিত। "
                "মামলার তথ্য না থাকার অর্থ এই নয় যে জমিটি মামলা-মুক্ত।"
            )
            explanation_en = (
                f"Court litigation or partition suit status for this plot is recorded as '{val or 'Unknown'}' in demo data. "
                "The absence of recorded case data does not prove the absence of active legal disputes."
            )

            action_bn = (
                "স্থানীয়ভাবে খোঁজ নিন এবং সংশ্লিষ্ট অধিক্ষেত্রের সহকারী জজ আদালত / যুগ্ম জেলা জজ আদালতের রেজিস্টারে "
                "কোনো মামলা বা নিষেধাজ্ঞা বিচারাধীন আছে কি না তা যাচাই করুন।"
            )
            action_en = (
                "Search civil court registers (Assistant Judge & Joint District Judge courts having jurisdiction) "
                "to confirm no pending title suits or temporary injunctions exist."
            )

            affected_bn = "মামলা বা মোকদ্দমার স্ট্যাটাস"
            affected_en = "Litigation / Case Verification Status"

            return {
                "rule_id": "RULE_UNKNOWN_CASE",
                "title": title_bn if is_bn else title_en,
                "title_bn": title_bn,
                "title_en": title_en,
                "severity": "Info",
                "badge_class": "info",
                "severity_display": "তথ্যমূলক" if is_bn else "Info",
                "affected_field": affected_bn if is_bn else affected_en,
                "explanation": explanation_bn if is_bn else explanation_en,
                "explanation_bn": explanation_bn,
                "explanation_en": explanation_en,
                "recommended_action": action_bn if is_bn else action_en,
                "recommended_action_bn": action_bn,
                "recommended_action_en": action_en,
            }
        return None

    @classmethod
    def _check_khas_acquisition(cls, plot: Dict[str, Any], lang: str = "bn") -> Optional[Dict[str, Any]]:
        """
        Rule 5: If khas or government acquisition info is unavailable, advise verification.
        Does NOT imply that plot is government-owned, acquired, or free from acquisition.
        """
        val = plot.get("khas_acquisition_status")
        val_lower = str(val or "").strip().lower()

        if cls._is_empty_or_placeholder(val) or "unknown" in val_lower or "pending" in val_lower or "unverified" in val_lower:
            is_bn = (lang != "en")
            title_bn = "খাস বা সরকারি অধিগ্রহণ স্ট্যাটাস অপ্রাপ্ত"
            title_en = "Khas / Government Acquisition Unverified"

            explanation_bn = (
                f"জমিটি সরকারি খাস, পরিত্যক্ত বা অর্পিত কি না অথবা কোনো অধিগ্রহণ নোটিশ জারি আছে কি না, তা ডেমো রেকর্ডে '{val or 'অজ্ঞাত'}' হিসেবে আছে। "
                "এই ডেমো ডেটা অধিগ্রহণ প্রক্রিয়া চলছে কি না তা নিশ্চিত করতে পারে না।"
            )
            explanation_en = (
                f"Whether this plot is classified as government Khas, Vested property, or subject to gazetted acquisition notices is recorded as '{val or 'Unknown'}'. "
                "This demonstration dataset cannot confirm government acquisition status."
            )

            action_bn = (
                "উপজেলা ভূমি অফিস (এসি ল্যান্ড) এবং জেলা প্রশাসকের (ডিসি) ভূমি অধিগ্রহণ শাখায় যোগাযোগ করে নিশ্চিত হোন "
                "যে ৪ ধারার কোনো অধিগ্রহণ নোটিশ বা খাস ঘোষণার আওতাভুক্ত নয়।"
            )
            action_en = (
                "Verify with the Upazila Land Office (AC Land) and the Land Acquisition (LA) wing of the Deputy Commissioner's Office "
                "to confirm no Section 4 notices or Khas schedules apply."
            )

            affected_bn = "খাস বা অধিগ্রহণ স্ট্যাটাস"
            affected_en = "Government Khas / Acquisition Status"

            return {
                "rule_id": "RULE_UNKNOWN_KHAS",
                "title": title_bn if is_bn else title_en,
                "title_bn": title_bn,
                "title_en": title_en,
                "severity": "Info",
                "badge_class": "info",
                "severity_display": "তথ্যমূলক" if is_bn else "Info",
                "affected_field": affected_bn if is_bn else affected_en,
                "explanation": explanation_bn if is_bn else explanation_en,
                "explanation_bn": explanation_bn,
                "explanation_en": explanation_en,
                "recommended_action": action_bn if is_bn else action_en,
                "recommended_action_bn": action_bn,
                "recommended_action_en": action_en,
            }
        return None

    @classmethod
    def _check_city_survey(cls, plot: Dict[str, Any], lang: str = "bn") -> Optional[Dict[str, Any]]:
        """
        Rule 6: City Survey Risk Scoring Indicator.
        Adds exactly 1 risk point if survey_type explicitly matches 'City Survey'.
        Does not add points for CS, SA, RS, BS or unknown survey types.
        Accurately explains that this is a configured screening indicator for urban
        cadastral boundary reconciliation, not legal proof of a defective title.
        """
        survey_type = str(plot.get("survey_type") or "").strip()
        survey_type_lower = survey_type.lower()

        # Explicit match for City Survey only
        is_city_survey = (
            survey_type_lower in {"city survey", "city-survey", "citysurvey", "সিটি জরিপ"}
            or "city survey" in survey_type_lower
            or "সিটি জরিপ" in survey_type
        )

        if not is_city_survey:
            return None

        is_bn = (lang != "en")
        title_bn = "সিটি জরিপ স্ক্রীনিং সূচক (+১ ঝুঁকি পয়েন্ট)"
        title_en = "City Survey Screening Indicator (+1 Risk Point)"

        explanation_bn = (
            "এই প্লটের জরিপের ধরন 'City Survey' (সিটি জরিপ) হিসেবে চিহ্নিত। "
            "পৌর ও শহরাঞ্চলে সিটি জরিপ খতিয়ানের ক্ষেত্রে পূর্ববর্তী আরএস বা বিএস জরিপের নকশা ও বায়া দলিলের সাথে "
            f"দাগ ও সীমানা পুঙ্খানুপুঙ্খ সমন্বয় প্রয়োজন হয় বিধায় কনফিগার করা নিয়ম অনুযায়ী ঠিক {cls.CITY_SURVEY_RISK_POINTS}টি "
            "ঝুঁকি পয়েন্ট যোগ করা হয়েছে। এটি কোনো আইনি স্বত্ব ত্রুটির প্রমাণ নয়, বরং সতর্কতামূলক বিশ্লেষণ সূচক।"
        )
        explanation_en = (
            "The recorded survey type for this plot explicitly matches 'City Survey'. "
            "In municipal urban areas, City Survey porchas require rigorous cross-examination against earlier RS/BS cadastral "
            f"maps and historical deeds to verify boundary reconciliation; exactly {cls.CITY_SURVEY_RISK_POINTS} risk point "
            "is added under configured screening rules. This is an informational screening parameter, not legal proof of an ownership defect."
        )

        action_bn = (
            "সিটি জরিপের পর্চা ও নকশার সাথে পূর্ববর্তী আরএস/বিএস খতিয়ানের দাগ নম্বর ও বায়া দলিলের মিল সরেজমিনে পরীক্ষা করুন।"
        )
        action_en = (
            "Cross-examine City Survey porchas and layout sheets against prior RS/BS cadastral maps and historical deeds to verify parcel boundary harmony."
        )

        affected_bn = f"জরিপের ধরন: {survey_type}"
        affected_en = f"Survey Type: {survey_type}"

        return {
            "rule_id": "RULE_CITY_SURVEY",
            "title": title_bn if is_bn else title_en,
            "title_bn": title_bn,
            "title_en": title_en,
            "severity": "Info",
            "badge_class": "info",
            "severity_display": "তথ্যমূলক (+১ পয়েন্ট)" if is_bn else "Info (+1 Point)",
            "risk_points": cls.CITY_SURVEY_RISK_POINTS,
            "affected_field": affected_bn if is_bn else affected_en,
            "explanation": explanation_bn if is_bn else explanation_en,
            "explanation_bn": explanation_bn,
            "explanation_en": explanation_en,
            "recommended_action": action_bn if is_bn else action_en,
            "recommended_action_bn": action_bn,
            "recommended_action_en": action_en,
        }
