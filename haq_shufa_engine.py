"""
haq_shufa_engine.py - Deterministic Legal Information Assessment Engine for Haq Shufa
BuyerGuard BD — Smart Land Pre-Purchase Verification Platform

Provides educational classification of pre-emption (Haq Shufa / Right of Pre-emption) risk indicators
under Bangladeshi statutory frameworks and Muslim personal law in both Bangla and English:
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
            "scope_bn": "কৃষিজমি ও রায়তি জোত",
            "applicability": "Right of pre-emption restricted exclusively to co-sharer tenants by inheritance following the 2006 statutory amendment (Act XXXIV of 2006). Co-sharers by purchase and contiguous holders are omitted.",
            "applicability_bn": "২০০৬ সালের সংশোধনীর পর কৃষিজমিতে অগ্রক্রয়াধিকার শুধুমাত্র ওয়ারিশসূত্রে সহ-শরিকদের জন্য সীমিত। খরিদসূত্রে শরিকদের বাদ দেওয়া হয়েছে।",
            "limitation": "Within 2 months of the service of notice under section 89, or within 2 months of the date of knowledge if notice was not served.",
            "limitation_bn": "ধারা ৮৯ অনুযায়ী নোটিশ জারির ২ মাসের মধ্যে, অথবা নোটিশ না পেলে হস্তান্তরের তথ্য জানার ২ মাসের মধ্যে।",
            "url": "http://bdlaws.minlaw.gov.bd/act-241/section-8698.html",
        },
        {
            "act": "The Non-Agricultural Tenancy Act, 1949",
            "section": "Section 24",
            "scope": "Non-agricultural land (residential, commercial, homestead tenancies)",
            "scope_bn": "অকৃষি জমি (বসতবাড়ি, আবাসিক ও বাণিজ্যিক প্লট)",
            "applicability": "Right of pre-emption exercisable by any co-sharer tenant (whether by purchase or inheritance) where a portion of the tenancy is transferred.",
            "applicability_bn": "অকৃষি প্রজাস্বত্বের অংশ হস্তান্তরের ক্ষেত্রে ওয়ারিশ বা খরিদ উভয় সূত্রের সহ-শরিক প্রজাই এই দাবি করতে পারেন।",
            "limitation": "Within 4 months of the service of notice under section 23; or if notice is not served, within applicable general limitation from date of knowledge.",
            "limitation_bn": "ধারা ২৩ অনুসারে নোটিশ জারির ৪ মাসের মধ্যে, অথবা অবগতির তারিখ হতে সাধারণ তামাদি মেয়াদের মধ্যে।",
            "url": "http://bdlaws.minlaw.gov.bd/act-231/section-8479.html",
        },
        {
            "act": "Muslim Personal Law (Haq Shufa / Right of Pre-emption)",
            "section": "General Muhammadan Law Doctrine",
            "scope": "Applies where statutory pre-emption is inapplicable or regarding contiguous lands and shared easements.",
            "scope_bn": "সংবিধিবদ্ধ আইনের অনুপস্থিতি অথবা সাধারণ রাস্তা ও সংলগ্ন সীমানার ক্ষেত্রে প্রযোজ্য।",
            "applicability": "Recognizes three classes of pre-emptors (Shufis): (1) Shafi-i-Sharik (co-sharers), (2) Shafi-i-Khalit (participators in appendages/easements), (3) Shafi-i-Jar (owners of adjoining property). Requires strict performance of three Demands (Talab-i-Mowasibat, Talab-i-Ishhad, and Talab-i-Tamlik).",
            "applicability_bn": "তিন শ্রেণির দাবিদার: (১) শাফি-ই-শারিক (সহ-শরিক), (২) শাফি-ই-খালিত (সুবিধাভোগী/চলাচলের পথের শরিক), এবং (৩) শাফি-ই-জার (সংলগ্ন প্রতিবেশী)। তিনটি আনুষ্ঠানিক তলব (দাবি) পালন আবশ্যক।",
            "limitation": "Immediate performance of Talab-i-Mowasibat upon hearing of sale, followed promptly by Talab-i-Ishhad before witnesses.",
            "limitation_bn": "বিক্রয়ের খবর শুনামাত্র অবিলম্বে তলব-ই-মোয়াছিবাত এবং পরবর্তীতে সাক্ষীদের উপস্থিতিতে তলব-ই-ইশহাদ সম্পাদন আবশ্যক।",
            "url": "http://bdlaws.minlaw.gov.bd/act-48/section-1601.html",
        },
    ]

    @classmethod
    def get_synthetic_scenarios(cls, lang: str = "bn") -> List[Dict[str, Any]]:
        """Return deterministic synthetic educational scenarios for interactive demonstrations."""
        is_bn = (lang != "en")
        return [
            {
                "id": "DEMO-SHUFA-01",
                "title": (
                    "দৃশ্যপট ১: অবিভক্ত কৃষিজ উত্তরাধিকার জমি"
                    if is_bn else
                    "Scenario 1: Undivided Agricultural Inheritance Land"
                ),
                "description": (
                    "বিক্রেতা পারিবারিক ওয়ারিশদের সাথে যৌথ মালিকানাধীন কৃষিজমির একটি অবিভক্ত অংশ বিক্রি করছেন, যেখানে কোনো নিবন্ধিত বণ্টননামা দলিল নেই এবং সহ-শরিকদের নোটিশ দেওয়া হয়নি।"
                    if is_bn else
                    "Seller is transferring an undivided share in inherited agricultural land to an outside party without a registered partition deed or statutory transfer notice."
                ),
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
                "title": (
                    "দৃশ্যপট ২: অসমাপ্ত তথ্য ও যাচাইবিহীন বণ্টন"
                    if is_bn else
                    "Scenario 2: Unverified Co-Ownership & Partition Facts"
                ),
                "description": (
                    "কাল্পনিক প্লটের দৃশ্যপট যেখানে জমির শ্রেণি, সহ-শরিকদের ওয়ারিশান সূত্র এবং বাটোয়ারা দলিলের রেকর্ড এখনও মাঠপর্যায়ে যাচাই করা হয়নি।"
                    if is_bn else
                    "A synthetic scenario where land classification, heirship genealogy, and partition deed execution have not been verified from registry records."
                ),
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
                "title": (
                    "দৃশ্যপট ৩: নিবন্ধিত বণ্টননামা ও পৃথক নামজারিভুক্ত জোত"
                    if is_bn else
                    "Scenario 3: Partitioned Sole Holding with Mutated Khatian"
                ),
                "description": (
                    "নিবন্ধিত বণ্টননামা দলিল, পৃথক স্বাধীন নামজারি খতিয়ান, নির্ধারিত সীমানা এবং একক মালিকানায় পৃথকীকৃত সম্পত্তি।"
                    if is_bn else
                    "An independent holding partitioned via registered deed, backed by a segregated mutation khatian, clear boundaries, and no common tenancy."
                ),
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
    def evaluate(cls, form_data: Dict[str, Any], lang: str = "bn") -> Dict[str, Any]:
        """
        Evaluate user or synthetic questionnaire responses and categorize pre-emption risk indicators.
        Returns one of three strictly informational categories in the selected language.
        """
        is_bn = (lang != "en")
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
                "factor": "জমির শ্রেণি: কৃষিজমি (Section 96 SAT Act)" if is_bn else "Property Classification: Agricultural Land (Section 96 SAT Act)",
                "factor_bn": "জমির শ্রেণি: কৃষিজমি (Section 96 SAT Act)",
                "factor_en": "Property Classification: Agricultural Land (Section 96 SAT Act)",
                "detail": (
                    "জমিটি The State Acquisition and Tenancy Act, 1950-এর Section 96 দ্বারা নিয়ন্ত্রিত। ২০০৬ সালের সংশোধনী অনুযায়ী শুধুমাত্র উত্তরাধিকার সূত্রে সহ-শরিকগণ অগ্রক্রয় (Haq Shufa) দাবি করতে পারেন।"
                    if is_bn else
                    "Governed by Section 96 of the SAT Act 1950. Following the 2006 statutory amendment, pre-emption is restricted exclusively to co-sharers by inheritance."
                ),
                "type": "info",
            })
        elif property_type == "non_agricultural":
            applicable_statutes.append(cls.VERIFIED_STATUTES[1])  # NAT Act s.24
            findings.append({
                "factor": "জমির শ্রেণি: অকৃষিজমি (Section 24 NAT Act)" if is_bn else "Property Classification: Non-Agricultural Land (Section 24 NAT Act)",
                "factor_bn": "জমির শ্রেণি: অকৃষিজমি (Section 24 NAT Act)",
                "factor_en": "Property Classification: Non-Agricultural Land (Section 24 NAT Act)",
                "detail": (
                    "জমিটি The Non-Agricultural Tenancy Act, 1949-এর Section 24 দ্বারা নিয়ন্ত্রিত। অংশ হস্তান্তরের ক্ষেত্রে উত্তরাধিকার বা খরিদ উভয় সূত্রের সহ-শরিকই অগ্রক্রয়ের আবেদন করতে পারেন।"
                    if is_bn else
                    "Governed by Section 24 of the NAT Act 1949. Pre-emption is exercisable by any co-sharer tenant (whether by purchase or inheritance) where a portion of the tenancy is transferred."
                ),
                "type": "info",
            })
        else:
            missing_fact_indicators += 1
            findings.append({
                "factor": "জমির শ্রেণি: অপ্রাপ্ত বা মিশ্র রেকর্ড" if is_bn else "Property Classification: Unverified / Mixed Record",
                "factor_bn": "জমির শ্রেণি: অপ্রাপ্ত বা মিশ্র রেকর্ড",
                "factor_en": "Property Classification: Unverified / Mixed Record",
                "detail": (
                    "জমির শ্রেণি (কৃষি বনাম অকৃষি) নির্ধারণ করে কোন আইন প্রযোজ্য হবে (SAT Act s.96 নাকি NAT Act s.24)। বর্তমান খতিয়ান ও পর্চা হতে এটি নিশ্চিত করা আবশ্যক।"
                    if is_bn else
                    "Property classification determines whether Section 96 SAT Act or Section 24 NAT Act governs. Must be established from current khatian and survey records."
                ),
                "type": "warning",
            })

        # 2. Evaluate Co-Ownership Structure
        if co_ownership == "inheritance_undivided":
            review_indicators += 2
            findings.append({
                "factor": "যৌথ মালিকানা: অবিভক্ত ওয়ারিশান সূত্র" if is_bn else "Co-Ownership: Undivided Co-Sharers by Inheritance",
                "factor_bn": "যৌথ মালিকানা: অবিভক্ত ওয়ারিশান সূত্র",
                "factor_en": "Co-Ownership: Undivided Co-Sharers by Inheritance",
                "detail": (
                    "উত্তরাধিকার সূত্রে সহ-শরিকদের কৃষিজমিতে Section 96 SAT Act এবং অকৃষিজমিতে Section 24 NAT Act অনুযায়ী অগ্রক্রয়ের সংবিধিবদ্ধ আইনি অধিকার রয়েছে।"
                    if is_bn else
                    "Co-sharers by inheritance hold statutory pre-emption rights under Section 96 SAT Act (agricultural) and Section 24 NAT Act (non-agricultural)."
                ),
                "type": "danger",
            })
        elif co_ownership == "purchase_undivided":
            if property_type == "non_agricultural":
                review_indicators += 2
                findings.append({
                    "factor": "যৌথ মালিকানা: খরিদ সূত্রে সহ-শরিক" if is_bn else "Co-Ownership: Undivided Co-Sharers by Purchase",
                    "factor_bn": "যৌথ মালিকানা: খরিদ সূত্রে সহ-শরিক",
                    "factor_en": "Co-Ownership: Undivided Co-Sharers by Purchase",
                    "detail": (
                        "Non-Agricultural Tenancy Act 1949-এর Section 24 অনুযায়ী খরিদ সূত্রে সহ-শরিকদেরও অগ্রক্রয় করার অধিকার বলবৎ রয়েছে।"
                        if is_bn else
                        "Under Section 24 NAT Act, co-sharers by purchase in non-agricultural tenancies retain statutory pre-emption remedies."
                    ),
                    "type": "danger",
                })
            elif property_type == "agricultural":
                findings.append({
                    "factor": "যৌথ মালিকানা: কৃষিজমিতে খরিদ সূত্রে সহ-শরিক" if is_bn else "Co-Ownership: Co-Sharers by Purchase in Agricultural Land",
                    "factor_bn": "যৌথ মালিকানা: কৃষিজমিতে খরিদ সূত্রে সহ-শরিক",
                    "factor_en": "Co-Ownership: Co-Sharers by Purchase in Agricultural Land",
                    "detail": (
                        "Section 96 SAT Act-এর ২০০৬ সালের সংশোধনীর পর খরিদ সূত্রে সহ-শরিকরা সংবিধিবদ্ধ অগ্রক্রয় দাবি করতে পারেন না, তবে সাধারণ বণ্টন মামলা প্রযোজ্য হতে পারে।"
                        if is_bn else
                        "Following the 2006 SAT Act amendment, co-sharers by purchase cannot claim statutory agricultural pre-emption under Section 96."
                    ),
                    "type": "warning",
                })
            else:
                review_indicators += 1
        elif co_ownership == "unsure" or not co_ownership:
            missing_fact_indicators += 2
            findings.append({
                "factor": "যৌথ মালিকানা: সহ-শরিকের তথ্য অনিশ্চিত" if is_bn else "Co-Ownership: Co-Sharer Genealogy Unverified",
                "factor_bn": "যৌথ মালিকানা: সহ-শরিকের তথ্য অনিশ্চিত",
                "factor_en": "Co-Ownership: Co-Sharer Genealogy Unverified",
                "detail": (
                    "সহ-শরিকের অস্তিত্বই হক শুফা বা অগ্রক্রয় অধিকারের মূল ভিত্তি। ওয়ারিশান সনদ এবং বায়া দলিলের মাধ্যমে সহ-শরিকদের তালিকা যাচাই করা অপরিহার্য।"
                    if is_bn else
                    "Co-ownership origin is the factual foundation of pre-emption. Verified heirship certificates and title deeds are necessary to establish co-sharer status."
                ),
                "type": "warning",
            })
        elif co_ownership == "sole_ownership":
            findings.append({
                "factor": "যৌথ মালিকানা: একক স্বতন্ত্র মালিকানা" if is_bn else "Co-Ownership: Independent Sole Ownership",
                "factor_bn": "যৌথ মালিকানা: একক স্বতন্ত্র মালিকানা",
                "factor_en": "Co-Ownership: Independent Sole Ownership",
                "detail": (
                    "জোতে কোনো সহ-শরিক নেই বলে তথ্য পাওয়া গেছে। পৃথক খতিয়ান দ্বারা সমর্থিত হলে সংবিধিবদ্ধ সহ-শরিকি হক শুফা প্রযোজ্য হয় না।"
                    if is_bn else
                    "Independent sole ownership indicated. When backed by segregated mutation records, statutory co-sharer pre-emption does not apply."
                ),
                "type": "success",
            })

        # 3. Evaluate Partition Status
        if partition_status in ["unpartitioned_no_deed", "amicable_no_deed"]:
            review_indicators += 2
            findings.append({
                "factor": "বাটোয়ারা: নিবন্ধিত বণ্টননামা দলিল নেই" if is_bn else "Partition Status: No Registered Partition Deed",
                "factor_bn": "বাটোয়ারা: নিবন্ধিত বণ্টননামা দলিল নেই",
                "factor_en": "Partition Status: No Registered Partition Deed",
                "detail": (
                    "নিবন্ধিত বাটোয়ারা দলিল বা আদালতের ডিক্রি ছাড়া শুধুমাত্র মৌখিক বা আপস বণ্টন Transfer of Property Act 1882-এর Section 44 অনুযায়ী সম্পত্তিকে আইনত অবিভক্ত রাখে।"
                    if is_bn else
                    "Without a registered partition deed or court decree, informal oral or amicable divisions leave the holding legally undivided under Section 44 of the Transfer of Property Act 1882."
                ),
                "type": "danger",
            })
        elif partition_status == "unknown_partition" or not partition_status:
            missing_fact_indicators += 1
            findings.append({
                "factor": "বাটোয়ারা: বণ্টননামার অবস্থা যাচাইবিহীন" if is_bn else "Partition Status: Demarcation & Partition Unverified",
                "factor_bn": "বাটোয়ারা: বণ্টননামার অবস্থা যাচাইবিহীন",
                "factor_en": "Partition Status: Demarcation & Partition Unverified",
                "detail": (
                    "বিক্রেতার অংশটি আনুষ্ঠানিকভাবে পৃথক হয়েছে কি না তা নিশ্চিত করতে সাব-রেজিস্ট্রি অফিসের তল্লাশি এবং এসি ল্যান্ড অফিসের বালাম বই পর্যালোচনা প্রয়োজন।"
                    if is_bn else
                    "Sub-Registry volume searches and AC (Land) records must be reviewed to verify whether the seller's share has been formally demarcated."
                ),
                "type": "warning",
            })
        elif partition_status == "formal_registered_partition":
            findings.append({
                "factor": "বাটোয়ারা: নিবন্ধিত বাটোয়ারা দলিল বিদ্যমান" if is_bn else "Partition Status: Formal Registered Partition Deed Exists",
                "factor_bn": "বাটোয়ারা: নিবন্ধিত বাটোয়ারা দলিল বিদ্যমান",
                "factor_en": "Partition Status: Formal Registered Partition Deed Exists",
                "detail": (
                    "চিহ্নিত তফসিল ও স্বাধীন নামজারি খতিয়ানসহ নিবন্ধিত বণ্টননামা দলিল যৌথ মালিকানার জটিলতা দূর করে।"
                    if is_bn else
                    "A registered partition deed accompanied by an independent mutation khatian segregates boundaries and extinguishes undivided tenancy."
                ),
                "type": "success",
            })

        # 4. Evaluate Transfer Scope & Notice
        if transfer_scope == "undivided_share_stranger":
            review_indicators += 2
            findings.append({
                "factor": "হস্তান্তর পরিধি: বহিরাগত ক্রেতার নিকট অবিভক্ত অংশ বিক্রয়" if is_bn else "Transfer Scope: Undivided Share to Outside Stranger",
                "factor_bn": "হস্তান্তর পরিধি: বহিরাগত ক্রেতার নিকট অবিভক্ত অংশ বিক্রয়",
                "factor_en": "Transfer Scope: Undivided Share to Outside Stranger",
                "detail": (
                    "সহ-শরিকদের সম্মতি ছাড়া কোনো বহিরাগত ব্যক্তির কাছে অবিভক্ত অংশ বিক্রি করা দেওয়ানি আদালতে হক শুফা মামলা দায়েরের প্রধান কারণ।"
                    if is_bn else
                    "Conveying an undivided share to a third-party purchaser without co-sharer waivers frequently triggers pre-emption civil litigation."
                ),
                "type": "danger",
            })
        elif transfer_scope == "to_existing_cosharer":
            findings.append({
                "factor": "হস্তান্তর পরিধি: বিদ্যমান সহ-শরিকের নিকট বিক্রয়" if is_bn else "Transfer Scope: Conveyance to Existing Co-Sharer",
                "factor_bn": "হস্তান্তর পরিধি: বিদ্যমান সহ-শরিকের নিকট বিক্রয়",
                "factor_en": "Transfer Scope: Conveyance to Existing Co-Sharer",
                "detail": (
                    "বিদ্যমান সহ-শরিকের কাছে হস্তান্তর বহিরাগত প্রবেশের কারণ ঘটায় না বিধায় সাধারণ আইনি মূল্যায়নে অগ্রক্রয়ের ঝুঁকি প্রশমিত হয়।"
                    if is_bn else
                    "Transfers between existing co-sharers do not introduce outside parties, reducing statutory pre-emption vulnerability."
                ),
                "type": "info",
            })
        elif transfer_scope == "unsure":
            missing_fact_indicators += 1

        if notice_status in ["no_notice_served", "disputed_notice"]:
            review_indicators += 1
            findings.append({
                "factor": "সংবিধিবদ্ধ নোটিশ: নোটিশ জারি হয়নি বা বিরোধমান" if is_bn else "Statutory Notice: Notice Not Served or Under Dispute",
                "factor_bn": "সংবিধিবদ্ধ নোটিশ: নোটিশ জারি হয়নি বা বিরোধমান",
                "factor_en": "Statutory Notice: Notice Not Served or Under Dispute",
                "detail": (
                    "Section 89 SAT Act বা Section 23 NAT Act অনুযায়ী আনুষ্ঠানিক নোটিশ জারি না হলে সহ-শরিকদের জন্য অবগতির তারিখ হতে মামলা দায়েরের তামাদি গণনা শুরু হয়।"
                    if is_bn else
                    "Absence of statutory notice under Section 89 SAT Act or Section 23 NAT Act allows co-sharers to compute the limitation period from the date of discovery."
                ),
                "type": "danger",
            })
        elif notice_status == "unknown_notice":
            missing_fact_indicators += 1
            findings.append({
                "factor": "সংবিধিবদ্ধ নোটিশ: নোটিশ জারির তথ্য অজানা" if is_bn else "Statutory Notice: Sub-Registry Notice Status Unverified",
                "factor_bn": "সংবিধিবদ্ধ নোটিশ: নোটিশ জারির তথ্য অজানা",
                "factor_en": "Statutory Notice: Sub-Registry Notice Status Unverified",
                "detail": (
                    "সাব-রেজিস্ট্রি অফিসে রেকর্ড পরীক্ষা করে দেখতে হবে যে হস্তান্তর নোটিশ যথাযথভাবে জারি ও তামিল হয়েছে কি না।"
                    if is_bn else
                    "Sub-Registry records must be examined to verify whether formal statutory transfer notices were served to recorded co-sharers."
                ),
                "type": "warning",
            })

        # 5. Easements and Vicinage
        if easement_status in ["shared_easement", "contiguous_vicinage"]:
            applicable_statutes.append(cls.VERIFIED_STATUTES[2])  # Muslim Law
            findings.append({
                "factor": "সংলগ্ন জমি বা সাধারণ রাস্তা/পানির পথ" if is_bn else "Adjoining Land / Shared Access & Easement",
                "factor_bn": "সংলগ্ন জমি বা সাধারণ রাস্তা/পানির পথ",
                "factor_en": "Adjoining Land / Shared Access & Easement",
                "detail": (
                    "সাধারণ রাস্তা (Shafi-i-Khalit) বা সংলগ্ন সীমানা (Shafi-i-Jar) থাকলে মুসলিম ব্যক্তিগত আইন (Muslim Personal Law) অনুযায়ী তলবসমূহ (Talab-i-Mowasibat, Talab-i-Ishhad) পরিপালন সাপেক্ষে দাবি উত্থাপিত হতে পারে।"
                    if is_bn else
                    "Shared easements (Shafi-i-Khalit) or adjoining boundaries (Shafi-i-Jar) may support claims under Muslim Personal Law if the formal demands are fulfilled."
                ),
                "type": "info",
            })

        # Determine Category Deterministically
        if missing_fact_indicators >= 2 or property_type == "unsure" or co_ownership == "unsure":
            category = cls.CATEGORY_FACTS_NEEDED
            category_bn = "প্রাসঙ্গিক তথ্য যাচাই প্রয়োজন"
            category_en = "Relevant Facts Need Verification"
            badge_color = "warning"
            summary_en = (
                "Key factual determinants remain unknown or unverified. Pre-emption eligibility "
                "depends strictly on verifiable records (land classification, heirship genealogy, Sub-Registry deeds, and AC Land mutation). "
                "These factual prerequisites must be confirmed before assessing pre-emption risks."
            )
            summary_bn = (
                "মূল তথ্যাবলি এখনও অজানা বা যাচাইবিহীন রয়েছে। হক শুফার ঝুঁকি জমির শ্রেণি, ওয়ারিশান ধারাবাহিকতা, "
                "সাব-রেজিস্ট্রি বালাম বই এবং নামজারি রেকর্ডের ওপর পুরোপুরি নির্ভরশীল। ঝুঁকি মূল্যায়নের আগে এই তথ্যগুলো যাচাই করা আবশ্যক।"
            )
        elif review_indicators >= 2:
            category = cls.CATEGORY_REVIEW_REQUIRED
            category_bn = "অতিরিক্ত আইনি পর্যালোচনা আবশ্যক"
            category_en = "Further Legal Review Recommended"
            badge_color = "danger"
            summary_en = (
                "Specific factual risk indicators identified. In Bangladesh land practice, "
                "undivided shares transferred without formal registered partition or statutory notice "
                "frequently trigger pre-emption proceedings by co-sharers. Formal legal scrutiny by an Advocate is essential."
            )
            summary_bn = (
                "অগ্রক্রয় ঝুঁকির সুনির্দিষ্ট কারণ সনাক্ত হয়েছে। বাংলাদেশে নিবন্ধিত বণ্টননামা ও সংবিধিবদ্ধ নোটিশ ছাড়া "
                "যৌথ জোতের অবিভক্ত অংশ বিক্রি করলে সহ-শরিকদের দ্বারা হক শুফা মামলা দায়েরের প্রবল ঝুঁকি থাকে। অভিজ্ঞ আইনজীবীর মতামত নেওয়া জরুরি।"
            )
        else:
            category = cls.CATEGORY_NO_RISK_FOUND
            category_bn = "প্রদত্ত তথ্যে কোনো ঝুঁকির নির্দেশক পাওয়া যায়নি"
            category_en = "No Pre-Emption Risk Indicators Detected in Demo Data"
            badge_color = "success"
            summary_en = (
                "Based solely on the responses provided (sole ownership, registered partition, and independent demarcated title), "
                "no standard pre-emption risk indicators were triggered. "
                "Note: This is an educational assessment based on input data and not a legal clearance of title."
            )
            summary_bn = (
                "প্রদত্ত তথ্যের ভিত্তিতে (একক মালিকানা, নিবন্ধিত বণ্টননামা ও স্বাধীন চিহ্নিত সীমানা) কোনো সাধারণ হক শুফা ঝুঁকির নির্দেশক পাওয়া যায়নি। "
                "মনে রাখবেন: এটি প্রদত্ত তথ্যের ওপর ভিত্তি করে একটি শিক্ষামূলক মূল্যায়ন, আইনি মালিকানার চূড়ান্ত নিশ্চয়তা নয়।"
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

        recommended_steps_bn = [
            "সাব-রেজিস্ট্রি অফিস থেকে বিক্রেতার দলিল এবং পূর্ববর্তী সকল বায়া দলিলের সার্টিফাইড নকল (Nokol) তুলে বালাম বই তল্লাশি করুন।",
            "সহকারী কমিশনার (ভূমি) / এসি ল্যান্ড অফিসে বিক্রেতার নামজারি খতিয়ান ও ডিসিআর যাচাই করে নিশ্চিত হোন জোতটি পৃথক কি না।",
            "উত্তরাধিকার সূত্রে প্রাপ্ত সম্পত্তি হলে সংশ্লিষ্ট ইউনিয়ন পরিষদ বা সিটি কর্পোরেশন কাউন্সিলর অফিস থেকে ওয়ারিশান সনদ সংগ্রহ করে সকল সহ-শরিকদের শনাক্ত করুন।",
            "রেজিস্ট্রেশন আইনের অধীন সকল সহ-শরিকদের মধ্যে কোনো নিবন্ধিত বণ্টননামা (Partition Deed) দলিল সম্পাদিত হয়েছে কি না তা যাচাই করুন।",
            "হস্তান্তরের সময় কৃষিজমির ক্ষেত্রে Section 89 SAT Act এবং অকৃষিজমির ক্ষেত্রে Section 23 NAT Act অনুযায়ী সংবিধিবদ্ধ নোটিশ প্রদান নিশ্চিত করুন।",
            "বায়নাপত্র বা দলিল সম্পাদনের পূর্বে বাংলাদেশ বার কাউন্সিলের সনদপ্রাপ্ত একজন অ্যাডভোকেটের নিকট থেকে লিখিত আইনি মতামত (Title Opinion) গ্রহণ করুন।",
        ]

        recommended_steps_en = [
            "Conduct an exhaustive Volume (Balam) book search at the Sub-Registry office and obtain certified copies (Nokol) of all preceding title deeds.",
            "Verify the seller's Mutation Khatian (e-Namjari) and DCR receipt at the AC (Land) office to confirm a segregated holding.",
            "Obtain an official Heirship Certificate from the Union Parishad or City Corporation Ward to identify all legal male and female heirs.",
            "Examine whether a formal partition deed (Aposh Bontonnama) was registered under the Registration Act among all co-heirs.",
            "Confirm that statutory transfer notices under Section 89 SAT Act or Section 23 NAT Act were formally served to recorded co-sharers.",
            "Obtain a written legal title opinion from an enrolled Advocate of the Bangladesh Bar Council prior to executing the conveyance deed.",
        ]

        summary_display = summary_bn if is_bn else summary_en
        category_display = category_bn if is_bn else category_en

        return {
            "category": category,
            "category_bn": category_bn,
            "category_en": category_en,
            "category_display": category_display,
            "badge_color": badge_color,
            "summary": summary_en,
            "summary_bn": summary_bn,
            "summary_display": summary_display,
            "findings": findings,
            "statutory_provisions": dedup_statutes,
            "recommended_steps": recommended_steps_bn if is_bn else recommended_steps_en,
            "recommended_steps_bn": recommended_steps_bn,
            "recommended_steps_en": recommended_steps_en,
            "educational_disclaimer": (
                "শিক্ষামূলক সিমুলেশন — BuyerGuard BD কোনো আইনি পরামর্শ বা মালিকানার নিশ্চয়তা প্রদান করে না এবং বাংলাদেশ বার কাউন্সিলের অনুমোদিত আইনজীবীর বিকল্প নয়। "
                "Statutory citations are provided for civic education and reference to the official Laws of Bangladesh repository."
                if is_bn else
                "Educational Simulation — BuyerGuard BD does not provide formal legal opinions or guarantee sound ownership. It is not a substitute for an enrolled Advocate. "
                "Statutory citations are provided for civic education and reference to the official Laws of Bangladesh repository."
            ),
        }
