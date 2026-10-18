"""
due_diligence_engine.py - Automated 7-Step Land Due-Diligence Verification Engine
BuyerGuard BD — Smart Land Pre-Purchase Verification Platform

Automates the 7 citizen due-diligence checks deterministically from plot and transaction data.
Every check returns a structured dictionary with status, explanation, detected conflicts,
missing evidence, and recommended actions in both Bangla and English.

Status Enum:
- PASS: Available demo records are internally consistent.
- WARNING: A conflict, litigation, or critical warning is detected.
- NEEDS_REVIEW: Manual inquiry, court search, or land office vetting required.
- INSUFFICIENT_DATA: Supporting record is missing or incomplete.
- NOT_APPLICABLE: Step does not apply to this plot (e.g., sole ownership partition).
"""

from typing import Dict, Any, List, Optional


class DiligenceStatus:
    PASS = "PASS"
    WARNING = "WARNING"
    NEEDS_REVIEW = "NEEDS_REVIEW"
    INSUFFICIENT_DATA = "INSUFFICIENT_DATA"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class DueDiligenceEngine:
    """
    Automated verification engine executing the 7 standardized Bangladesh land
    pre-purchase due-diligence checks against database records.
    """

    STATUS_METADATA = {
        DiligenceStatus.PASS: {
            "bn": "যাচাইকৃত (ডেমো রেকর্ড)",
            "en": "Pass (Demo Record)",
            "badge": "success",
        },
        DiligenceStatus.WARNING: {
            "bn": "সতর্কবার্তা সনাক্ত",
            "en": "Warning Identified",
            "badge": "danger",
        },
        DiligenceStatus.NEEDS_REVIEW: {
            "bn": "পর্যালোচনা প্রয়োজন",
            "en": "Needs Manual Review",
            "badge": "warning",
        },
        DiligenceStatus.INSUFFICIENT_DATA: {
            "bn": "তথ্য অপ্রাপ্ত",
            "en": "Insufficient Data",
            "badge": "secondary",
        },
        DiligenceStatus.NOT_APPLICABLE: {
            "bn": "প্রযোজ্য নয়",
            "en": "Not Applicable",
            "badge": "light text-dark border",
        },
    }

    @staticmethod
    def _is_empty(val: Any) -> bool:
        if val is None:
            return True
        s = str(val).strip().lower()
        return s in {"", "none", "null", "missing", "not provided", "not available", "unknown", "n/a", "প্রমাণক অপ্রাপ্ত"}

    @classmethod
    def run_all_checks(
        cls,
        plot: Dict[str, Any],
        transactions: Optional[List[Dict[str, Any]]] = None,
        lang: str = "bn",
    ) -> Dict[str, Any]:
        """
        Execute all 7 verification steps against the provided plot and transactions.
        Returns a structured dictionary with all 7 items and aggregated metrics.
        """
        txs = transactions or []
        is_bn = (lang != "en")

        step1 = cls._check_step_1_deed(plot, txs, is_bn)
        step2 = cls._check_step_2_mutation(plot, txs, is_bn)
        step3 = cls._check_step_3_title_chain(plot, txs, is_bn)
        step4 = cls._check_step_4_partition(plot, txs, is_bn)
        step5 = cls._check_step_5_litigation(plot, txs, is_bn)
        step6 = cls._check_step_6_government_interest(plot, txs, is_bn)

        # Step 7 consumes findings from steps 1-6
        prior_steps = [step1, step2, step3, step4, step5, step6]
        step7 = cls._check_step_7_legal_readiness(plot, prior_steps, is_bn)

        checks = [step1, step2, step3, step4, step5, step6, step7]

        # Calculate counts
        passed_count = sum(1 for c in checks if c["status"] == DiligenceStatus.PASS)
        warning_count = sum(1 for c in checks if c["status"] == DiligenceStatus.WARNING)
        needs_review_count = sum(1 for c in checks if c["status"] == DiligenceStatus.NEEDS_REVIEW)
        insufficient_data_count = sum(1 for c in checks if c["status"] == DiligenceStatus.INSUFFICIENT_DATA)
        not_applicable_count = sum(1 for c in checks if c["status"] == DiligenceStatus.NOT_APPLICABLE)

        summary_title_bn = f"যাচাইকরণ ফলাফল: ৭টি স্বয়ংক্রিয় পরীক্ষা সম্পন্ন"
        summary_title_en = f"Verification Results: 7 Checks Evaluated"

        return {
            "plot_id": plot.get("plot_id"),
            "total_checks": 7,
            "passed_count": passed_count,
            "warning_count": warning_count,
            "needs_review_count": needs_review_count,
            "insufficient_data_count": insufficient_data_count,
            "not_applicable_count": not_applicable_count,
            "summary_title": summary_title_bn if is_bn else summary_title_en,
            "summary_title_bn": summary_title_bn,
            "summary_title_en": summary_title_en,
            "readiness_outcome": step7.get("readiness_outcome"),
            "readiness_outcome_bn": step7.get("readiness_outcome_bn"),
            "readiness_outcome_en": step7.get("readiness_outcome_en"),
            "readiness_badge": step7.get("badge_class"),
            "checks": checks,
        }

    # -------------------------------------------------------------
    # Step 1: Sub-Registry and Deed Verification
    # -------------------------------------------------------------
    @classmethod
    def _check_step_1_deed(
        cls, plot: Dict[str, Any], transactions: List[Dict[str, Any]], is_bn: bool
    ) -> Dict[str, Any]:
        deed_ref = plot.get("deed_ref")
        reg_date = plot.get("reg_date")
        reg_details = plot.get("reg_details")
        office = plot.get("sub_registry_office")

        missing_items = []
        conflicts = []

        if cls._is_empty(deed_ref):
            missing_items.append("মূল দলিল নম্বর" if is_bn else "Primary Deed Reference")
        if cls._is_empty(office):
            missing_items.append("সাব-রেজিস্ট্রি অফিসের নাম" if is_bn else "Sub-Registry Office Name")
        if cls._is_empty(reg_date) and cls._is_empty(reg_details):
            missing_items.append("দলিল নিবন্ধনের তারিখ বা বালামের তথ্য" if is_bn else "Deed Registration Date / Balam Details")

        # Conflict check with active transactions
        active_txs = [t for t in transactions if str(t.get("record_status", "")).lower() == "active"]
        tx_deeds = {t.get("deed_ref") for t in active_txs if not cls._is_empty(t.get("deed_ref"))}

        if len(tx_deeds) > 1:
            conflicts.append(
                f"একাধিক সক্রিয় দলিলের দাবি ({', '.join(sorted(str(d) for d in tx_deeds))})"
                if is_bn else
                f"Multiple concurrent active conveyance claims ({', '.join(sorted(str(d) for d in tx_deeds))})"
            )
        elif deed_ref and tx_deeds and (deed_ref not in tx_deeds):
            conflicts.append(
                f"প্লটের দলিল ({deed_ref}) এবং হস্তান্তরের দলিল ({', '.join(sorted(str(d) for d in tx_deeds))}) ভিন্ন"
                if is_bn else
                f"Plot master deed ({deed_ref}) conflicts with active transaction deed ({', '.join(sorted(str(d) for d in tx_deeds))})"
            )

        if conflicts:
            status = DiligenceStatus.WARNING
            expl_bn = "উপলব্ধ ডেমো নথিতে দলিল নম্বরে পরস্পরবিরোধী তথ্য সনাক্ত হয়েছে। এটি দ্বৈত-বিক্রয় বা কেরানি ভুলের ঝুঁকি নির্দেশ করে।"
            expl_en = "Conflicting deed references detected in available demo records, indicating potential duplicate-sale or indexing inconsistencies."
            action_bn = "সংশ্লিষ্ট সাব-রেজিস্ট্রি অফিসের মূল বালাম বই তল্লাশি করে নিবন্ধিত দলিলের সত্যতা ও তফসিল নিশ্চিত করুন।"
            action_en = "Inspect original Sub-Registry Volume (Balam) books to establish chronological priority and schedule details."
        elif cls._is_empty(deed_ref):
            status = DiligenceStatus.INSUFFICIENT_DATA
            expl_bn = "প্লটের প্রাথমিক রেজিস্ট্রিকৃত দলিল নম্বর ডেমো রেকর্ডে অপ্রাপ্ত।"
            expl_en = "Primary registered deed reference is missing from this demonstration record."
            action_bn = "বিক্রেতার নিকট থেকে নিবন্ধিত মূল সাফ-কবলা/হেবা দলিলের প্রত্যায়িত নকল সংগ্রহ করুন।"
            action_en = "Require certified copies of original registered conveyance deed from the seller."
        elif missing_items:
            status = DiligenceStatus.NEEDS_REVIEW
            expl_bn = f"দলিল নম্বর প্রাপ্ত হলেও নিবন্ধনের কিছু তথ্য ({', '.join(missing_items)}) ডেমো ডেটায় অসম্পূর্ণ।"
            expl_en = f"Deed reference is recorded, but registration attributes ({', '.join(missing_items)}) are incomplete in demo records."
            action_bn = "সাব-রেজিস্ট্রি অফিসে বালাম বই তল্লাশি দিয়ে নিবন্ধন তারিখ ও বালাম নম্বর যাচাই করুন।"
            action_en = "Conduct Sub-Registry office inspection to confirm registration date and volume pages."
        else:
            status = DiligenceStatus.PASS
            expl_bn = f"দলিল নম্বর ({deed_ref}), সাব-রেজিস্ট্রি অফিস ({office}) ও নিবন্ধনের বিবরণ ডেমো রেকর্ডে অভ্যন্তরীণভাবে সামঞ্জস্যপূর্ণ।"
            expl_en = f"Deed reference ({deed_ref}), Sub-Registry Office ({office}), and registration particulars are internally consistent in available demo data."
            action_bn = "চূড়ান্ত চুক্তির পূর্বে সাব-রেজিস্ট্রি বালাম বই তল্লাশি দিয়ে দায়মুক্তি সনদ (Non-Encumbrance Certificate) নিন।"
            action_en = "Obtain certified non-encumbrance certificate (NEC) from the Sub-Registry office prior to contract execution."

        meta = cls.STATUS_METADATA[status]
        title_bn = "মূল দলিল বালাম তল্লাশি ও সাব-রেজিস্ট্রি যাচাইকরণ"
        title_en = "Original Title Deed (Dalil) Volume Book Search & Sub-Registry Verification"
        return {
            "check_id": "step_1_deed_registry",
            "step_number": "১" if is_bn else "1",
            "step_number_int": 1,
            "title": title_bn if is_bn else title_en,
            "title_bn": title_bn,
            "title_en": title_en,
            "authority": office or ("সাব-রেজিস্ট্রি অফিস" if is_bn else "Sub-Registry Office"),
            "status": status,
            "status_label": meta["bn"] if is_bn else meta["en"],
            "status_label_bn": meta["bn"],
            "status_label_en": meta["en"],
            "badge_class": meta["badge"],
            "explanation": expl_bn if is_bn else expl_en,
            "explanation_bn": expl_bn,
            "explanation_en": expl_en,
            "missing_info": ", ".join(missing_items) if missing_items else None,
            "conflicts": "; ".join(conflicts) if conflicts else None,
            "recommended_action": action_bn if is_bn else action_en,
            "official_verification_required": status != DiligenceStatus.PASS,
            "records_referenced": [r for r in [deed_ref, office, reg_date] if r and not cls._is_empty(r)],
        }

    # -------------------------------------------------------------
    # Step 2: Mutation / E-Namjari Verification
    # -------------------------------------------------------------
    @classmethod
    def _check_step_2_mutation(
        cls, plot: Dict[str, Any], transactions: List[Dict[str, Any]], is_bn: bool
    ) -> Dict[str, Any]:
        mut_status = plot.get("mutation_status")
        khatian_ref = plot.get("khatian_ref")
        mut_lower = str(mut_status or "").strip().lower()

        missing_items = []
        conflicts = []

        if cls._is_empty(mut_status):
            missing_items.append("নামজারি অবস্থা" if is_bn else "Mutation Status")
        if cls._is_empty(khatian_ref):
            missing_items.append("খতিয়ান নম্বর" if is_bn else "Khatian Reference")

        if cls._is_empty(mut_status) or "missing" in mut_lower:
            status = DiligenceStatus.INSUFFICIENT_DATA
            expl_bn = "এই প্লটের নামজারি বা ই-নামজারি রেকর্ড ডেমো সিস্টেমে পাওয়া যায়নি।"
            expl_en = "Mutation or e-Namjari records are absent from this demonstration record."
            action_bn = "বিক্রেতার নামে সহকারী কমিশনার (ভূমি) অফিস কর্তৃক নামজারি খতিয়ান সৃজন না হওয়া পর্যন্ত বায়না বা ক্রয় থেকে বিরত থাকুন।"
            action_en = "Do not proceed with purchase until seller obtains mutation khatian in their own name from AC (Land) office."
        elif "pending" in mut_lower:
            status = DiligenceStatus.NEEDS_REVIEW
            expl_bn = f"নামজারি আবেদন প্রক্রিয়াধীন ({mut_status}) হিসেবে ডেমো রেকর্ডে লিপিবদ্ধ রয়েছে।"
            expl_en = f"Mutation application is currently recorded as pending ({mut_status}) in demo data."
            action_bn = "উপজেলা ভূমি অফিসে ই-নামজারি কেস নম্বর ও শুনানির অগ্রগতি যাচাই করুন।"
            action_en = "Track e-Namjari case progress and hearing resolution at the Upazila Land Office."
        elif "mutated" in mut_lower or "complete" in mut_lower:
            if cls._is_empty(khatian_ref):
                status = DiligenceStatus.WARNING
                conflicts.append("নামজারি সম্পন্ন দাবি করা হলেও খতিয়ান নম্বর অনুপস্থিত" if is_bn else "Mutation claimed complete but khatian reference is missing")
                expl_bn = "নামজারি সম্পন্ন দাবি করা হলেও খতিয়ান নম্বর পাওয়া যায়নি, যা অসম্পূর্ণ বা ভুয়া রেকর্ডের ইঙ্গিত দিতে পারে।"
                expl_en = "Mutation is marked complete but khatian number is missing, signaling inconsistent demonstration records."
                action_bn = "এসি ল্যান্ড অফিসে নামজারি খতিয়ান পর্চা ও ডিসিআরের সত্যতা যাচাই করুন।"
                action_en = "Verify mutation porcha and DCR at AC (Land) office."
            else:
                status = DiligenceStatus.PASS
                expl_bn = f"নামজারি রেকর্ড সম্পন্ন ({mut_status}) এবং খতিয়ান নম্বর ({khatian_ref}) ডেমো নথিতে বিদ্যমান।"
                expl_en = f"Mutation status recorded as completed ({mut_status}) with valid khatian reference ({khatian_ref}) in demo records."
                action_bn = "ভূমি উন্নয়ন কর পরিশোধের হাল সনের দাখিলা (Dakhila) সংগ্রহ করুন।"
                action_en = "Verify latest Land Development Tax receipt (Dakhila) against this mutation khatian."
        else:
            status = DiligenceStatus.NEEDS_REVIEW
            expl_bn = f"নামজারি স্ট্যাটাস অস্পষ্ট ({mut_status})।"
            expl_en = f"Mutation status is ambiguous ({mut_status}) in demo data."
            action_bn = "ভূমি অফিসে রেকর্ড যাচাই করুন।"
            action_en = "Verify record status with local land revenue authorities."

        meta = cls.STATUS_METADATA[status]
        return {
            "check_id": "step_2_mutation",
            "step_number": "২" if is_bn else "2",
            "step_number_int": 2,
            "title": "নামজারি / ই-নামজারি যাচাইকরণ" if is_bn else "Mutation / E-Namjari Verification",
            "title_bn": "নামজারি / ই-নামজারি যাচাইকরণ",
            "title_en": "Mutation / E-Namjari Verification",
            "authority": "সহকারী কমিশনার (ভূমি) অফিস" if is_bn else "AC (Land) Office",
            "status": status,
            "status_label": meta["bn"] if is_bn else meta["en"],
            "status_label_bn": meta["bn"],
            "status_label_en": meta["en"],
            "badge_class": meta["badge"],
            "explanation": expl_bn if is_bn else expl_en,
            "explanation_bn": expl_bn,
            "explanation_en": expl_en,
            "missing_info": ", ".join(missing_items) if missing_items else None,
            "conflicts": "; ".join(conflicts) if conflicts else None,
            "recommended_action": action_bn if is_bn else action_en,
            "official_verification_required": status != DiligenceStatus.PASS,
            "records_referenced": [r for r in [khatian_ref, mut_status] if r and not cls._is_empty(r)],
        }

    # -------------------------------------------------------------
    # Step 3: Historical Title Deed Chain Verification
    # -------------------------------------------------------------
    @classmethod
    def _check_step_3_title_chain(
        cls, plot: Dict[str, Any], transactions: List[Dict[str, Any]], is_bn: bool
    ) -> Dict[str, Any]:
        if not transactions:
            status = DiligenceStatus.INSUFFICIENT_DATA
            expl_bn = "এই প্লটের পূর্ববর্তী কোনো লেনদেন বা বায়া দলিলের ইতিহাস ডেমো ডাটাবেজে সংরক্ষিত নেই।"
            expl_en = "No prior transaction or chain-of-title records are available in the demonstration database."
            action_bn = "কমপক্ষে ১২ থেকে ২৫ বছরের পূর্ববর্তী ধারাবাহিক বায়া দলিল ও জরিপ খতিয়ান তলব করুন।"
            action_en = "Demand continuous historical chain deeds (Bia Dalil) spanning at least 12 to 25 years."
            conflicts = None
            missing = "ঐতিহাসিক বায়া দলিলের তালিকা" if is_bn else "Historical Title Deeds List"
        else:
            # Check for conflict groups or double-sale markers
            conflict_groups = [t.get("conflict_group_id") for t in transactions if t.get("conflict_group_id")]
            active_txs = [t for t in transactions if str(t.get("record_status", "")).lower() == "active"]
            active_deeds = {t.get("deed_ref") for t in active_txs if not cls._is_empty(t.get("deed_ref"))}

            if conflict_groups or len(active_deeds) > 1:
                status = DiligenceStatus.WARNING
                conflicts = (
                    f"সক্রিয় দ্বৈত-বিক্রয় সংঘাত ({', '.join(sorted(str(c) for c in set(conflict_groups)))})"
                    if is_bn else
                    f"Active conflicting sale claims ({', '.join(sorted(str(c) for c in set(conflict_groups)))})"
                )
                missing = None
                expl_bn = f"মালিকানা চেইনে একই জমির বিপরীতে একাধিক সক্রিয় দলিল ({', '.join(sorted(str(d) for d in active_deeds))}) পাওয়া গেছে।"
                expl_en = f"Ownership chain contains concurrent competing active deeds ({', '.join(sorted(str(d) for d in active_deeds))})."
                action_bn = "অবিলম্বে সাব-রেজিস্ট্রি অফিসে তল্লাশি দিন এবং কোনো জাল বা সমান্তরাল দলিল তৈরি হয়েছে কি না পরীক্ষা করুন।"
                action_en = "Immediately conduct exhaustive Sub-Registry searches to isolate fraudulent or parallel deeds."
            else:
                status = DiligenceStatus.PASS
                conflicts = None
                missing = None
                expl_bn = f"উপলব্ধ ডেমো নথিতে {len(transactions)}টি হস্তান্তরের ধারাবাহিকতা কালানুক্রমিকভাবে সঙ্গতিপূর্ণ।"
                expl_en = f"Available demo data contains {len(transactions)} conveyance record(s) exhibiting consistent chronological continuity."
                action_bn = "মূল বায়া দলিলগুলোর সাথে জেলা রেকর্ড রুমের সিএস, এসএ, আরএস খতিয়ানের ধারাবাহিকতা মিলিয়ে দেখুন।"
                action_en = "Cross-examine original Bia deeds against historical survey records (CS/SA/RS) at District Record Room."

        meta = cls.STATUS_METADATA[status]
        return {
            "check_id": "step_3_title_chain",
            "step_number": "৩" if is_bn else "3",
            "step_number_int": 3,
            "title": "ধারাবাহিক বায়া দলিল ও স্বত্ব চেইন" if is_bn else "Historical Title Deed Chain Verification",
            "title_bn": "ধারাবাহিক বায়া দলিল ও স্বত্ব চেইন",
            "title_en": "Historical Title Deed Chain Verification",
            "authority": "জেলা রেকর্ড রুম ও সাব-রেজিস্ট্রি" if is_bn else "District Record Room & Sub-Registry",
            "status": status,
            "status_label": meta["bn"] if is_bn else meta["en"],
            "status_label_bn": meta["bn"],
            "status_label_en": meta["en"],
            "badge_class": meta["badge"],
            "explanation": expl_bn if is_bn else expl_en,
            "explanation_bn": expl_bn,
            "explanation_en": expl_en,
            "missing_info": missing,
            "conflicts": conflicts,
            "recommended_action": action_bn if is_bn else action_en,
            "official_verification_required": status != DiligenceStatus.PASS,
            "records_referenced": [t.get("transaction_ref") for t in transactions[:3] if t.get("transaction_ref")],
        }

    # -------------------------------------------------------------
    # Step 4: Partition Deed and Ownership-Share Verification
    # -------------------------------------------------------------
    @classmethod
    def _check_step_4_partition(
        cls, plot: Dict[str, Any], transactions: List[Dict[str, Any]], is_bn: bool
    ) -> Dict[str, Any]:
        partition_status = plot.get("partition_deed_status")
        ownership_source = plot.get("ownership_source")
        source_lower = str(ownership_source or "").lower()
        part_lower = str(partition_status or "").lower()

        missing = None
        conflicts = None

        # Check if single owner / not applicable
        if "একক স্বত্ব" in part_lower or "not applicable" in part_lower or ("ক্রয়" in source_lower and "বণ্টন প্রযোজ্য নয়" in part_lower):
            status = DiligenceStatus.NOT_APPLICABLE
            expl_bn = f"মালিকানা অর্জনের উৎস '{ownership_source or 'ক্রয় সূত্রে'}' এবং রেকর্ডটি একক স্বত্বভুক্ত হওয়ায় বণ্টননামার বাধ্যবাধকতা প্রযোজ্য নয়।"
            expl_en = f"Ownership source is recorded as '{ownership_source or 'By Purchase'}' under sole tenancy; partition deed is not applicable."
            action_bn = "বিক্রেতার নিরঙ্কুশ একক স্বত্ব ও দখলে থাকার বিষয়টি সরেজমিনে নিশ্চিত করুন।"
            action_en = "Confirm physical possession and sole ownership demarcation on site."
        elif "রেজিস্ট্রিকৃত আপস-বণ্টননামা" in part_lower or "registered partition" in part_lower:
            status = DiligenceStatus.PASS
            expl_bn = f"ডেমো নথিতে রেজিস্ট্রিকৃত আপস-বণ্টননামা ({partition_status}) লিপিবদ্ধ রয়েছে এবং শরিকি হিস্যা চিহ্নিত।"
            expl_en = f"Registered partition deed is documented ({partition_status}) with demarcated heirship shares."
            action_bn = "বণ্টন দলিলের মানচিত্র ও চৌহদ্দি অনুসারে সরেজমিনে সীমানা পরিমাপ করুন।"
            action_en = "Demarcate ground boundaries according to partition deed schedule and map."
        elif "অবণ্টনকৃত" in part_lower or "unpartitioned" in part_lower or "ওয়ারিশ" in source_lower:
            status = DiligenceStatus.WARNING
            conflicts = "অবণ্টনকৃত যৌথ সম্পত্তি — শরিকদের অধিকার ও হক শুফা ঝুঁকি" if is_bn else "Unpartitioned joint holding — pre-emption / co-sharer risk"
            expl_bn = "জমিটি পৈতৃক/ওয়ারিশ সূত্রে প্রাপ্ত হলেও সকল শরিকের মধ্যে কোনো রেজিস্ট্রিকৃত বাটোয়ারা বা আপস-বণ্টননামা দলিল ডেমো রেকর্ডে নেই।"
            expl_en = "Property originates through inheritance, but no registered partition deed (Bontonnama) among all co-heirs exists in demo records."
            action_bn = "ইউনিয়ন পরিষদ/পৌরসভা থেকে ওয়ারিশ সনদ নিন এবং রেজিস্ট্রেশন আইন অনুসারে রেজিস্ট্রিকৃত আপস-বণ্টননামা সম্পাদন করান।"
            action_en = "Obtain certified heirship certificate and mandate an executed registered partition deed before purchase."
        elif cls._is_empty(partition_status) or "প্রমাণক অপ্রাপ্ত" in part_lower or "evidence not available" in part_lower:
            status = DiligenceStatus.INSUFFICIENT_DATA
            missing = "ওয়ারিশ সনদ ও বণ্টননামা প্রমাণক" if is_bn else "Heirship Certificate & Partition Evidence"
            expl_bn = "বণ্টননামা দলিল বা ওয়ারিশি হিস্যার তথ্য ডেমো রেকর্ডে অপ্রাপ্ত।"
            expl_en = "Partition deed or ownership share evidence is absent from the available records."
            action_bn = "বিক্রেতার ওয়ারিশ সনদ ও পূর্ববর্তী মালিকানার উৎস যাচাই করুন।"
            action_en = "Verify genealogy certificate and underlying source of ownership."
        else:
            status = DiligenceStatus.NEEDS_REVIEW
            expl_bn = f"বণ্টন সংক্রান্ত তথ্য '{partition_status}' পর্যালোচনার দাবি রাখে।"
            expl_en = f"Partition status '{partition_status}' requires manual verification."
            action_bn = "আইনজীবীর মাধ্যমে ওয়ারিশ সনদ ও বণ্টনের বৈধতা যাচাই করুন।"
            action_en = "Have an advocate verify genealogy and co-ownership distribution."

        meta = cls.STATUS_METADATA[status]
        return {
            "check_id": "step_4_partition_share",
            "step_number": "৪" if is_bn else "4",
            "step_number_int": 4,
            "title": "আপস-বণ্টননামা ও মালিকানার হিস্যা" if is_bn else "Partition Deed & Ownership-Share Verification",
            "title_bn": "আপস-বণ্টননামা ও মালিকানার হিস্যা",
            "title_en": "Partition Deed & Ownership-Share Verification",
            "authority": "সাব-রেজিস্ট্রি ও স্থানীয় পরিষদ" if is_bn else "Sub-Registry & Local Parishad",
            "status": status,
            "status_label": meta["bn"] if is_bn else meta["en"],
            "status_label_bn": meta["bn"],
            "status_label_en": meta["en"],
            "badge_class": meta["badge"],
            "explanation": expl_bn if is_bn else expl_en,
            "explanation_bn": expl_bn,
            "explanation_en": expl_en,
            "missing_info": missing,
            "conflicts": conflicts,
            "recommended_action": action_bn if is_bn else action_en,
            "official_verification_required": status in {DiligenceStatus.WARNING, DiligenceStatus.NEEDS_REVIEW, DiligenceStatus.INSUFFICIENT_DATA},
            "records_referenced": [r for r in [partition_status, ownership_source] if r and not cls._is_empty(r)],
        }

    # -------------------------------------------------------------
    # Step 5: Civil Court Case and Litigation Check
    # -------------------------------------------------------------
    @classmethod
    def _check_step_5_litigation(
        cls, plot: Dict[str, Any], transactions: List[Dict[str, Any]], is_bn: bool
    ) -> Dict[str, Any]:
        case_info = plot.get("case_info_status")
        case_details = plot.get("case_details")
        case_str = f"{case_info or ''} {case_details or ''}".lower()

        conflicts = None
        missing = None

        if "suit" in case_str or "মোকদ্দমা" in case_str or "মামলা চলমান" in case_str or "active case" in case_str:
            status = DiligenceStatus.WARNING
            conflicts = case_details or case_info
            expl_bn = f"কাল্পনিক ডেমো রেকর্ডে এই প্লটের বিপরীতে আদালতের মামলা বা বিরোধের তথ্য রয়েছে: {case_details or case_info}।"
            expl_en = f"Litigation warning recorded in demo dataset: {case_details or case_info}."
            action_bn = "সংশ্লিষ্ট দেওয়ানি আদালত থেকে আরজি ও অন্তর্বর্তীকালীন কোনো নিষেধাজ্ঞা (Injunction) আছে কি না তা আইনজীবীর মাধ্যমে পরীক্ষা করুন।"
            action_en = "Engage counsel to search court registers for plaint details, injunctions, or lis pendens restrictions."
        elif cls._is_empty(case_info) or "unknown" in case_str or "pending" in case_str or "unverified" in case_str:
            status = DiligenceStatus.NEEDS_REVIEW
            missing = "আদালত অনুসন্ধান প্রতিবেদন" if is_bn else "Court Register Search Report"
            expl_bn = f"আদালতের মামলার তথ্য ডেমো রেকর্ডে '{case_info or 'অজ্ঞাত'}' হিসেবে চিহ্নিত। তথ্য না থাকার অর্থ মামলা-মুক্ত নয়।"
            expl_en = f"Litigation status recorded as '{case_info or 'Unknown'}' in demo data. Absence of records does not prove absence of disputes."
            action_bn = "অধিক্ষেত্রাধীন সহকারী জজ ও যুগ্ম জেলা জজ আদালতে স্বত্ব মোকদ্দমা রেজিস্টার তল্লাশি দিন।"
            action_en = "Inspect title suit registers at local Assistant Judge and Joint District Judge courts."
        else:
            status = DiligenceStatus.PASS
            expl_bn = "উপলব্ধ ডেমো রেকর্ডে কোনো দেওয়ানি মোকদ্দমা বা নিষেধাজ্ঞার তথ্য পাওয়া যায়নি। (বাস্তব ক্ষেত্রে আদালত তল্লাশি অপরিহার্য)।"
            expl_en = "No case reported in available demo records. (This demo does not guarantee the plot is free from litigation in reality)."
            action_bn = "স্থানীয়ভাবে বিরোধ ও দখলদারিত্বের বিষয়ে তথ্য সংগ্রহ করুন।"
            action_en = "Inquire locally regarding possessory tranquility and unrecorded family disputes."

        meta = cls.STATUS_METADATA[status]
        return {
            "check_id": "step_5_litigation",
            "step_number": "৫" if is_bn else "5",
            "step_number_int": 5,
            "title": "দেওয়ানি আদালত মামলা ও স্বত্ব বিরোধ" if is_bn else "Civil Court Case & Litigation Check",
            "title_bn": "দেওয়ানি আদালত মামলা ও স্বত্ব বিরোধ",
            "title_en": "Civil Court Case & Litigation Check",
            "authority": "যুগ্ম জেলা জজ আদালত" if is_bn else "Joint District Judge Court",
            "status": status,
            "status_label": meta["bn"] if is_bn else meta["en"],
            "status_label_bn": meta["bn"],
            "status_label_en": meta["en"],
            "badge_class": meta["badge"],
            "explanation": expl_bn if is_bn else expl_en,
            "explanation_bn": expl_bn,
            "explanation_en": expl_en,
            "missing_info": missing,
            "conflicts": conflicts,
            "recommended_action": action_bn if is_bn else action_en,
            "official_verification_required": True,
            "records_referenced": [r for r in [case_info, case_details] if r and not cls._is_empty(r)],
        }

    # -------------------------------------------------------------
    # Step 6: Khas, Vested Property, Government Interest & Acquisition Check
    # -------------------------------------------------------------
    @classmethod
    def _check_step_6_government_interest(
        cls, plot: Dict[str, Any], transactions: List[Dict[str, Any]], is_bn: bool
    ) -> Dict[str, Any]:
        khas_status = plot.get("khas_acquisition_status")
        gov_details = plot.get("gov_interest_details")
        gov_str = f"{khas_status or ''} {gov_details or ''}".lower()

        conflicts = None
        missing = None

        if "warning identified" in gov_str or "khas schedule" in gov_str or "অর্পিত" in gov_str or "খাস" in gov_str and "not marked" not in gov_str:
            status = DiligenceStatus.WARNING
            conflicts = gov_details or khas_status
            expl_bn = f"সতর্কবার্তা: জমিটি সরকারি স্বার্থ বা খাস/অর্পিত তালিকাভুক্তির সম্ভাব্য ইঙ্গিতবাহী ({gov_details or khas_status})।"
            expl_en = f"Warning Identified: Plot contains potential government Khas or Vested property indicator ({gov_details or khas_status})."
            action_bn = "সহকারী কমিশনার (ভূমি) এবং জেলা প্রশাসকের কার্যালয়ে খাস/অর্পিত রেজিস্টার পরীক্ষা করুন।"
            action_en = "Examine official Khas and Vested property registers ('Ka'/'Kha' schedules) at AC (Land) office."
        elif cls._is_empty(khas_status) or "unknown" in gov_str or "pending" in gov_str or "inquiry" in gov_str or "vetting" in gov_str:
            status = DiligenceStatus.NEEDS_REVIEW
            missing = "ভূমি অধিগ্রহণ শাখা ছাড়পত্র" if is_bn else "Land Acquisition Wing Clearance"
            expl_bn = f"খাস বা অধিগ্রহণ স্ট্যাটাস ডেমো রেকর্ডে '{khas_status or 'অজ্ঞাত'}'। সরকারি দপ্তর থেকে যাচাইকরণ আবশ্যক।"
            expl_en = f"Needs Official Verification: Khas or acquisition status is recorded as '{khas_status or 'Unknown'}'. Official vetting required."
            action_bn = "ডিসি অফিসের ভূমি অধিগ্রহণ (LA) শাখায় ৪ ধারার কোনো নোটিশ আছে কি না নিশ্চিত হোন।"
            action_en = "Verify with DC Office Land Acquisition wing that no Section 4 public project acquisition notice is served."
        else:
            status = DiligenceStatus.PASS
            expl_bn = "No Warning Indicator in Available Demo Data: ডেমো রেকর্ডে কোনো খাস বা অধিগ্রহণের তথ্য নেই। (এটি সরকারি ছাড়পত্র নয়)।"
            expl_en = "No Warning Indicator in Available Demo Data: No government Khas or acquisition notice identified in demo records."
            action_bn = "উপজেলা ভূমি অফিসে ১ নং খতিয়ান (খাস খতিয়ান) বহির্ভূত হওয়ার বিষয়টি নিশ্চিত করুন।"
            action_en = "Confirm parcel is excluded from Register 1 (Government Khas Khatian) at Upazila Land Office."

        meta = cls.STATUS_METADATA[status]
        return {
            "check_id": "step_6_government_interest",
            "step_number": "৬" if is_bn else "6",
            "step_number_int": 6,
            "title": "খাস, অর্পিত ও সরকারি অধিগ্রহণ" if is_bn else "Government Interest, Khas & Acquisition Check",
            "title_bn": "খাস, অর্পিত ও সরকারি অধিগ্রহণ",
            "title_en": "Government Interest, Khas & Acquisition Check",
            "authority": "উপজেলা ভূমি অফিস ও ডিসি অফিস (LA)" if is_bn else "AC (Land) & DC Office (LA)",
            "status": status,
            "status_label": meta["bn"] if is_bn else meta["en"],
            "status_label_bn": meta["bn"],
            "status_label_en": meta["en"],
            "badge_class": meta["badge"],
            "explanation": expl_bn if is_bn else expl_en,
            "explanation_bn": expl_bn,
            "explanation_en": expl_en,
            "missing_info": missing,
            "conflicts": conflicts,
            "recommended_action": action_bn if is_bn else action_en,
            "official_verification_required": True,
            "records_referenced": [r for r in [khas_status, gov_details] if r and not cls._is_empty(r)],
        }

    # -------------------------------------------------------------
    # Step 7: Preliminary Legal-Review Readiness
    # -------------------------------------------------------------
    @classmethod
    def _check_step_7_legal_readiness(
        cls, plot: Dict[str, Any], prior_steps: List[Dict[str, Any]], is_bn: bool
    ) -> Dict[str, Any]:
        """
        Synthesizes results from steps 1-6 into a preliminary screening summary.
        Does NOT replace an advocate.
        """
        unresolved_warnings = [s for s in prior_steps if s["status"] == DiligenceStatus.WARNING]
        unresolved_reviews = [s for s in prior_steps if s["status"] == DiligenceStatus.NEEDS_REVIEW]
        missing_data_steps = [s for s in prior_steps if s["status"] == DiligenceStatus.INSUFFICIENT_DATA]

        # Missing core identifiers
        missing_identifiers = []
        if cls._is_empty(plot.get("deed_ref")):
            missing_identifiers.append("মূল দলিল নম্বর" if is_bn else "Deed Number")
        if cls._is_empty(plot.get("khatian_ref")):
            missing_identifiers.append("খতিয়ান নম্বর" if is_bn else "Khatian Number")
        if cls._is_empty(plot.get("dag_no")):
            missing_identifiers.append("দাগ নম্বর" if is_bn else "Dag Number")
        if cls._is_empty(plot.get("mutation_status")):
            missing_identifiers.append("নামজারি" if is_bn else "Mutation")

        # Determine outcome category
        if unresolved_warnings:
            outcome_key = "HIGH_PRIORITY_REVIEW"
            outcome_bn = "জরুরি আইনি পর্যালোচনা আবশ্যক (High-Priority Legal Review Recommended)"
            outcome_en = "High-Priority Legal Review Recommended"
            badge = "danger"
            status = DiligenceStatus.WARNING
            expl_bn = (
                f"স্বয়ংক্রিয় প্রাথমিক স্ক্রীনিংয়ে {len(unresolved_warnings)}টি সতর্কবার্তা সনাক্ত হয়েছে "
                f"({', '.join(w['title_bn'] for w in unresolved_warnings)})। "
                "আইনজীবীর মাধ্যমে বিরোধ ও নথির সত্যতা নিশ্চিত না হওয়া পর্যন্ত আর্থিক লেনদেন ঝুঁকিপূর্ণ।"
            )
            expl_en = (
                f"Automated screening detected {len(unresolved_warnings)} active warning(s) "
                f"({', '.join(w['title_en'] for w in unresolved_warnings)}). "
                "Engage professional legal counsel immediately to evaluate identified risks before transferring funds."
            )
        elif missing_identifiers or missing_data_steps:
            outcome_key = "ADDITIONAL_DOCS_REQUIRED"
            outcome_bn = "অতিরিক্ত নথি প্রয়োজন (Additional Documents Required)"
            outcome_en = "Additional Documents Required"
            badge = "warning"
            status = DiligenceStatus.NEEDS_REVIEW
            missing_str = ", ".join(missing_identifiers) if missing_identifiers else "প্রয়োজনীয় প্রমাণক"
            expl_bn = (
                f"পরিপূর্ণ মূল্যায়নের পূর্বে বিক্রেতার কাছ থেকে অতিরিক্ত নথি তলব করা আবশ্যক ({missing_str})। "
                "নথি ঘাটতি থাকলে সঠিক বায়া দলিল চেইন ও নামজারি নির্ধারণ করা যায় না।"
            )
            expl_en = (
                f"Essential records are incomplete before comprehensive title vetting ({', '.join(missing_identifiers) or 'supporting evidence'}). "
                "Demand certified copies from the seller before proceeding to drafting."
            )
        elif unresolved_reviews:
            outcome_key = "READY_FOR_REVIEW"
            outcome_bn = "পেশাদার আইনি পর্যালোচনার জন্য প্রস্তুত (Ready for Professional Review)"
            outcome_en = "Ready for Professional Review"
            badge = "info"
            status = DiligenceStatus.NEEDS_REVIEW
            expl_bn = (
                "প্রাথমিক ডেটা প্রস্তুত রয়েছে। তবে আদালত তল্লাশি ও খাস/অধিগ্রহণ সংক্রান্ত কিছু দাপ্তরিক যাচাইকরণ "
                "একজন সনদপ্রাপ্ত বার কাউন্সিল আইনজীবীর মাধ্যমে সম্পাদন করা প্রয়োজন।"
            )
            expl_en = (
                "Preliminary records are gathered. Proceed with an enrolled Bar Council advocate to conduct "
                "formal civil court searches and municipal/land office clearances."
            )
        else:
            outcome_key = "READY_FOR_REVIEW"
            outcome_bn = "পেশাদার আইনি পর্যালোচনার জন্য প্রস্তুত (Ready for Professional Review)"
            outcome_en = "Ready for Professional Review"
            badge = "success"
            status = DiligenceStatus.PASS
            expl_bn = (
                "উপলব্ধ ডেমো ডেটায় কোনো সংঘাত সনাক্ত হয়নি। সাফ-কবলা চুক্তি সম্পাদনের জন্য "
                "আইনজীবীর মাধ্যমে চূড়ান্ত দলিল খসড়া ও চৌহদ্দি যাচাই করার পরামর্শ দেওয়া হচ্ছে।"
            )
            expl_en = (
                "Available demonstration records exhibit internal consistency. Retain an advocate to inspect "
                "original physical volumes, draft conveyance deed covenants, and certify possession."
            )

        action_bn = (
            "বাংলাদেশ বার কাউন্সিলের সনদপ্রাপ্ত একজন সিভিল ল' বিশেষজ্ঞ আইনজীবীর মাধ্যমে তল্লাশিনামা ও "
            "স্বত্ব প্রতিবেদন (Legal Title Opinion) প্রস্তুত করান।"
        )
        action_en = (
            "Retain an enrolled Bar Council advocate to produce a formal written Title Opinion and physically verify Balam book indexes."
        )

        title_bn = "স্বয়ংক্রিয় প্রাথমিক স্ক্রীনিং — আইনজীবী দ্বারা যাচাইকরণ এখনও আবশ্যক"
        title_en = "Automated Preliminary Screening — Advocate Review Still Required"

        meta = cls.STATUS_METADATA[status]
        return {
            "check_id": "step_7_legal_readiness",
            "step_number": "৭" if is_bn else "7",
            "step_number_int": 7,
            "title": title_bn if is_bn else title_en,
            "title_bn": title_bn,
            "title_en": title_en,
            "authority": "বার কাউন্সিল আইনজীবী" if is_bn else "Bar Council Enrolled Advocate",
            "status": status,
            "status_label": meta["bn"] if is_bn else meta["en"],
            "status_label_bn": meta["bn"],
            "status_label_en": meta["en"],
            "badge_class": badge,
            "explanation": expl_bn if is_bn else expl_en,
            "explanation_bn": expl_bn,
            "explanation_en": expl_en,
            "missing_info": ", ".join(missing_identifiers) if missing_identifiers else None,
            "conflicts": "; ".join(w["title_bn"] if is_bn else w["title_en"] for w in unresolved_warnings) if unresolved_warnings else None,
            "recommended_action": action_bn if is_bn else action_en,
            "official_verification_required": True,
            "readiness_outcome": outcome_bn if is_bn else outcome_en,
            "readiness_outcome_bn": outcome_bn,
            "readiness_outcome_en": outcome_en,
            "readiness_outcome_key": outcome_key,
            "records_referenced": [w["check_id"] for w in unresolved_warnings],
        }
