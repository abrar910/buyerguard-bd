"""
haq_shufa_engine.py - Deterministic Legal Information Assessment Engine for Haq Shufa
BuyerGuard BD — Smart Land Pre-Purchase Verification Platform

Provides educational classification of pre-emption (Haq Shufa / Right of Pre-emption) risk indicators
under Bangladeshi statutory frameworks and Muslim personal law:
1. The State Acquisition and Tenancy Act, 1950 (Section 96) - Agricultural land
2. The Non-Agricultural Tenancy Act, 1949 (Section 24) - Non-agricultural land
3. Muslim Law of Pre-emption (Haq Shufa) - Co-sharers, appendages, and vicinage

IMPORTANT LEGAL GOVERNANCE:
- Results are strictly informational categories:
    * "Further Legal Review Required"
    * "Relevant Facts Need Verification"
    * "No Risk Indicator Found in Provided Information"
- Never definitively decides that a property is or is not subject to pre-emption.
- Strictly educational simulation; does not substitute for an enrolled Advocate's title opinion.
"""

from typing import Dict, Any, List, Optional


class HaqShufaEngine:
    CATEGORY_REVIEW_REQUIRED = "Further Legal Review Required"
    CATEGORY_FACTS_NEEDED = "Relevant Facts Need Verification"
    CATEGORY_NO_RISK_FOUND = "No Risk Indicator Found in Provided Information"

    VERIFIED_STATUTES = [
        {
            "act": "The State Acquisition and Tenancy Act, 1950",
            "section": "Section 96",
            "scope": "Agricultural land (holding of a raiyat)",
            "applicability": "Right of pre-emption restricted exclusively to co-sharer tenants by inheritance following the 2006 statutory amendment (Act XXXIV of 2006). Co-sharers by purchase and contiguous holders are omitted.",
            "limitation": "Within 2 months of the service of notice under section 89, or within 2 months of the date of knowledge if notice was not served.",
            "url": "http://bdlaws.minlaw.gov.bd/act-241/section-8698.html",
        },
        {
            "act": "The Non-Agricultural Tenancy Act, 1949",
            "section": "Section 24",
            "scope": "Non-agricultural land (residential, commercial, homestead tenancies)",
            "applicability": "Right of pre-emption exercisable by any co-sharer tenant (whether by purchase or inheritance) where a portion of the tenancy is transferred.",
            "limitation": "Within 4 months of the service of notice under section 23; or if notice is not served, within the applicable general limitation period from date of knowledge (Article 181 of Limitation Act 1908).",
            "url": "http://bdlaws.minlaw.gov.bd/act-231/section-8479.html",
        },
        {
            "act": "Muslim Personal Law (Haq Shufa / Right of Pre-emption)",
            "section": "General Muhammadan Law Doctrine",
            "scope": "Applies where statutory pre-emption is inapplicable or regarding contiguous lands and shared easements.",
            "applicability": "Recognizes three classes of pre-emptors (Shufis): (1) Shafi-i-Sharik (co-sharers), (2) Shafi-i-Khalit (participators in appendages/easements), (3) Shafi-i-Jar (owners of adjoining property). Requires strict performance of three Demands (Talab-i-Mowasibat, Talab-i-Ishhad, and Talab-i-Tamlik).",
            "limitation": "Immediate performance of Talab-i-Mowasibat upon hearing of sale, followed promptly by Talab-i-Ishhad before witnesses.",
            "url": "http://bdlaws.minlaw.gov.bd/act-48/section-1601.html",
        },
    ]

    @classmethod
    def get_synthetic_scenarios(cls) -> List[Dict[str, Any]]:
        """Return deterministic synthetic educational scenarios for interactive demonstrations."""
        return [
            {
                "id": "DEMO-SHUFA-01",
                "title": "Synthetic Scenario 1: Undivided Agricultural Inheritance Land",
                "description": "Seller is transferring an undivided share in agricultural land inherited jointly with family heirs, without a registered partition deed or co-sharer notice.",
                "data": {
                    "property_type": "agricultural",
                    "co_ownership": "inheritance_undivided",
                    "partition_status": "unpartitioned_no_deed",
                    "transfer_scope": "undivided_share_stranger",
                    "notice_status": "no_notice_served",
                    "easement_status": "independent",
                },
            },
            {
                "id": "DEMO-SHUFA-02",
                "title": "Synthetic Scenario 2: Unverified Co-Ownership & Partition Facts",
                "description": "Fictional plot scenario where property classification, co-sharer genealogy, and partition deed records remain unverified.",
                "data": {
                    "property_type": "unsure",
                    "co_ownership": "unsure",
                    "partition_status": "unknown_partition",
                    "transfer_scope": "unsure",
                    "notice_status": "unknown_notice",
                    "easement_status": "unsure",
                },
            },
            {
                "id": "DEMO-SHUFA-03",
                "title": "Synthetic Scenario 3: Partitioned Sole Holding with Mutated Khatian",
                "description": "Property separated through registered partition deed, dedicated independent mutated khatian, distinct survey boundaries, and sole ownership.",
                "data": {
                    "property_type": "agricultural",
                    "co_ownership": "sole_ownership",
                    "partition_status": "formal_registered_partition",
                    "transfer_scope": "entire_demarcated_holding",
                    "notice_status": "not_applicable_sole",
                    "easement_status": "independent",
                },
            },
        ]

    @classmethod
    def evaluate(cls, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate user or synthetic questionnaire responses and categorize pre-emption risk indicators.
        Returns one of three strictly informational categories.
        """
        property_type = (form_data.get("property_type") or "").strip().lower()
        co_ownership = (form_data.get("co_ownership") or "").strip().lower()
        partition_status = (form_data.get("partition_status") or "").strip().lower()
        transfer_scope = (form_data.get("transfer_scope") or "").strip().lower()
        notice_status = (form_data.get("notice_status") or "").strip().lower()
        easement_status = (form_data.get("easement_status") or "").strip().lower()

        findings: List[Dict[str, str]] = []
        applicable_statutes: List[Dict[str, Any]] = []
        review_indicators = 0
        missing_fact_indicators = 0

        # 1. Evaluate Property Classification
        if property_type == "agricultural":
            applicable_statutes.append(cls.VERIFIED_STATUTES[0])  # SAT Act s.96
            findings.append({
                "factor": "Property Classification: Agricultural Land",
                "detail": "Governed by Section 96 of The State Acquisition and Tenancy Act, 1950. Under the 2006 statutory amendment, pre-emption right is restricted exclusively to co-sharer tenants by inheritance.",
                "type": "info",
            })
        elif property_type == "non_agricultural":
            applicable_statutes.append(cls.VERIFIED_STATUTES[1])  # NAT Act s.24
            findings.append({
                "factor": "Property Classification: Non-Agricultural Land",
                "detail": "Governed by Section 24 of The Non-Agricultural Tenancy Act, 1949. Co-sharer tenants (both by inheritance and purchase) can file for pre-emption when a share is transferred.",
                "type": "info",
            })
        else:
            missing_fact_indicators += 1
            findings.append({
                "factor": "Property Classification: Unverified / Mixed Record",
                "detail": "Classification (Agricultural vs. Non-Agricultural) dictates which statute applies (SAT Act s.96 vs NAT Act s.24). This must be verified from current revenue survey khatians and porchas.",
                "type": "warning",
            })

        # 2. Evaluate Co-Ownership Structure
        if co_ownership == "inheritance_undivided":
            review_indicators += 2
            findings.append({
                "factor": "Co-Ownership: Undivided Joint Heirs",
                "detail": "Co-sharers by inheritance possess statutory pre-emption rights under Section 96 SAT Act (for agricultural land) and Section 24 NAT Act (for non-agricultural land).",
                "type": "danger",
            })
        elif co_ownership == "purchase_undivided":
            if property_type == "non_agricultural":
                review_indicators += 2
                findings.append({
                    "factor": "Co-Ownership: Co-Sharers by Purchase",
                    "detail": "Under Section 24 of the Non-Agricultural Tenancy Act 1949, co-sharers by purchase retain the statutory right to pre-empt non-agricultural transfers.",
                    "type": "danger",
                })
            elif property_type == "agricultural":
                findings.append({
                    "factor": "Co-Ownership: Co-Sharers by Purchase in Agricultural Land",
                    "detail": "Following the 2006 amendment to Section 96 SAT Act, co-sharers by purchase cannot file statutory pre-emption for agricultural land, though personal law or general partition suits may still arise.",
                    "type": "warning",
                })
            else:
                review_indicators += 1
        elif co_ownership == "unsure" or not co_ownership:
            missing_fact_indicators += 2
            findings.append({
                "factor": "Co-Ownership: Unverified Co-Sharer Status",
                "detail": "The existence of co-sharers is the primary determinant of pre-emption rights. Title genealogy (heirship certificate) and survey records must be investigated.",
                "type": "warning",
            })
        elif co_ownership == "sole_ownership":
            findings.append({
                "factor": "Co-Ownership: Sole Independent Owner Reported",
                "detail": "No existing co-sharers identified in the tenancy holding. If verified by separate recorded khatian, statutory co-sharer pre-emption does not apply.",
                "type": "success",
            })

        # 3. Evaluate Partition Status
        if partition_status in ["unpartitioned_no_deed", "amicable_no_deed"]:
            review_indicators += 2
            findings.append({
                "factor": "Partition: No Registered Partition Deed",
                "detail": "Amicable or informal family possession without a registered partition deed or court partition decree leaves the property legally undivided under Section 44 of the Transfer of Property Act 1882.",
                "type": "danger",
            })
        elif partition_status == "unknown_partition" or not partition_status:
            missing_fact_indicators += 1
            findings.append({
                "factor": "Partition: Status Unverified",
                "detail": "Whether the seller's specific portion has been formally separated requires review of Sub-Registry search records and AC (Land) mutation books.",
                "type": "warning",
            })
        elif partition_status == "formal_registered_partition":
            findings.append({
                "factor": "Partition: Formal Registered Partition Recorded",
                "detail": "Recorded partition deed with demarcated schedule and independent mutated khatian eliminates joint-tenancy ambiguity.",
                "type": "success",
            })

        # 4. Evaluate Transfer Scope & Notice
        if transfer_scope == "undivided_share_stranger":
            review_indicators += 2
            findings.append({
                "factor": "Transfer: Undivided Share to Stranger / Third Party",
                "detail": "Selling an undivided fractional share to an outsider without co-sharer participation is the classic trigger for pre-emption applications in civil court.",
                "type": "danger",
            })
        elif transfer_scope == "to_existing_cosharer":
            findings.append({
                "factor": "Transfer: Sale Between Existing Co-Sharers",
                "detail": "Transfer to an existing co-sharer generally does not introduce an outside stranger, mitigating traditional pre-emption claims under standard legal tests.",
                "type": "info",
            })
        elif transfer_scope == "unsure":
            missing_fact_indicators += 1

        if notice_status in ["no_notice_served", "disputed_notice"]:
            review_indicators += 1
            findings.append({
                "factor": "Statutory Notice: Not Served / Active Dispute",
                "detail": "Failure to serve formal statutory notice (Section 89 SAT Act / Section 23 NAT Act) extends the limitation period for co-sharers to file for pre-emption from their date of knowledge.",
                "type": "danger",
            })
        elif notice_status == "unknown_notice":
            missing_fact_indicators += 1
            findings.append({
                "factor": "Statutory Notice: Verification Needed",
                "detail": "Sub-Registry registration records must be checked to ascertain if notice of transfer was executed and served on all recorded co-tenants.",
                "type": "warning",
            })

        # 5. Easements and Vicinage
        if easement_status in ["shared_easement", "contiguous_vicinage"]:
            applicable_statutes.append(cls.VERIFIED_STATUTES[2])  # Muslim Law
            findings.append({
                "factor": "Adjoining Property / Common Easement",
                "detail": "Where shared easements (Shafi-i-Khalit) or adjoining boundaries (Shafi-i-Jar) exist, personal Muslim law pre-emption rules may be invoked subject to strict legal demands (Talabs).",
                "type": "info",
            })

        # Determine Category Deterministically
        if missing_fact_indicators >= 2 or property_type == "unsure" or co_ownership == "unsure":
            category = cls.CATEGORY_FACTS_NEEDED
            badge_color = "warning"
            summary = (
                "Key factual determinants remain unknown or unverified. Pre-emption eligibility "
                "depends strictly on verifiable records (land classification, heirship genealogy, Sub-Registry deeds, and AC Land mutation). "
                "These factual prerequisites must be confirmed before assessing pre-emption risks."
            )
        elif review_indicators >= 2:
            category = cls.CATEGORY_REVIEW_REQUIRED
            badge_color = "danger"
            summary = (
                "Specific factual risk indicators identified. In Bangladesh land practice, "
                "undivided shares transferred without formal registered partition or statutory notice "
                "frequently trigger pre-emption proceedings by co-sharers. Formal legal scrutiny by an Advocate is essential."
            )
        else:
            category = cls.CATEGORY_NO_RISK_FOUND
            badge_color = "success"
            summary = (
                "Based solely on the responses provided (sole ownership, registered partition, and independent demarcated title), "
                "no standard pre-emption risk indicators were triggered. "
                "Note: This is an educational assessment based on input data and not a legal clearance of title."
            )

        # Deduplicate statutes
        seen_acts = set()
        dedup_statutes = []
        for s in applicable_statutes:
            if s["section"] not in seen_acts:
                seen_acts.add(s["section"])
                dedup_statutes.append(s)

        if not dedup_statutes:
            dedup_statutes = cls.VERIFIED_STATUTES[:2]

        recommended_steps = [
            "Obtain and inspect Certified True Copies of all Bia deeds and the current seller's deed from the Sub-Registry office.",
            "Verify the seller's Mutation Khatian and DCR at the AC (Land) office to confirm if the holding is separated or joint.",
            "If property is inherited, obtain an official Heirship (Genealogy) Certificate from the local Union Parishad or City Ward Councillor to identify all co-sharers.",
            "Verify whether a formal registered Partition Deed exists among all heirs/co-sharers under the Registration Act.",
            "Ensure statutory notice under Section 89 of SAT Act (for agricultural land) or Section 23 of NAT Act (for non-agricultural land) is properly processed upon transfer.",
            "Consult an enrolled Advocate of the Bangladesh Bar Council for an independent Written Legal Opinion on title and encumbrances.",
        ]

        return {
            "category": category,
            "badge_color": badge_color,
            "summary": summary,
            "findings": findings,
            "statutory_provisions": dedup_statutes,
            "recommended_steps": recommended_steps,
            "educational_disclaimer": (
                "EDUCATIONAL SIMULATION ONLY — BuyerGuard BD does not provide legal advice, "
                "guarantee ownership, or replace a licensed Advocate of the Bangladesh Bar Council. "
                "Statutory citations are provided for civic education and reference to the official Laws of Bangladesh repository."
            ),
        }
