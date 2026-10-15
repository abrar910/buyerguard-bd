# BuyerGuard BD — 3-Minute Demonstration Video Script
**LandTech Innovation Hackathon 2026**  
**Daffodil International University, Bangladesh**  
**Track:** P5 — Citizen Pre-Purchase Verification (with P3 Fraud Detection)

---

### Timing Breakdown (Total Duration: 3 Minutes / 180 Seconds)

| Timestamp | Segment | Visual On Screen | Narration / Presenter Action |
|---|---|---|---|
| **0:00 – 0:35** | **The Problem in Bangladesh** | Landing page (`/`) showing hero banner and tagline "Check Before You Buy." | "Assalamu Alaikum and greetings judges. In Bangladesh, buying land is one of the biggest financial decisions a citizen can make — yet it carries enormous risks. Title deeds are kept at Sub-Registry offices, but mutation and revenue records are at Upazila AC Land offices. When these records don't align, buyers fall victim to double-selling fraud or buy unmutated land with broken chains of title. To solve this, our team created **BuyerGuard BD — Smart Land Pre-Purchase Verification Platform**." |
| **0:35 – 1:00** | **Live Records Dashboard** | Navigate to `/dashboard`. Highlight 4 stat cards calculated from SQLite. | "Here on the Live Dashboard, we see statistics calculated directly from our local SQLite database and deterministic rule engine. Out of 22 synthetic demonstration plots, the system automatically detects plots requiring review, incomplete records, and critical duplicate-sale conflicts. Users can filter by mutation status or review status, and instantly search visible records." |
| **1:00 – 1:50** | **Search & Double-Selling Detection** | Type `PLOT-1004` into search bar, hit verify, navigate to `/plots/PLOT-1004`. | "Let's test an intentionally simulated conflict: `PLOT-1004`. As we open the plot details, our explainable rule engine immediately triggers a prominent red alert: **'Potential Duplicate-Sale Inconsistency Detected' (`RULE_DUP_SALE`)**. Looking below at the simulated transaction history, we see two conflicting active sale claims filed under the same conflict group with different deed numbers! The engine does not make arbitrary guesses; it clearly explains *which* deeds conflict, *why* it is dangerous, and advises the buyer to conduct an urgent Sub-Registry Balam book search before paying earnest money." |
| **1:50 – 2:20** | **Citizen Due Diligence Checklist** | Scroll to the interactive checklist on the right sidebar. Check items 1, 2, and 3. | "On the right, BuyerGuard BD provides an interactive 7-point Citizen Pre-Purchase Checklist tailored for Bangladesh land practices: inspecting deeds at the Sub-Registry, checking e-Namjari porchas, tracing Bia deeds through CS, SA, RS, and BS surveys, and verifying civil court litigation. As the user checks items, the progress bar updates smoothly to '3 of 7 Completed', and the state is automatically persisted in their browser's local storage." |
| **2:20 – 2:45** | **Printable Diligence Report** | Click **'View Printable Summary'** (`/plots/PLOT-1004/report`). Click **'Print Summary'**. | "Once the citizen finishes their pre-purchase review, they can click 'View Printable Summary'. This loads a clean, print-formatted due diligence report. It includes all plot identifiers, completeness metrics, explainable warnings, transaction history, and purchaser/advocate signature lines. Notice our explicit disclaimer: *'Synthetic Demonstration Record — Not an Official Government Document.'* Citizens can take this physical report directly to their legal counsel or Sub-Registry search." |
| **2:45 – 3:00** | **Conclusion & Ethical Scope** | Return to Home page. Highlight clean code and zero external dependencies. | "BuyerGuard BD runs 100% locally on Python, Flask, SQLite, and vanilla web standards with no external API fees or cloud dependencies. While it is an academic prototype using fictional data, it demonstrates how transparent digital tools can empower ordinary Bangladeshi citizens with the knowledge to **Check Before They Buy**. Thank you!" |

---

### Presenter Preparation Checklist:
- [ ] Ensure local web server is running: `python app.py` (accessible at `http://127.0.0.1:5000`).
- [ ] Have browser open at `http://127.0.0.1:5000/`.
- [ ] Test the demo flow once beforehand to ensure seamless transitions.
- [ ] Keep speech clear, confident, and adhere strictly to the 3-minute limit.
