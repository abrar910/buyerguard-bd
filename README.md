# BuyerGuard BD — Smart Land Pre-Purchase Verification Platform
> **Tagline:** *Check Before You Buy.*  
> **Track:** Track P5 — Citizen Pre-Purchase Verification (Related: Track P3 — Fraud & Double-Selling Detection)  
> **Prepared for:** LandTech Innovation Hackathon 2026, Daffodil International University (DIU), Bangladesh  

---

## 1. Executive Summary & Problem Context

In Bangladesh, land transactions are notoriously complex and vulnerable to fraudulent conveyances. Citizens face an administrative divide:
- **Registration Directorate (Sub-Registry):** Registers deeds (*Dalil*) under the Registration Act, 1908.
- **Ministry of Land (AC Land / Tahsil):** Maintains mutation khatians (*Namjari*), Duplicate Carbon Receipts (*DCR*), and land tax receipts (*Dakhila*) under the State Acquisition and Tenancy Act, 1950.

Because these databases have historically been siloed, prospective buyers struggle to verify:
1. Whether multiple active deeds have been executed for the same plot (**Double-Selling / Fraud**).
2. Whether the seller's mutation (*Namjari*) is officially recorded.
3. Whether the historical chain of title (*Bia Dalil*) is continuous through historical surveys (CS, SA, RS, BS).
4. Whether the plot has undisclosed civil court injunctions or government *Khas* / acquisition notices.

**BuyerGuard BD** is an explainable, citizen-facing pre-purchase verification platform prototype. It organizes synthetic land plot records, cross-references deed and mutation status, applies deterministic Python rules to detect simulated anomalies (including duplicate-sale conflicts), guides users with an interactive 7-point due diligence checklist, and generates printable summary reports.

---

## 2. Implemented Features

- **Dynamic Records Dashboard (`/dashboard`):** Real-time statistics derived directly from SQLite and the deterministic rule engine (Total demo plots, review-required flags, duplicate-sale conflicts, and incomplete records).
- **Multi-Criteria Search (`/search`):** Query synthetic plots by Plot ID (`PLOT-1004`), Khatian reference (`KH-DEMO-1001`), Deed reference (`DEED-DEMO-1002`), or Mouza code (`DEMO-MOUZA-01`) with clear not-found guidance.
- **Explainable Anomaly & Risk Detection Engine (`risk_engine.py`):**
  - `RULE_DUP_SALE`: Detects simulated duplicate-sale conflicts where multiple active transactions have differing deed claims.
  - `RULE_INCOMPLETE_RECORD`: Highlights missing mutation status, deed reference, or khatian numbers.
  - `RULE_REF_MISMATCH`: Identifies discrepancies between the plot master record and active transfer deed numbers.
  - `RULE_UNKNOWN_CASE`: Advises citizens when litigation status is unrecorded in demo data.
  - `RULE_UNKNOWN_KHAS`: Flags unverified Khas or government acquisition status.
- **Completeness Index:** Quantitative scoring percentage (e.g. 100%, 78%, 56%) calculating the presence of essential diligence fields so missing data is never mistaken for safety.
- **Interactive Citizen Pre-Purchase Checklist (`/checklist` & on plot details):** A 7-point diligence tracker persisted in `localStorage` covering Sub-Registry checks, e-Namjari porcha, historical Bia deeds, partition deeds (*Bontonnama*), civil court checks, khas vetting, and advocate review.
- **Printable Due Diligence Summary Report (`/plots/<plot_id>/report`):** Formal print-ready document (`@media print`) complete with metadata, explainable warnings, and signature blocks for prospective buyers and legal counsel.
- **Deterministic Synthetic Seed Data (`seed_data.py`):** 22 structured fictional demonstration plots and transaction chains reflecting realistic Bangladesh scenarios.
- **Health Check Endpoint (`/health`):** JSON endpoint verifying active SQLite connection and plot count.
- **100% Automated Test Suite:** 24 unit and integration tests passing with `pytest`.

---

## 3. Technology Stack

- **Backend:** Python 3.11, Flask 3.1, Jinja2 Templates.
- **Database:** SQLite3 (standard Python library) with foreign key constraints, indexes, and parameterized queries.
- **Logic Engine:** Deterministic, rule-based Python module (`risk_engine.py`).
- **Frontend:** HTML5, CSS3 (custom navy/teal design system + print stylesheet), Bootstrap 5.3, Bootstrap Icons, Vanilla JavaScript.
- **Testing:** `pytest` (24 test cases covering routes, rules, and disclaimers).
- **Environment & Package Management:** `uv` by Astral (self-contained, reproducible virtual environment).

*Zero External Dependency Requirements:* Requires no paid API keys, no Google Maps API keys, no Hugging Face API keys, and no live government credentials. Runs entirely locally and offline.

---

## 4. SQLite Database Architecture

The application uses an embedded SQLite database (`buyerguard.db`) initialized automatically on startup:

### `plots` Table
- `id` (INTEGER PRIMARY KEY AUTOINCREMENT)
- `plot_id` (TEXT UNIQUE NOT NULL) — Fictional identifier (e.g. `PLOT-1001`)
- `demo_district` (TEXT NOT NULL) — Administrative division (e.g. "Demo District A")
- `demo_upazila` (TEXT NOT NULL) — Upazila division (e.g. "Demo Upazila 01")
- `demo_mouza_code` (TEXT NOT NULL) — Mouza designation (e.g. "DEMO-MOUZA-01")
- `khatian_ref` (TEXT) — Khatian reference (e.g. `KH-DEMO-1001`)
- `deed_ref` (TEXT) — Primary registered title deed reference
- `mutation_status` (TEXT) — "Mutated", "Missing", "Pending", etc.
- `case_info_status` (TEXT) — Litigation verification status
- `khas_acquisition_status` (TEXT) — Khas / Acquisition status
- `description` (TEXT) — Scenario details
- `created_at` (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)

### `transactions` Table
- `id` (INTEGER PRIMARY KEY AUTOINCREMENT)
- `plot_id` (TEXT NOT NULL, FOREIGN KEY -> plots.plot_id)
- `transaction_ref` (TEXT NOT NULL) — Transaction reference code (e.g. `TX-1004-CLAIM-A`)
- `deed_ref` (TEXT) — Specific deed cited in the transaction
- `transaction_type` (TEXT NOT NULL) — Sale, Purchase, Inheritance, Gift, or Simulated Duplicate Sale
- `transaction_date` (TEXT NOT NULL) — YYYY-MM-DD
- `record_status` (TEXT NOT NULL) — "Active", "Superseded", or "Pending"
- `conflict_group_id` (TEXT) — Identifies simulated conflict groups (e.g. `CONF-1004`)

Indexes are applied to `plots(plot_id)`, `plots(khatian_ref)`, `plots(deed_ref)`, `plots(demo_mouza_code)`, and `transactions(plot_id)`.

---

## 5. Synthetic Demonstration Data & Predictable Scenarios

All data is strictly fictional. Key test cases include:
1. **`PLOT-1001` (Clean Benchmark):** Complete records, completed mutation, no active litigation, 100% completeness score, no triggered flags.
2. **`PLOT-1002` (Missing Mutation):** Valid deed but missing mutation record; triggers `RULE_INCOMPLETE_RECORD`.
3. **`PLOT-1003` (Missing Deed Reference):** Lacks primary deed number in plot master table; triggers `RULE_INCOMPLETE_RECORD`.
4. **`PLOT-1004` (Double-Selling Conflict):** Two active transactions (`TX-1004-CLAIM-A` & `TX-1004-CLAIM-B`) with distinct deeds under `CONF-1004`; triggers `RULE_DUP_SALE` (High Severity).
5. **`PLOT-1005` (Reference Mismatch):** Plot master deed (`DEED-DEMO-1005-MASTER`) contradicts active transaction deed (`DEED-DEMO-1005-ALT`); triggers `RULE_REF_MISMATCH`.
6. **`PLOT-1006` (Unverified Litigation):** Case status is unknown; triggers `RULE_UNKNOWN_CASE`.
7. **`PLOT-1007` (Unverified Khas / Acquisition):** Vetting is unrecorded; triggers `RULE_UNKNOWN_KHAS`.
8. **`PLOT-1008` (Multi-Warning Plot):** Combines missing mutation, unverified litigation, and unverified acquisition status.
9. **`PLOT-1009` (Legitimate Historical Chain):** 3-stage chain (Inheritance 2012 -> Gift 2018 -> Sale 2022). Older records are marked `Superseded`, demonstrating that healthy multi-transfer histories do not trigger false conflict warnings.

---

## 6. Installation & Execution Guide

For a controlled Linux VPS setup using Gunicorn, systemd, Nginx, a protected secret, and a database outside the release directory, see [docs/deployment.md](docs/deployment.md). The checked-in files under `deployment/` are configuration templates only; they do not deploy anything remotely.

### Prerequisites
- Python 3.10+ (or Python 3.11 installed via `uv`)
- Web browser (Chrome, Edge, Firefox, or Safari)

### Step 1: Clone or Navigate to Project Directory
```bash
cd buyerguard-bd
```

### Step 2: Create and Activate Virtual Environment
```bash
# Using standard Python:
python -m venv .venv

# On Windows (PowerShell):
.\.venv\Scripts\activate

# On Linux/macOS:
source .venv/bin/activate
```

### Step 3: Install Required Packages
```bash
pip install -r requirements.txt
```

### Step 4: Run the Application
```bash
python app.py
```
*(The SQLite database automatically initializes and populates all 22 synthetic seed records on first launch.)*

### Step 5: Open in Your Browser
Visit: **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 7. Running the Automated Tests

To run the full suite of 24 unit and integration tests:

```bash
pytest -v
```

Expected output:
```
tests/test_app.py::test_landing_page PASSED
tests/test_app.py::test_dashboard_statistics PASSED
tests/test_app.py::test_search_known_plot PASSED
tests/test_app.py::test_search_unknown_plot_not_found_state PASSED
tests/test_app.py::test_clean_plot_detail PASSED
tests/test_app.py::test_missing_mutation_scenario PASSED
tests/test_app.py::test_missing_deed_scenario PASSED
tests/test_app.py::test_duplicate_sale_scenario PASSED
tests/test_app.py::test_mismatch_reference_scenario PASSED
tests/test_app.py::test_unknown_case_scenario PASSED
tests/test_app.py::test_unknown_khas_scenario PASSED
tests/test_app.py::test_multi_warning_scenario PASSED
tests/test_app.py::test_printable_report PASSED
tests/test_app.py::test_standalone_checklist PASSED
tests/test_app.py::test_health_endpoint PASSED
tests/test_app.py::test_invalid_plot_returns_404 PASSED
tests/test_app.py::test_no_official_government_claims PASSED
tests/test_risk_engine.py::test_clean_plot_evaluation PASSED
tests/test_risk_engine.py::test_missing_mutation_warning PASSED
tests/test_risk_engine.py::test_missing_deed_ref_warning PASSED
tests/test_risk_engine.py::test_duplicate_sale_conflict_warning PASSED
tests/test_risk_engine.py::test_legitimate_historical_chain_does_not_trigger_duplicate_sale PASSED
tests/test_risk_engine.py::test_inconsistent_reference_warning PASSED
tests/test_risk_engine.py::test_unknown_case_and_khas_warnings PASSED

============================= 24 passed in 6.31s ==============================
```

---

## 8. AI Coding Assistant Disclosure

In accordance with LandTech Innovation Hackathon 2026 rules:
- **Tool Used:** Antigravity AI Coding Assistant (Google DeepMind Advanced Agentic Coding).
- **Role:** Antigravity assisted the development team in structuring the project files, configuring SQLite database schemas, coding the explainable risk engine rules, designing the responsive Bootstrap 5 interface, and generating the pytest test suite.
- **Review & Ownership:** All code, logic, documentation, and synthetic data were reviewed, verified, and tested by the student team.

---

## 9. Known Limitations & Future Roadmap

### Current Limitations:
- **Offline / Synthetic Prototype:** Uses an offline SQLite database. It is not connected to live government servers or the DGLRS e-Mutation API.
- **Deterministic Rules:** Uses rule-based logic; it does not perform optical character recognition (OCR) on handwritten historical deeds.
- **Single-Tenant Local MVP:** Designed for local evaluation without multi-user authentication.

### Future Roadmap:
1. **Government API Integration:** Direct read-only connection to Land Reform Board (LRB) e-Namjari and Sub-Registry e-Registration databases.
2. **Bengali (Bangla) Language Localization:** Full bilingual toggle for English and Bengali to maximize citizen accessibility across rural upazilas.
3. **GIS & Mouza Map Boundary Overlay:** Integration with Bangladesh Digital Survey (BDS) spatial coordinates to visualize physical plot boundaries.

---

## 10. Data, Privacy & Ethical Statement

- **100% Synthetic Data:** No real citizen names, National ID (NID) numbers, phone numbers, or real-world parcel coordinates exist within this repository.
- **No Scraping:** The system does not scrape or crawl government websites.
- **Responsible Claims:** The system explicitly avoids words like "Government Verified", "Ownership Guaranteed", or "Legally Safe". All generated reports and screens display a mandatory synthetic data disclaimer.

---
**BuyerGuard BD &copy; 2026** &bull; Daffodil International University LandTech Innovation Hackathon Submission.
