# BuyerGuard BD — Smart Land Pre-Purchase Verification Platform
## Concept Note & Technical Brief
**LandTech Innovation Hackathon 2026**  
**Daffodil International University, Bangladesh**

---

### 1. Project Title & Executive Abstract

- **Project Title:** BuyerGuard BD — Smart Land Pre-Purchase Verification Platform  
- **Tagline:** *Check Before You Buy.*  
- **Primary Hackathon Track:** Track P5 — Citizen Pre-Purchase Verification  
- **Related Hackathon Feature:** Track P3 — Fraud & Double-Selling Detection  
- **Category:** LegalTech / PropTech / Citizen-Facing Digital Land Governance  

**Abstract:**  
Purchasing immovable property in Bangladesh is notoriously fraught with opacity, fragmented documentation, and high fraud risks. Prospective purchasers must manually cross-reference records across disconnected administrative bodies: original deeds (Dalil) at local Sub-Registry offices, mutation khatians (Namjari) and Duplicate Carbon Receipts (DCR) at Upazila Land Offices (AC Land), historical survey records (CS, SA, RS, City/BS) at District Settlement offices, and litigation registries at local civil courts. Incomplete or contradictory records frequently result in fraudulent conveyances and catastrophic double-selling disputes.

**BuyerGuard BD** is an explainable, citizen-centric pre-purchase verification platform prototype. It aggregates demonstration land records into a single intuitive interface, evaluating records against a deterministic Python rule engine to detect simulated duplicate-sale conflicts, flag incomplete mutations, highlight deed discrepancies, and guide prospective buyers through an interactive 7-point due diligence checklist and printable verification summary.

---

### 2. Selected Problem Statement & Bangladesh Context

In Bangladesh, land administration is structurally bifurcated between:
1. **The Registration Directorate (Ministry of Law, Justice and Parliamentary Affairs):** Administers deeds (Dalil) through Sub-Registry offices under the Registration Act, 1908.
2. **The Ministry of Land:** Administers land records, surveys, mutation (Namjari), and land revenue (Khajna) through Deputy Commissioner (DC) offices, Upazila Assistant Commissioners (Land), and Union Land Offices under the State Acquisition and Tenancy Act, 1950.

Because these administrative repositories historically operate without real-time synchronization, prospective buyers face several critical systemic challenges:
- **Double-Selling / Parallel Deeds:** Unscrupulous sellers exploit registration delays or unmutated records to execute duplicate transfer deeds with multiple unsuspecting buyers.
- **Unmutated Land Conveyance:** Buyers purchase land without checking whether the seller's title was mutated in the government revenue ledger, creating unresolvable title disputes.
- **Incomplete Chain of Title (Bia Dalil):** Gaps between historical survey records (CS, SA, RS, BS) and current ownership remain undetected until after earnest money has changed hands.
- **Unverified Encumbrances & Court Injunctions:** Undisclosed partition disputes or pending title suits in local civil courts leave buyers vulnerable to eviction.
- **Khas & Acquisition Notices:** Land subject to government acquisition under the Acquisition and Requisition of Immovable Property Act, 2017, or classified as Khas/Vested property is mistakenly transacted.

---

### 3. Proposed Solution

BuyerGuard BD bridges this informational divide for ordinary citizens by offering a transparent pre-purchase verification gateway:
- **Unified Demonstration Dossier:** Organizes deed references, khatian records, administrative codes (District, Upazila, Mouza), and simulated transaction logs into an accessible single-screen view.
- **Explainable Rule Engine:** Rather than relying on opaque algorithms, the system applies deterministic, auditable rules that state exactly which field is missing or inconsistent and why it matters.
- **Simulated Double-Selling Detection:** Evaluates active transactions on a plot to identify conflicting active sale claims or parallel deed conveyances.
- **Completeness Index:** Calculates a quantitative data completeness score, preventing buyers from confusing "no record found" with "legally safe."
- **Interactive Citizen Diligence Checklist:** A guided 7-stage due diligence workflow persisted in browser local storage.
- **Printable Due Diligence Summary:** A print-formatted verification report that prospective buyers can present to certified advocates for formal legal searches.

*Important Disclosure:* BuyerGuard BD is an educational and technical prototype. All records are synthetic. The platform does not claim official title certification or live government integration.

---

### 4. System Architecture & Technology Stack

The platform is engineered with a modular, lightweight, zero-dependency architecture designed to run reliably on resource-constrained local machines without paid external API keys:

```
[ Citizen Web Client (HTML5 / Bootstrap 5 / Vanilla JS) ]
                          │
                   HTTP / REST
                          ▼
             [ Flask Web Application (Python 3.11) ]
              ├── Routing & Context Ingestion
              ├── Jinja2 Templating Engine
              └── Explainable Rule Engine (risk_engine.py)
                          │
                 Parameterized SQL
                          ▼
            [ SQLite Embedded Database (database.py) ]
              ├── plots Table (Indexed by plot_id, mouza, deed)
              └── transactions Table (Indexed by conflict_group)
```

- **Frontend:** HTML5, CSS3 with responsive mobile-friendly layouts, Bootstrap 5.3, Bootstrap Icons, and Vanilla JavaScript for checklist state persistence.
- **Backend:** Python 3.11 with Flask, providing robust routing, input sanitization, and graceful error handling.
- **Database:** Embedded SQLite with foreign key enforcement and indexed lookups for plot IDs, deed numbers, and mouza codes.
- **Rule Engine:** Modular, explainable Python engine evaluating 5 deterministic rules:
  1. `RULE_DUP_SALE`: Detects multiple active sale claims across differing deeds.
  2. `RULE_INCOMPLETE_RECORD`: Flags missing deeds, mutation records, or khatians.
  3. `RULE_REF_MISMATCH`: Identifies discrepancies between plot records and transfer logs.
  4. `RULE_UNKNOWN_CASE`: Warns of unverified civil litigation.
  5. `RULE_UNKNOWN_KHAS`: Explains unverified Khas or government acquisition status.
- **Testing:** Comprehensive pytest suite with Flask test client validating all routes, rules, and scenarios.

---

### 5. Main Features & Functionality

1. **Interactive Records Dashboard:**
   - Real-time statistics derived directly from SQLite (Total demo plots, review-required flags, duplicate-sale conflicts, incomplete records).
   - Multi-criteria filtering by review status and mutation status.
   - Client-side instant filter search.
2. **Plot Search Engine:**
   - Search by Plot ID (e.g., `PLOT-1004`), Khatian reference (`KH-DEMO-1001`), Deed reference (`DEED-DEMO-1002`), or Mouza code (`DEMO-MOUZA-01`).
   - Normalization of query terms with clean not-found guidance suggesting active demo plots.
3. **Comprehensive Plot Details & Chain of Title:**
   - Complete display of administrative metadata, deed/mutation references, and chronological transaction chains (distinguishing active vs. superseded transfers).
4. **Transparent Verification Warnings:**
   - Every triggered warning displays rule code, severity badge, explanation of the discrepancy, affected reference, and concrete recommended citizen action.
5. **Interactive 7-Point Due Diligence Checklist:**
   - Tracks deed verification, mutation examination, chain-of-title review, missing document audit, court litigation search, khas/acquisition check, and legal counsel engagement.
   - Live completion counter and progress bar saved in browser storage.
6. **Printable Pre-Purchase Summary Report:**
   - Print-optimized CSS (`@media print`) rendering a formal documentation summary with explicit synthetic disclaimers, signature blocks for purchasers, and advocate review notes.

---

### 6. Implementation Plan & Countrywide Scalability Considerations

To transition from an educational hackathon prototype to a national citizen utility, the following phased roadmap is envisioned:

- **Phase 1: Academic MVP & Feedback (Current):**
  - Demonstrate prototype at LandTech Innovation Hackathon 2026.
  - Gather feedback from legal experts, land surveyors (Amins), and real estate advocates.
- **Phase 2: Standardized Land Data Exchange Schema (LDES):**
  - Formulate open JSON schemas for land records to represent CS/SA/RS/BS khatians and deed metadata uniformly.
- **Phase 3: Digital Land Governance Integration (Future Vision):**
  - Interoperability via secure, read-only Government APIs:
    - *e-Mutation (e-Namjari):* Automated verification against Land Reform Board (LRB) databases.
    - *Sub-Registry Digital Archive:* Cross-referencing against Directorate of Registration volumes.
    - *Digital Land Map (Mouza Map):* Linking spatial boundary coordinates from DGLRS.
- **Phase 4: District-by-District Rollout & Civic Outreach:**
  - Pilot testing in designated upazilas to evaluate citizen adoption, literacy constraints, and mobile usability.

---

### 7. Limitations, Data Privacy & Ethical Considerations

- **Synthetic Data Boundary:** All 22 demonstration plots, khatian numbers, deed references, and mouza codes are 100% synthetic. No real personal identities, National ID (NID) numbers, biometric data, or actual land records are stored or processed.
- **No Scraping or Unauthorized Infiltration:** The project strictly complies with ethical guidelines; it does not scrape, crawl, or attempt unauthorized connections to government portals.
- **Non-Conclusive Legal Status:** The platform explicitly avoids terms like "Legally Safe", "Government Verified", or "Fraud Confirmed". It functions purely as an informational diligence aid.
- **Citizen Empowerment without Disintermediation:** The platform advises citizens to consult qualified advocates and licensed surveyors, reinforcing the established legal ecosystem.

---

### 8. Team & Mentor Information

- **Project Name:** BuyerGuard BD
- **Institution:** Daffodil International University (DIU), Bangladesh
- **Event:** LandTech Innovation Hackathon 2026
- **Track:** P5 — Citizen Pre-Purchase Verification (with P3 Fraud Detection)
- **Team Name:** [Insert Student Team Name]
- **Team Members:**
  - Member 1: [Student Name — Role / Student ID]
  - Member 2: [Student Name — Role / Student ID]
  - Member 3: [Student Name — Role / Student ID]
  - Member 4: [Student Name — Role / Student ID]
- **Faculty / Hackathon Mentor:** [Mentor Name, Designation, Department]
- **Repository:** `buyerguard-bd` (Local Workspace Repository)
