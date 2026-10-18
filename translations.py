"""
translations.py - Comprehensive Bilingual (Bangla & English) Localization Dictionary
BuyerGuard BD — Smart Land Pre-Purchase Verification Platform

Provides complete text strings for all user-facing elements across the application,
supporting instant one-click switching with Bangla ('bn') as the default.
"""

from typing import Dict, Any, Optional

TRANSLATIONS: Dict[str, Dict[str, str]] = {
    # -------------------------------------------------------------
    # General / Branding / Navigation
    # -------------------------------------------------------------
    "app_name": {
        "bn": "BuyerGuard BD",
        "en": "BuyerGuard BD",
    },
    "app_tagline": {
        "bn": "জমি কেনার আগেই যাচাই করুন — স্মার্ট ল্যান্ড প্রি-পারচেজ ভেরিফিকেশন প্ল্যাটফর্ম",
        "en": "Check Before You Buy — Smart Land Pre-Purchase Verification Platform",
    },
    "tagline_short": {
        "bn": "জমি কেনার আগেই যাচাই করুন",
        "en": "Check Before You Buy",
    },
    "demo_badge": {
        "bn": "শিক্ষামূলক ডেমো",
        "en": "DEMO ONLY",
    },
    "banner_text": {
        "bn": "সতর্কবার্তা: এটি ল্যান্ডটেক ২০২৬-এর জন্য কাল্পনিক ডেটা দ্বারা প্রস্তুতকৃত একটি শিক্ষামূলক প্রোটোটাইপ। এটি কোনো সরকারি লাইভ ডাটাবেজের সাথে যুক্ত নয়।",
        "en": "Notice: Educational prototype using synthetic demonstration data for LandTech 2026. Not connected to live government databases.",
    },
    "nav_home": {
        "bn": "হোম অনুসন্ধান",
        "en": "Home Search",
    },
    "nav_dashboard": {
        "bn": "রেকর্ড ড্যাশবোর্ড",
        "en": "Records Dashboard",
    },
    "nav_checklist": {
        "bn": "নাগরিক চেকলিস্ট",
        "en": "Citizen Checklist",
    },
    "nav_haq_shufa": {
        "bn": "হক শুফা আইনি নির্দেশিকা",
        "en": "Haq Shufa Legal Guide",
    },
    "nav_search_placeholder": {
        "bn": "প্লট / দলিল / খতিয়ান নম্বর...",
        "en": "Plot / Deed / Khatian no...",
    },
    "nav_search_aria": {
        "bn": "প্লট অনুসন্ধান করুন",
        "en": "Search plot records",
    },
    "nav_search_btn_title": {
        "bn": "অনুসন্ধান",
        "en": "Search",
    },
    "footer_tagline": {
        "bn": "বাংলাদেশে জমি কেনার পূর্বে সাধারণ নাগরিক ও ক্রেতাদের জন্য ব্যাখ্যাযোগ্য, তথ্যভিত্তিক ঝুঁকি বিশ্লেষণ ও আইনি সচেতনতামূলক প্ল্যাটফর্ম।",
        "en": "Explainable, fact-based risk analysis and legal awareness platform for citizens and prospective land buyers in Bangladesh.",
    },
    "footer_quick_links": {
        "bn": "দ্রুত নেভিগেশন",
        "en": "Quick Navigation",
    },
    "footer_health_check": {
        "bn": "সিস্টেম হেলথ চেক",
        "en": "System Health Check",
    },
    "footer_disclaimer_title": {
        "bn": "দায়মুক্তি ও সতর্কবার্তা",
        "en": "Disclaimer & Notice",
    },
    "footer_disclaimer_text": {
        "bn": "এই প্ল্যাটফর্মটি একটি শিক্ষামূলক সিমুলেশন। এটি ভূমি রেকর্ড ও জরিপ অধিদপ্তর (DGLRS), সাব-রেজিস্ট্রি পোর্টাল বা কোনো সরকারি লাইভ ডেটাবেজের সাথে সংযুক্ত নয়। যেকোনো জমি লেনদেনের পূর্বে অবশ্যই মূল বালাম বই তল্লাশি ও সার্টিফাইড রেকর্ড যাচাই করুন এবং পেশাদার আইনজীবীর পরামর্শ নিন।",
        "en": "This platform is an educational simulation. It is not connected to the Directorate General of Land Records and Surveys (DGLRS), Sub-Registry portals, or any live government system. Always perform physical Volume (Balam) book searches and consult an enrolled advocate prior to any transaction.",
    },
    "footer_copyright": {
        "bn": "ল্যান্ডটেক ইনোভেশন হ্যাকাথন ২০২৬ &bull; ড্যাফোডিল ইন্টারন্যাশনাল ইউনিভার্সিটি (DIU), বাংলাদেশ। সর্বস্বত্ব সংরক্ষিত।",
        "en": "LandTech Innovation Hackathon 2026 &bull; Daffodil International University (DIU), Bangladesh. All rights reserved.",
    },

    # -------------------------------------------------------------
    # Home Page (index.html)
    # -------------------------------------------------------------
    "hero_title": {
        "bn": "জমি কেনার আগেই যাচাই করুন।",
        "en": "Check Before You Buy Land.",
    },
    "hero_subtitle": {
        "bn": "বাংলাদেশে জমি ক্রয়ের পূর্বে দলিলের সঠিকতা, নামজারি খতিয়ান, উত্তরাধিকার বা বাটোয়ারা অবস্থা এবং কাল্পনিক দ্বৈত-বিক্রয় (Double-Selling) সংঘাত যাচাইয়ে নাগরিকদের জন্য একটি সহজে বোধগম্য ও ব্যাখ্যামূলক প্রোটোটাইপ।",
        "en": "An explainable, citizen-facing prototype to verify deed consistency, mutation khatians, partition status, and simulated double-selling conflicts before entering property agreements in Bangladesh.",
    },
    "hero_search_label": {
        "bn": "প্লট নম্বর, খতিয়ান, দলিল নম্বর বা মৌজা কোড দিয়ে অনুসন্ধান করুন:",
        "en": "Search by Plot Number, Khatian, Deed Reference, or Mouza Code:",
    },
    "hero_search_placeholder": {
        "bn": "যেমন: PLOT-1001, KH-DEMO-1004, DEED-DEMO-1002, বা DEMO-MOUZA-01",
        "en": "e.g., PLOT-1001, KH-DEMO-1004, DEED-DEMO-1002, or DEMO-MOUZA-01",
    },
    "hero_search_btn": {
        "bn": "রেকর্ড যাচাই করুন",
        "en": "Verify Records",
    },
    "hero_demo_cases_label": {
        "bn": "ডেমো কেস পরীক্ষা করুন:",
        "en": "Try Demo Cases:",
    },
    "hero_pill_clean": {
        "bn": "PLOT-1001 (ডেমোতে কোনো ঝুঁকি নেই / No Flags in Demo)",
        "en": "PLOT-1001 (No Flags in Demo Data)",
    },
    "hero_pill_dup_sale": {
        "bn": "PLOT-1004 (দ্বৈত-বিক্রয়ের বিরোধ / Double Sale)",
        "en": "PLOT-1004 (Double-Selling Conflict)",
    },
    "hero_pill_missing_mutation": {
        "bn": "PLOT-1002 (নামজারি অনুপস্থিত / Missing Mutation)",
        "en": "PLOT-1002 (Missing Mutation Khatian)",
    },
    "hero_pill_mismatch": {
        "bn": "PLOT-1005 (দলিল গরমিল / Reference Mismatch)",
        "en": "PLOT-1005 (Deed Reference Mismatch)",
    },
    "why_verify_title": {
        "bn": "বাংলাদেশে জমি কেনার পূর্বে কেন যাচাইকরণ অপরিহার্য?",
        "en": "Why Pre-Purchase Land Verification is Critical in Bangladesh",
    },
    "why_verify_subtitle": {
        "bn": "প্রশাসনিক বিভাজন ও তথ্যের বিচ্ছিন্নতার কারণে জমি ক্রেতারা যেসকল সাধারণ ঝুঁকির মুখে পড়েন:",
        "en": "Common vulnerabilities buyers face due to siloed records between registration and land offices:",
    },
    "card_dglrs_title": {
        "bn": "নিবন্ধন বনাম ভূমি অফিস সমন্বয়হীনতা",
        "en": "Registration vs. Land Office Silo",
    },
    "card_dglrs_desc": {
        "bn": "সাব-রেজিস্ট্রি অফিসে দলিল নিবন্ধন হয় কিন্তু নামজারি খতিয়ান রক্ষণাবেক্ষণ করে সহকারী কমিশনার (ভূমি) অফিস। রিয়েল-টাইম ডাটা সিঙ্ক না থাকায় একই জমি একাধিকবার বিক্রয়ের সুযোগ তৈরি হয়।",
        "en": "Deeds are registered at the Sub-Registry while mutation records are managed by the AC (Land) office. Lack of synchronization creates vulnerabilities to parallel conveyance claims.",
    },
    "card_chain_title": {
        "bn": "বায়া দলিলের ধারাবাহিকতা",
        "en": "Chain of Title (Bia Deeds)",
    },
    "card_chain_desc": {
        "bn": "সিএস, এসএ, আরএস থেকে বর্তমান জরিপ পর্যন্ত মালিকানার নিরবচ্ছিন্ন বায়া দলিল এবং ওয়ারিশদের রেজিস্ট্রিকৃত বাটোয়ারানামা না থাকলে ভবিষ্যতে স্বত্ব নিয়ে মামলা মোকদ্দমা হতে পারে।",
        "en": "Unbroken historical title deeds across CS, SA, RS, and BS surveys, along with registered partition deeds among co-heirs, are required to establish sound ownership.",
    },
    "card_haq_shufa_title": {
        "bn": "হক শুফা বা অগ্রক্রয়াধিকার",
        "en": "Haq Shufa / Pre-emption Rights",
    },
    "card_haq_shufa_desc": {
        "bn": "স্টেট একুইজিশন অ্যান্ড প্রজাস্বত্ব আইনের ৯৬ ধারা বা অকৃষি প্রজাস্বত্ব আইনের ২৪ ধারা অনুযায়ী ওয়ারিশি সহ-শরিকদের অগ্রাধিকার না দিয়ে ক্রয় করলে পরবর্তীতে দেওয়ানি মোকদ্দমা হতে পারে।",
        "en": "Purchasing undivided shares without statutory notice under Section 96 SAT Act or Section 24 NAT Act exposes purchasers to legal pre-emption claims by co-sharers.",
    },
    "rules_overview_title": {
        "bn": "ব্যাখ্যামূলক রুল ইঞ্জিন যেভাবে ঝুঁকি চিহ্নিত করে",
        "en": "How the Explainable Risk Engine Evaluates Records",
    },
    "rules_overview_subtitle": {
        "bn": "কোনো ব্ল্যাক-বক্স মডেল বা অনুমান নয়; প্রতিটি সিদ্ধান্ত স্বচ্ছ, উন্মুক্ত ও যাচাইযোগ্য যুক্তির ওপর প্রতিষ্ঠিত।",
        "en": "No black-box models or guesses; every evaluation follows transparent, verifiable deterministic logic.",
    },

    # -------------------------------------------------------------
    # Dashboard (dashboard.html)
    # -------------------------------------------------------------
    "dash_title": {
        "bn": "কাল্পনিক ভূমি রেকর্ড ড্যাশবোর্ড",
        "en": "Synthetic Land Records Dashboard",
    },
    "dash_subtitle": {
        "bn": "SQLite ডেটাবেজ এবং ব্যাখ্যামূলক রুল ইঞ্জিন থেকে সরাসরি পরিগণিত পরিসংখ্যান।",
        "en": "Real-time statistics derived directly from SQLite records and the explainable rule engine.",
    },
    "dash_btn_checklist": {
        "bn": "প্রাক-ক্রয় চেকলিস্ট",
        "en": "Pre-Purchase Checklist",
    },
    "dash_btn_search": {
        "bn": "নতুন অনুসন্ধান",
        "en": "New Search",
    },
    "dash_stat_total": {
        "bn": "মোট ডেমো প্লট",
        "en": "Total Demo Plots",
    },
    "dash_stat_review": {
        "bn": "পর্যালোচনা প্রয়োজন",
        "en": "Review Recommended",
    },
    "dash_stat_conflict": {
        "bn": "দ্বৈত-বিক্রয় বিরোধ",
        "en": "Duplicate Sale Conflicts",
    },
    "dash_stat_incomplete": {
        "bn": "অসম্পূর্ণ রেকর্ড",
        "en": "Incomplete Records",
    },
    "dash_filter_all": {
        "bn": "সকল ডেমো প্লট",
        "en": "All Demo Plots",
    },
    "dash_filter_review": {
        "bn": "পর্যালোচনা প্রয়োজন",
        "en": "Review Recommended",
    },
    "dash_filter_conflict": {
        "bn": "দ্বৈত-বিক্রয় বিরোধ",
        "en": "Duplicate Sale Conflicts",
    },
    "dash_filter_incomplete": {
        "bn": "অসম্পূর্ণ রেকর্ড",
        "en": "Incomplete Records",
    },
    "dash_quick_search_placeholder": {
        "bn": "আইডি, মৌজা, খতিয়ান বা দলিল দিয়ে ফিল্টার করুন...",
        "en": "Filter by Plot ID, Mouza, Khatian, or Deed...",
    },
    "dash_th_plot_id": {
        "bn": "প্লট আইডি",
        "en": "Plot ID",
    },
    "dash_th_area": {
        "bn": "প্রশাসনিক এলাকা",
        "en": "Administrative Area",
    },
    "dash_th_mouza": {
        "bn": "মৌজা কোড",
        "en": "Mouza Code",
    },
    "dash_th_deed": {
        "bn": "মূল দলিল রেফারেন্স",
        "en": "Deed Reference",
    },
    "dash_th_khatian": {
        "bn": "খতিয়ান নম্বর",
        "en": "Khatian Reference",
    },
    "dash_th_mutation": {
        "bn": "নামজারি অবস্থা",
        "en": "Mutation Status",
    },
    "dash_th_completeness": {
        "bn": "সম্পূর্ণতা",
        "en": "Completeness",
    },
    "dash_th_status": {
        "bn": "সার্বিক মূল্যায়ন",
        "en": "Overall Status",
    },
    "dash_th_actions": {
        "bn": "পদক্ষেপ",
        "en": "Action",
    },
    "dash_btn_view": {
        "bn": "বিস্তারিত দেখুন",
        "en": "View Details",
    },
    "dash_empty_table": {
        "bn": "এই ফিল্টারে কোনো প্লট রেকর্ড পাওয়া যায়নি।",
        "en": "No demonstration records match this filter.",
    },

    # -------------------------------------------------------------
    # Search Results (search_results.html)
    # -------------------------------------------------------------
    "search_results_title": {
        "bn": "অনুসন্ধানের ফলাফল",
        "en": "Search Results",
    },
    "search_results_query_for": {
        "bn": "এর জন্য অনুসন্ধান ফলাফল:",
        "en": "Query:",
    },
    "search_results_found": {
        "bn": "টি রেকর্ড সনাক্ত করা হয়েছে।",
        "en": "demonstration record(s) found.",
    },
    "search_new_search_btn": {
        "bn": "নতুন অনুসন্ধান",
        "en": "New Search",
    },
    "search_not_found_title": {
        "bn": "কোনো প্রদর্শনী রেকর্ড খুঁজে পাওয়া যায়নি",
        "en": "No Demonstration Records Found",
    },
    "search_not_found_desc": {
        "bn": "আমাদের ডেমো ডেটাবেজে এই অনুসন্ধানের সাথে মিল রয়েছে এমন কোনো রেকর্ড পাওয়া যায়নি। অনুগ্রহ করে সঠিক ডেমো রেফারেন্স দিয়ে অনুসন্ধান করুন।",
        "en": "No matching synthetic records were found in the demonstration database. Please try using a valid demonstration reference.",
    },
    "search_try_demo_plots": {
        "bn": "উপলব্ধ ডেমো প্লটগুলো দিয়ে পরীক্ষা করে দেখুন:",
        "en": "Try searching for these available demo plots:",
    },
    "search_btn_all_records": {
        "bn": "সম্পূর্ণ রেকর্ড তালিকা দেখুন",
        "en": "View All Records on Dashboard",
    },

    # -------------------------------------------------------------
    # Plot Detail (plot_detail.html)
    # -------------------------------------------------------------
    "plot_detail_title": {
        "bn": "প্লট রেকর্ড:",
        "en": "Plot Record:",
    },
    "plot_detail_btn_print": {
        "bn": "প্রতিবেদন প্রিন্ট করুন",
        "en": "Print Verification Report",
    },
    "plot_detail_btn_dash": {
        "bn": "ড্যাশবোর্ডে ফিরে যান",
        "en": "Back to Dashboard",
    },
    "plot_rule_findings_title": {
        "bn": "ব্যাখ্যামূলক রুল ইঞ্জিনের ফলাফল ও পর্যবেক্ষণ",
        "en": "Explainable Rule Engine Findings",
    },
    "plot_warning_indicators_evaluated": {
        "bn": "টি সতর্কতা নির্দেশক মূল্যায়িত",
        "en": "warning indicator(s) evaluated",
    },
    "plot_no_warnings_title": {
        "bn": "ডেমো ডেটায় কোনো অসঙ্গতি বা ঝুঁকি নির্দেশক পাওয়া যায়নি",
        "en": "No Simulated Inconsistencies Detected in Demo Data",
    },
    "plot_no_warnings_desc": {
        "bn": "এই প্রদর্শনী রেকর্ডে সংগতিপূর্ণ কাল্পনিক দলিল ও নামজারি নম্বর বিদ্যমান এবং কোনো সমান্তরাল বিক্রয় সংঘাত সনাক্ত হয়নি। বাস্তব লেনদেনে সর্বদা সরেজমিন পরিদর্শন ও রেজিস্ট্রি বালাম বই তল্লাশি করুন।",
        "en": "Consistent deed references and mutation records exist in this demonstration scenario with no parallel conveyance claims. Always conduct physical registry searches before entering actual agreements.",
    },
    "plot_specific_ref": {
        "bn": "নির্দিষ্ট রেফারেন্স:",
        "en": "Affected Reference:",
    },
    "plot_action_required": {
        "bn": "করণীয় যাচাইকরণ পদক্ষেপ:",
        "en": "Recommended Due Diligence Action:",
    },
    "plot_master_card_title": {
        "bn": "মূল প্লটের তথ্যাবলি",
        "en": "Master Plot Attributes",
    },
    "plot_attr_plot_id": {
        "bn": "প্লট নম্বর",
        "en": "Plot Identifier",
    },
    "plot_attr_mouza": {
        "bn": "মৌজা কোড",
        "en": "Demo Mouza Code",
    },
    "plot_attr_area": {
        "bn": "প্রশাসনিক এলাকা",
        "en": "Upazila & District",
    },
    "plot_attr_deed": {
        "bn": "মূল দলিল নম্বর",
        "en": "Primary Deed Reference",
    },
    "plot_attr_khatian": {
        "bn": "খতিয়ান নম্বর",
        "en": "Khatian Reference",
    },
    "plot_attr_mutation": {
        "bn": "নামজারি স্ট্যাটাস",
        "en": "Mutation Status (Namjari)",
    },
    "plot_attr_case": {
        "bn": "মামলা সংক্রান্ত তথ্য",
        "en": "Litigation Status",
    },
    "plot_attr_khas": {
        "bn": "খাস বা অধিগ্রহণ তথ্য",
        "en": "Khas / Acquisition Status",
    },
    "not_available": {
        "bn": "রেকর্ডে অপ্রাপ্ত",
        "en": "Not Available in Records",
    },
    "completeness_title": {
        "bn": "তথ্য পূর্ণাঙ্গতা সূচক",
        "en": "Information Completeness Index",
    },
    "completeness_desc": {
        "bn": "প্রাক-ক্রয় অনুসন্ধানের জন্য প্রয়োজনীয় ৫টি মূল ফিল্ডের উপস্থিতি পরিমাপ করে। তথ্যের অনুপস্থিতি কখনো নিরাপত্তার নিশ্চয়তা নয়।",
        "en": "Measures the presence of five fundamental pre-purchase diligence fields. Missing data must never be mistaken for safety.",
    },
    "completeness_missing_label": {
        "bn": "অনুপস্থিত বা অপ্রাপ্ত ডেমো উপাদানসমূহ:",
        "en": "Missing / Unverified Demo Elements:",
    },
    "completeness_all_present": {
        "bn": "সকল প্রাক-ক্রয় যাচাইকরণ উপাত্ত এই রেকর্ডে বিদ্যমান রয়েছে।",
        "en": "All core pre-purchase verification fields are populated in this demonstration record.",
    },
    "tx_chain_title": {
        "bn": "হস্তান্তরের ধারাবাহিক ইতিহাস",
        "en": "Simulated Transaction History Chain",
    },
    "tx_chain_records_count": {
        "bn": "টি রেকর্ড",
        "en": "record(s)",
    },
    "tx_th_ref": {
        "bn": "লেনদেন রেফারেন্স",
        "en": "Tx Reference",
    },
    "tx_th_deed": {
        "bn": "দলিল নম্বর",
        "en": "Deed Reference",
    },
    "tx_th_type": {
        "bn": "হস্তান্তর ধরন",
        "en": "Transaction Type",
    },
    "tx_th_date": {
        "bn": "তারিখ",
        "en": "Date",
    },
    "tx_th_status": {
        "bn": "স্ট্যাটাস",
        "en": "Record Status",
    },
    "tx_th_conflict": {
        "bn": "সংঘাত গ্রুপ",
        "en": "Conflict Group",
    },
    "tx_empty": {
        "bn": "কোনো লেনদেন রেকর্ড পাওয়া যায়নি।",
        "en": "No transaction records found for this plot.",
    },

    # -------------------------------------------------------------
    # Complete Land Information (Sections A through G)
    # -------------------------------------------------------------
    "sec_a_title": {
        "bn": "ক. জমির প্রাথমিক পরিচিতি",
        "en": "A. Basic Land Identification",
    },
    "plot_attr_khatian_no": {
        "bn": "খতিয়ান নম্বর",
        "en": "Khatian Number",
    },
    "plot_attr_plot_no": {
        "bn": "প্লট নম্বর",
        "en": "Plot Number",
    },
    "plot_attr_dag_no": {
        "bn": "দাগ নম্বর",
        "en": "Dag Number",
    },
    "plot_attr_mouza_name": {
        "bn": "মৌজার নাম",
        "en": "Mouza Name",
    },
    "plot_attr_jl_no": {
        "bn": "জে.এল. নম্বর",
        "en": "J.L. Number (Mouza)",
    },
    "sec_b_title": {
        "bn": "খ. দলিল ও রেজিস্ট্রেশনের তথ্য",
        "en": "B. Deed & Registration Information",
    },
    "plot_attr_deed_no": {
        "bn": "দলিল নম্বর",
        "en": "Deed Number",
    },
    "plot_attr_reg_details": {
        "bn": "দলিল নিবন্ধনের তথ্য",
        "en": "Deed Registration Details",
    },
    "plot_attr_sub_registry": {
        "bn": "সাব-রেজিস্ট্রি অফিসের নাম",
        "en": "Sub-Registry Office Name",
    },
    "sec_c_title": {
        "bn": "গ. নামজারি তথ্য",
        "en": "C. Mutation Information",
    },
    "plot_attr_mutation_status": {
        "bn": "নামজারি / ই-নামজারি",
        "en": "Mutation / E-Namjari Status",
    },
    "sec_d_title": {
        "bn": "ঘ. মামলা-সংক্রান্ত তথ্য",
        "en": "D. Case & Litigation Information",
    },
    "plot_attr_case_info": {
        "bn": "মামলা-সংক্রান্ত তথ্য",
        "en": "Case & Litigation Information",
    },
    "sec_e_title": {
        "bn": "ঙ. সরকারি স্বার্থ",
        "en": "E. Government Interest",
    },
    "plot_attr_gov_interest": {
        "bn": "সরকারি স্বার্থ / খাস বা অধিগ্রহণকৃত জমি",
        "en": "Government Interest / Khas or Acquired Land",
    },
    "sec_f_title": {
        "bn": "চ. জরিপ তথ্য",
        "en": "F. Survey Information",
    },
    "plot_attr_survey_type": {
        "bn": "জরিপের ধরন",
        "en": "Survey Type",
    },
    "sec_g_title": {
        "bn": "ছ. জমির মালিকানা অর্জনের উৎস",
        "en": "G. Source of Ownership",
    },
    "plot_attr_ownership_source": {
        "bn": "জমির মালিকানা অর্জনের উৎস",
        "en": "Source of Ownership",
    },
    "plot_attr_partition_status": {
        "bn": "আপস-বণ্টননামার অবস্থা",
        "en": "Partition Deed Status",
    },

    # -------------------------------------------------------------
    # Automated 7-Step Verification Workflow
    # -------------------------------------------------------------
    "auto_checklist_title": {
        "bn": "৭-দফা স্বয়ংক্রিয় প্রাক-ক্রয় যাচাইকরণ",
        "en": "7-Step Automated Pre-Purchase Verification",
    },
    "auto_checklist_subtitle": {
        "bn": "সিলেক্টেড প্লটের ডাটাবেজ রেকর্ড ও উপলব্ধ দলিলের ভিত্তিতে স্বয়ংক্রিয়ভাবে মূল্যায়িত ফলাফল",
        "en": "Automatically evaluated due diligence against selected plot records and evidence",
    },
    "auto_checklist_eval_label": {
        "bn": "যাচাইকরণ ফলাফল: ৭টি স্বয়ংক্রিয় পরীক্ষা মূল্যায়িত",
        "en": "Verification Results: 7 Checks Evaluated",
    },
    "auto_checklist_passed": {
        "bn": "উত্তীর্ণ",
        "en": "Passed",
    },
    "auto_checklist_warnings": {
        "bn": "সতর্কবার্তা",
        "en": "Warnings",
    },
    "auto_checklist_review": {
        "bn": "পর্যালোচনা প্রয়োজন",
        "en": "Needs Review",
    },
    "auto_checklist_insufficient": {
        "bn": "তথ্য অপ্রাপ্ত",
        "en": "Insufficient Data",
    },
    "auto_checklist_na": {
        "bn": "প্রযোজ্য নয়",
        "en": "Not Applicable",
    },
    "auto_checklist_rerun": {
        "bn": "পুনরায় যাচাই করুন",
        "en": "Re-run Verification",
    },
    "auto_checklist_detected_conflicts": {
        "bn": "শনাক্তকৃত অসঙ্গতি / সংঘাত:",
        "en": "Detected Conflicts / Inconsistencies:",
    },
    "auto_checklist_missing_docs": {
        "bn": "প্রয়োজনীয় অপ্রাপ্ত তথ্য / নথি:",
        "en": "Missing Required Records / Information:",
    },
    "auto_checklist_recommended_action": {
        "bn": "পরামর্শকৃত যাচাইকরণ পদক্ষেপ:",
        "en": "Recommended Next Diligence Action:",
    },
    "auto_checklist_legal_notice": {
        "bn": "স্বয়ংক্রিয় প্রাথমিক স্ক্রীনিং — আইনজীবী দ্বারা যাচাইকরণ এখনও আবশ্যক",
        "en": "Automated Preliminary Screening — Advocate Review Still Required",
    },
    "city_survey_risk_indicator": {
        "bn": "সিটি জরিপ স্ক্রীনিং সূচক (+১ পয়েন্ট)",
        "en": "City Survey Screening Indicator (+1 Point)",
    },

    # -------------------------------------------------------------
    # Checklist (checklist.html)
    # -------------------------------------------------------------
    "checklist_page_title": {
        "bn": "নাগরিক প্রাক-ক্রয় জমি যাচাইকরণ চেকলিস্ট",
        "en": "Citizen Pre-Purchase Land Diligence Checklist",
    },
    "checklist_page_subtitle": {
        "bn": "বাংলাদেশে জমি কেনার পূর্বে প্রতারণা ও জটিল মামলা এড়াতে ৭-দফা বাস্তবসম্মত প্রাক-ক্রয় যাচাই নির্দেশিকা।",
        "en": "A 7-point investigative due diligence checklist to reduce fraud vulnerability and litigation risk before signing property agreements in Bangladesh.",
    },
    "checklist_reset_btn": {
        "bn": "চেকলিস্ট রিসেট",
        "en": "Reset Checklist",
    },
    "checklist_print_btn": {
        "bn": "চেকলিস্ট প্রিন্ট করুন",
        "en": "Print Checklist",
    },
    "checklist_progress_label": {
        "bn": "চেকলিস্ট সম্পন্নতার অবস্থা:",
        "en": "Checklist Progress:",
    },
    "checklist_completed_count_suffix": {
        "bn": "টি ধাপ সম্পন্ন",
        "en": "steps completed",
    },

    # -------------------------------------------------------------
    # Printable Report (report.html)
    # -------------------------------------------------------------
    "report_title": {
        "bn": "জমি প্রাক-ক্রয় যাচাইকরণ প্রতিবেদন",
        "en": "Land Pre-Purchase Verification Summary Report",
    },
    "report_back_btn": {
        "bn": "প্লট রেকর্ডে ফিরে যান",
        "en": "Back to Plot Record",
    },
    "report_print_btn": {
        "bn": "প্রিন্ট করুন / PDF সংরক্ষণ",
        "en": "Print / Save PDF",
    },
    "report_sec1_title": {
        "bn": "১. প্রদর্শনী প্লটের পরিচিতি ও বিবরণ",
        "en": "1. Demonstration Plot Identification & Core Attributes",
    },
    "report_sec2_title": {
        "bn": "২. ব্যাখ্যামূলক রুল ইঞ্জিনের ফলাফল ও পর্যবেক্ষণ",
        "en": "2. Explainable Rule Engine Findings & Observations",
    },
    "report_sec3_title": {
        "bn": "৩. হস্তান্তরের অতীত ধারাবাহিক বিবরণ",
        "en": "3. Simulated Historical Conveyance Chain Log",
    },
    "report_signatures_buyer": {
        "bn": "সম্ভাব্য ক্রেতার স্বাক্ষর ও তারিখ",
        "en": "Prospective Purchaser Signature & Date",
    },
    "report_signatures_counsel": {
        "bn": "আইনজীবীর যাচাই নোট ও স্বাক্ষর",
        "en": "Enrolled Advocate / Legal Counsel Review & Signature",
    },
    "report_disclaimer_title": {
        "bn": "কাল্পনিক প্রদর্শনী রেকর্ড — সরকারি কোনো অফিশিয়াল দলিল নয়:",
        "en": "SYNTHETIC DEMONSTRATION RECORD — NOT AN OFFICIAL GOVERNMENT DOCUMENT:",
    },
    "report_disclaimer_text": {
        "bn": "এই প্রতিবেদনটি একটি শিক্ষামূলক সফটওয়্যার প্রোটোটাইপ দ্বারা প্রস্তুতকৃত। এটি কোনো আইনি স্বত্ব সনদ, সরকারি প্রত্যয়ন, বিচার বিভাগীয় ছাড়পত্র বা নির্ভেজাল দায়মুক্তির নিশ্চয়তা প্রদান করে না। বাংলাদেশে জমি কেনার আগে সর্বদা সংশ্লিষ্ট সাব-রেজিস্ট্রি অফিসে মূল বালাম বই তল্লাশি করুন এবং অভিজ্ঞ সনদপ্রাপ্ত আইনজীবীর পরামর্শ নিন।",
        "en": "This summary report is generated by an educational software prototype. It does not constitute official certification of title, judicial clearance, or guaranteed ownership. Always conduct manual Volume (Balam) book registry searches and retain professional legal counsel prior to entering land conveyances.",
    },

    # -------------------------------------------------------------
    # Haq Shufa Guide (haq_shufa.html)
    # -------------------------------------------------------------
    "haq_shufa_page_title": {
        "bn": "হক শুফা আইনগত সহায়িকা (Haq Shufa Legal Guide)",
        "en": "Haq Shufa Legal Guide (Right of Pre-emption)",
    },
    "haq_shufa_page_subtitle": {
        "bn": "অগ্রক্রয়াধিকার ও জমি ক্রয়ের পূর্বে সতর্কতা নির্দেশিকা (Right of Pre-emption)",
        "en": "Right of Pre-Emption & Pre-Purchase Due Diligence Guide",
    },
    "haq_shufa_hero_p": {
        "bn": "বাংলাদেশে হক শুফা বা অগ্রক্রয়াধিকার সম্পর্কিত তথ্যভিত্তিক নাগরিক আইনি নির্দেশিকা। জমির শ্রেণি, শরিকানা হিস্যার প্রকৃতি, রেজিস্ট্রিকৃত বণ্টননামা দলিল এবং সংবিধিবদ্ধ নোটিশ কীভাবে ক্রেতার ঝুঁকিকে প্রভাবিত করে তা জানুন।",
        "en": "An explainable, fact-based educational guide on Haq Shufa (Right of Pre-emption) under Bangladesh property law. Learn how land classification, co-ownership origin, registered partition deeds, and statutory notice impact buyer vulnerability.",
    },
    "haq_shufa_notice_title": {
        "bn": "আইনি সীমাবদ্ধতা ও সতর্কতা",
        "en": "Educational Scope Notice",
    },
    "haq_shufa_notice_text": {
        "bn": "এই প্ল্যাটফর্মটি কেবলমাত্র আইনি সচেতনতা ও শিক্ষার উদ্দেশ্যে তৈরি এবং কোনো যোগ্য আইনি পরামর্শের বিকল্প নয়। হক শুফার প্রকৃত যোগ্যতা সংশ্লিষ্ট জমির খতিয়ান, সাব-রেজিস্ট্রি বালাম ও আদালতের নজিরের ওপর নির্ভরশীল। জমি ক্রয়ের পূর্বে সর্বদা বাংলাদেশ বার কাউন্সিলের সনদপ্রাপ্ত আইনজীবীর পরামর্শ নিন।",
        "en": "This tool is educational and does not replace qualified legal advice. Pre-emption eligibility depends on complex factual chains, registry volume searches, and judicial precedents. Always consult an enrolled Advocate of the Bangladesh Bar Council.",
    },
    "haq_shufa_what_title": {
        "bn": "হক শুফা বা অগ্রক্রয়াধিকার কী?",
        "en": "Understanding Haq Shufa / Right of Pre-Emption",
    },
    "haq_shufa_what_desc": {
        "bn": "হক শুফা (Right of Pre-emption) হলো এমন একটি বিশেষ আইনগত অগ্রাধিকার, যার অধীনে কোনো যৌথ সম্পত্তির সহ-শরিক (Co-sharer) বা নির্দিষ্ট ক্ষেত্রে সংলগ্ন প্রতিবেশীর অন্য কোনো বহিরাগত ক্রেতার (Third Party Stranger) পরিবর্তে একই মূল্যে উক্ত সম্পত্তি ক্রয় করার অগ্রাধিকার থাকে।",
        "en": "Haq Shufa (Right of Pre-emption) is a preferential legal right under which an existing co-owner, co-sharer tenant, or in specific Islamic jurisprudence, an adjoining neighbor, possesses priority to purchase an immovable property before or in substitution of an outside buyer, on identical terms.",
    },
    "haq_shufa_core_principle": {
        "bn": "মূল আইনি দর্শন: বাংলাদেশের সম্পত্তি আইনের মূল লক্ষ্য হলো যৌথ পরিবারিক সম্পত্তি ও ভিটাভূমিতে অনাকাঙ্ক্ষিত বহিরাগত ব্যক্তির প্রবেশ রোধ করা এবং বৈধ শরিকদের স্বত্ব সুসংহত করার সুযোগ দেওয়া।",
        "en": "Core Legal Principle: In Bangladesh property law, pre-emption is designed to protect joint holdings and shared homesteads from the involuntary intrusion of unfamiliar third parties, enabling legitimate co-owners to consolidate title through legal court proceedings.",
    },
    "haq_shufa_statute_title": {
        "bn": "বাংলাদেশের সংবিধিবদ্ধ আইন কাঠামো",
        "en": "Bangladeshi Statutory Framework",
    },
    "haq_shufa_official_law_text": {
        "bn": "অফিসিয়াল আইন পাঠ",
        "en": "Official Law Text",
    },
    "haq_shufa_tool_title": {
        "bn": "হক শুফা ক্রয়পূর্ব ঝুঁকি নির্দেশক মূল্যায়ন",
        "en": "Haq Shufa Pre-Purchase Risk Indicator Assessment",
    },
    "haq_shufa_tool_desc": {
        "bn": "জমি ক্রয়ের পূর্বে সম্ভাব্য অগ্রক্রয়াধিকারের ঝুঁকি যাচাই করতে বাস্তব তথ্যভিত্তিক প্রশ্নগুলোর উত্তর দিন।",
        "en": "Answer factual due diligence questions to evaluate pre-emption indicators under Bangladesh land law. Results are categorized into three informational groups.",
    },
    "haq_shufa_load_demo": {
        "bn": "টেস্ট সিনারিও লোড করুন:",
        "en": "Load Synthetic Test Scenarios:",
    },
    "haq_shufa_scenario_1_btn": {
        "bn": "দৃশ্যপট ১ (ওয়ারিশি কৃষিজমি)",
        "en": "Scenario 1 (Inheritance)",
    },
    "haq_shufa_scenario_2_btn": {
        "bn": "দৃশ্যপট ২ (অযাচাইকৃত তথ্য)",
        "en": "Scenario 2 (Unverified Facts)",
    },
    "haq_shufa_scenario_3_btn": {
        "bn": "দৃশ্যপট ৩ (বণ্টনকৃত একক জোত)",
        "en": "Scenario 3 (Partitioned Sole Holding)",
    },
    "haq_shufa_eval_btn": {
        "bn": "ক্রয়পূর্ব ঝুঁকি নির্দেশক মূল্যায়ন করুন",
        "en": "Evaluate Pre-Purchase Risk Indicators",
    },
    "haq_shufa_reset_btn": {
        "bn": "রিসেট",
        "en": "Reset Questions",
    },
    "haq_shufa_print_btn": {
        "bn": "মূল্যায়ন রিপোর্ট প্রিন্ট করুন",
        "en": "Print Assessment",
    },
    "haq_shufa_findings_title": {
        "bn": "চিহ্নিত বাস্তব নির্দেশকসমূহ",
        "en": "Observed Factual Indicators",
    },
    "haq_shufa_provisions_title": {
        "bn": "প্রযোজ্য আইনগত ধারা ও তথ্যসূত্র",
        "en": "Relevant Legal Provisions & Citations",
    },
    "haq_shufa_steps_title": {
        "bn": "দলিল স্বাক্ষরের পূর্বে ক্রেতার জন্য করণীয় সতর্কতা",
        "en": "Citizen Due Diligence Steps Before Signing Deed",
    },
    "haq_shufa_roadmap_title": {
        "bn": "ক্রয়পূর্ব আইনি অনুসন্ধান নির্দেশিকা (Due Diligence Roadmap)",
        "en": "Pre-Purchase Due Diligence Roadmap",
    },
    "haq_shufa_roadmap_desc": {
        "bn": "জমি ক্রয়ের পরবর্তী সময়ে অগ্রক্রয়াধিকার বা হক শুফার মোকদ্দমা এড়াতে বাংলাদেশে অনুসৃত প্রমিত অনুসন্ধান পদক্ষেপ।",
        "en": "Standard investigative steps required in Bangladesh to minimize post-purchase pre-emption litigation.",
    },

    # -------------------------------------------------------------
    # Error Pages (404.html, 500)
    # -------------------------------------------------------------
    "error_404_title": {
        "bn": "তথ্য বা পৃষ্ঠা পাওয়া যায়নি",
        "en": "Record or Page Not Found",
    },
    "error_404_heading": {
        "bn": "তথ্য বা পৃষ্ঠা খুঁজে পাওয়া যায়নি",
        "en": "Requested Page or Record Not Found",
    },
    "error_404_desc": {
        "bn": "অনুরোধকৃত ডেমো প্লট বা পৃষ্ঠাটি ডেমোনস্ট্রেশন ডাটাবেজে খুঁজে পাওয়া যায়নি।",
        "en": "The requested synthetic plot or page could not be located in the demonstration database.",
    },
    "error_404_placeholder": {
        "bn": "ডেমো প্লট আইডি, খতিয়ান বা দলিল নং লিখুন...",
        "en": "Search demo plots, khatians, deeds...",
    },
    "error_btn_home": {
        "bn": "হোম পেজ",
        "en": "Home Page",
    },
    "error_btn_dashboard": {
        "bn": "ড্যাশবোর্ড",
        "en": "Dashboard",
    },
}


def t(key: str, lang: str = "bn", default: Optional[str] = None) -> str:
    """
    Retrieve localized string for a given key and language.
    Falls back to English if key is missing in Bangla, or returns default/key if not found.
    """
    normalized_lang = "en" if lang == "en" else "bn"
    entry = TRANSLATIONS.get(key)
    if not entry:
        return default if default is not None else key
    return entry.get(normalized_lang) or entry.get("en") or entry.get("bn") or default or key


def get_checklist_items(lang: str = "bn") -> list:
    """Return the 7 standardized citizen pre-purchase diligence checklist items."""
    is_bn = (lang != "en")
    return [
        {
            "id": "step_deed",
            "number": "১" if is_bn else "1",
            "title": "মূল দলিল বালাম তল্লাশি ও সত্যতা যাচাই" if is_bn else "Original Title Deed (Dalil) Volume Book Search",
            "title_alt": "Original Title Deed (Dalil) Verification" if is_bn else "মূল দলিল বালাম তল্লাশি ও সত্যতা যাচাই",
            "authority": "সাব-রেজিস্ট্রি অফিস" if is_bn else "Sub-Registry Office",
            "desc": (
                "সংশ্লিষ্ট সাব-রেজিস্ট্রি অফিস থেকে বিক্রেতার ক্রয়/হেবা/বণ্টন দলিলের সার্টিফাইড নকল তুলুন। "
                "মূল ভলিউম বালাম বইয়ে তল্লাশি দিয়ে দলিল নম্বর, রেজিস্ট্রেশনের তারিখ, পণমূল্য ও নির্ভেজাল দায়মুক্তি যাচাই করুন।"
                if is_bn else
                "Obtain a certified copy (Nokol) of the seller's purchase, heba, or partition deed from the Sub-Registry office. "
                "Inspect the physical Volume (Balam) book to verify deed registration number, execution date, consideration, and encumbrance status."
            ),
        },
        {
            "id": "step_mutation",
            "number": "২" if is_bn else "2",
            "title": "নামজারি খতিয়ান ও ডিসিআর পরীক্ষা" if is_bn else "Mutation Khatian (Namjari) & DCR Verification",
            "title_alt": "Mutation Khatian (Namjari) & DCR Examination" if is_bn else "নামজারি খতিয়ান ও ডিসিআর পরীক্ষা",
            "authority": "সহকারী কমিশনার (ভূমি) অফিস" if is_bn else "AC (Land) Office",
            "desc": (
                "স্টেট অ্যাকুইজিশন অ্যান্ড প্রজাস্বত্ব আইনের অধীন বিক্রেতার নিজ নামে নামজারি (ই-নামজারি) সম্পন্ন হয়েছে কি না নিশ্চিত হোন। "
                "নামজারি খতিয়ান পর্চা, ডিসিআর (Duplicate Carbon Receipt) এবং হাল সনের ভূমি উন্নয়ন কর (খাজনা দাখিলা) যাচাই করুন।"
                if is_bn else
                "Confirm that the seller has completed mutation (e-Namjari) under the SAT Act in their own name. "
                "Verify the Mutation Khatian Porcha, Duplicate Carbon Receipt (DCR), and up-to-date Land Development Tax receipt (Dakhila)."
            ),
        },
        {
            "id": "step_chain",
            "number": "৩" if is_bn else "3",
            "title": "ধারাবাহিক বায়া দলিল ও অতীত জরিপ পরচা" if is_bn else "Continuous Chain of Title & Survey Records (CS/SA/RS/BS)",
            "title_alt": "Continuous Chain of Title & Historical Surveys" if is_bn else "ধারাবাহিক বায়া দলিল ও অতীত জরিপ পরচা",
            "authority": "জেলা রেকর্ড রুম ও ভূমি অফিস" if is_bn else "District Record Room & Land Office",
            "desc": (
                "কমপক্ষে ১২ থেকে ২৫ বছরের পূর্ববর্তী ধারাবাহিক মালিকানা দলিল (বায়া দলিল) পরীক্ষা করুন। "
                "সিএস (CS), এসএ (SA), আরএস (RS), এবং সিটি/বিএস (BS) জরিপের খতিয়ান ধারাবাহিকতায় কোনো বিচ্যুতি আছে কি না খতিয়ে দেখুন।"
                if is_bn else
                "Examine the unbroken historical chain of prior title deeds (Bia Dalil) spanning at least 12 to 25 years. "
                "Verify continuous link across historical land records including CS, SA, RS, and City/BS surveys to avoid missing-link disputes."
            ),
        },
        {
            "id": "step_partition",
            "number": "৪" if is_bn else "4",
            "title": "রেজিস্ট্রিকৃত আপস-বণ্টননামা ও ওয়ারিশ সনদ" if is_bn else "Registered Partition Deed (Bontonnama) & Heirship Certificate",
            "title_alt": "Partition Deed & Genealogy Examination" if is_bn else "রেজিস্ট্রিকৃত আপস-বণ্টননামা ও ওয়ারিশ সনদ",
            "authority": "ইউনিয়ন পরিষদ / সিটি কর্পোরেশন" if is_bn else "Union Parishad / City Corporation",
            "desc": (
                "জমিটি পৈতৃক বা যৌথ সম্পত্তি হলে সংশ্লিষ্ট ইউনিয়ন পরিষদ/ওয়ার্ড কাউন্সিলর কর্তৃক প্রদত্ত নির্ভুল ওয়ারিশ সনদ নিন। "
                "সকল শরিক কর্তৃক স্বাক্ষরিত রেজিস্ট্রিকৃত আপস-বণ্টননামা দলিল নিশ্চিত করুন, যাতে ভবিষ্যতে হক শুফা বা স্বত্বের দাবি না ওঠে।"
                if is_bn else
                "If the property originated through inheritance or joint holding, obtain a verified genealogy certificate. "
                "Ensure an executed, registered partition deed (Aposh Bontonnama) exists among all heirs to prevent future pre-emption claims."
            ),
        },
        {
            "id": "step_court",
            "number": "৫" if is_bn else "5",
            "title": "দেওয়ানি আদালত ও নিষেধাজ্ঞা অনুসন্ধান" if is_bn else "Civil Court Title Suit & Injunction Search",
            "title_alt": "Civil Court Litigation Search" if is_bn else "দেওয়ানি আদালত ও নিষেধাজ্ঞা অনুসন্ধান",
            "authority": "যুগ্ম জেলা জজ আদালত" if is_bn else "Joint District Judge Court",
            "desc": (
                "স্থানীয় সিনিয়র সহকারী জজ ও যুগ্ম জেলা জজ আদালতে কোনো স্বত্ব মোকদ্দমা, বণ্টন মামলা বা অস্থায়ী নিষেধাজ্ঞা চলমান আছে কি না অনুসন্ধান করুন। "
                "ব্যাংক বা আর্থিক প্রতিষ্ঠানে জমিটি দায়বদ্ধ বা বন্ধক রাখা আছে কি না যাচাই করুন।"
                if is_bn else
                "Conduct title suit inquiries at local civil courts (Senior Assistant Judge & Joint District Judge) to verify no pending injunctions, partition suits, or mortgage liens exist."
            ),
        },
        {
            "id": "step_khas",
            "number": "৬" if is_bn else "6",
            "title": "খাস, অর্পিত বা সরকারি অধিগ্রহণ যাচাই" if is_bn else "Government Khas, Vested, or Acquisition Verification",
            "title_alt": "Khas & Government Acquisition Screening" if is_bn else "খাস, অর্পিত বা সরকারি অধিগ্রহণ যাচাই",
            "authority": "উপজেলা ভূমি অফিস ও ডিসি অফিস" if is_bn else "Upazila Land Office & DC Office (LA)",
            "desc": (
                "জমিটি সরকারি খাস খতিয়ানভুক্ত, অর্পিত সম্পত্তি (Vested Property), পরিত্যক্ত সম্পত্তি কিংবা সরকারের কোনো উন্নয়ন প্রকল্পের জন্য অধিগ্রহণ নোটিশভুক্ত কি না নিশ্চিত হোন।"
                if is_bn else
                "Confirm that the plot is not classified as government Khas, Vested Property ('Ka' or 'Kha' schedules), abandoned land, or marked for public acquisition by the DC Office."
            ),
        },
        {
            "id": "step_advocate",
            "number": "৭" if is_bn else "7",
            "title": "সনদপ্রাপ্ত আইনজীবী দ্বারা দলিল খসড়া ও স্বত্ব যাচাই" if is_bn else "Professional Legal Counsel Deed Drafting & Vetting",
            "title_alt": "Advocate Legal Title Vetting" if is_bn else "সনদপ্রাপ্ত আইনজীবী দ্বারা দলিল খসড়া ও স্বত্ব যাচাই",
            "authority": "বার কাউন্সিল আইনজীবী" if is_bn else "Bar Council Enrolled Advocate",
            "desc": (
                "বায়না দলিল (Baina) বা চূড়ান্ত সাফ-কবলা দলিল রেজিস্ট্রির পূর্বে বাংলাদেশ বার কাউন্সিলের একজন অভিজ্ঞ আইনজীবীকে দিয়ে মূল স্বত্ব প্রতিবেদন প্রস্তুত করান। "
                "চৌকহদ্দি (Boundary Demarcation) ও দখল সরেজমিনে নিশ্চিত করুন।"
                if is_bn else
                "Engage an experienced Bar Council enrolled advocate to inspect original documents, draft the conveyance deed with exact boundary schedules (Chouhaddi), and confirm physical possession."
            ),
        },
    ]


def get_roadmap_items(lang: str = "bn") -> list:
    """Return the due diligence roadmap table items in selected language."""
    is_bn = (lang != "en")
    return [
        {
            "stage": "বায়া দলিল ও ভলিউম বালাম তল্লাশি" if is_bn else "Bia Deeds & Registry Volume Search",
            "authority": "সাব-রেজিস্ট্রি অফিস" if is_bn else "Sub-Registry Office",
            "objectives": (
                "কমপক্ষে ১২ থেকে ২৫ বছরের মালিকানা হস্তান্তর ধারাবাহিকতা ও দায়বদ্ধতা তল্লাশি।"
                if is_bn else
                "Inspect Volume Books for minimum 12-25 years chain of title and encumbrance search."
            ),
            "significance": (
                "পূর্বতন হস্তান্তর, সাবেক শরিক ও রেজিস্ট্রিকৃত বণ্টননামার তথ্য প্রকাশ করে।"
                if is_bn else
                "Discloses recorded transfers, previous co-sharers, and registered partition deeds."
            ),
            "significance_class": "text-danger fw-semibold",
        },
        {
            "stage": "ওয়ারিশ কায়েম সনদপত্র" if is_bn else "Heirship Certificate",
            "authority": "ইউনিয়ন পরিষদ / সিটি ওয়ার্ড কার্যালয়" if is_bn else "Union Parishad / City Ward",
            "objectives": (
                "মৃত সাবেক মালিকের সকল বৈধ পুরুষ ও মহিলা ওয়ারিশের তালিকা যাচাই।"
                if is_bn else
                "Verified genealogy listing all legal male and female heirs of deceased predecessor owners."
            ),
            "significance": (
                "ওয়ারিশসূত্রে সহ-শরিকদের চিহ্নিত করে যাদের SAT Act ধারা ৯৬ অনুসারে হক শুফার অধিকার রয়েছে।"
                if is_bn else
                "Identifies co-sharers by inheritance who possess Section 96 SAT Act pre-emption rights."
            ),
            "significance_class": "text-danger fw-semibold",
        },
        {
            "stage": "রেজিস্ট্রিকৃত আপস-বণ্টননামা দলিল" if is_bn else "Registered Partition Deed",
            "authority": "সাব-রেজিস্ট্রি অফিস" if is_bn else "Sub-Registry Office",
            "objectives": (
                "সকল ওয়ারিশ কর্তৃক স্বাক্ষরিত ও রেজিস্ট্রিকৃত বণ্টননামা দলিলের অস্তিত্ব নিশ্চিতকরণ।"
                if is_bn else
                "Confirm execution and registration of a formal partition deed signed by all heirs."
            ),
            "significance": (
                "যৌথ মালিকানার অবসান ঘটায় এবং সুনির্দিষ্ট প্লটের পৃথক সীমানা প্রতিষ্ঠা করে।"
                if is_bn else
                "Extinguishes joint tenancy; demarcates specific separate plot boundaries."
            ),
            "significance_class": "text-success fw-semibold",
        },
        {
            "stage": "নামজারি খতিয়ান ও ডিসিআর" if is_bn else "Separate Mutation & DCR",
            "authority": "সহকারী কমিশনার (ভূমি) কার্যালয়" if is_bn else "AC (Land) Office",
            "objectives": (
                "বিক্রেতার নামে পৃথক নামজারি খতিয়ান, ডিসিআর রসিদ ও হালনাগাদ ভূমি উন্নয়ন কর দাখিলা নিশ্চিতকরণ।"
                if is_bn else
                "Ensure seller has opened an independent Mutation Khatian, DCR receipt, and up-to-date land development tax dakhila."
            ),
            "significance": (
                "আলাদা জমা-খারিজ এবং সরকারের কাছে পৃথক খাজনা প্রদানের বৈধ প্রমাণপত্র।"
                if is_bn else
                "Demonstrates separate fiscal assessment and segregated holding."
            ),
            "significance_class": "text-success fw-semibold",
        },
        {
            "stage": "সংবিধিবদ্ধ হস্তান্তর নোটিশ" if is_bn else "Statutory Transfer Notice",
            "authority": "সাব-রেজিস্ট্রি অফিস" if is_bn else "Sub-Registry Office",
            "objectives": (
                "SAT Act ধারা ৮৯ বা NAT Act ধারা ২৩ অনুসারে রেকর্ডীয় সহ-শরিকদের আনুষ্ঠানিক নোটিশ জারি।"
                if is_bn else
                "Issuance of notice under Section 89 of the SAT Act or Section 23 of the NAT Act to recorded co-sharers."
            ),
            "significance": (
                "আইনগত তামাদির সময়সীমা সীমিত করে (SAT Act-এর জন্য ২ মাস, NAT Act-এর জন্য ৪ মাস)।"
                if is_bn else
                "Restricts statutory limitation window (2 months for SAT Act, 4 months for NAT Act)."
            ),
            "significance_class": "text-warning fw-semibold",
        },
    ]
