"""
seed_data.py - Deterministic Synthetic Seed Data Generator
BuyerGuard BD — Smart Land Pre-Purchase Verification Platform

Populates SQLite database with 22 structured synthetic plot records and
associated transaction histories for testing and demonstration.
Never contains real personal, biometric, or actual government records.
"""

from typing import Optional
from database import get_db_connection, init_db


SAMPLE_PLOTS = [
    {
        "plot_id": "PLOT-1001",
        "demo_district": "Demo District A",
        "demo_upazila": "Demo Upazila 01",
        "demo_mouza_code": "DEMO-MOUZA-01",
        "khatian_ref": "KH-DEMO-1001",
        "deed_ref": "DEED-DEMO-1001",
        "mutation_status": "Mutated (Namjari Complete)",
        "case_info_status": "No Active Litigation Reported in Demo Records",
        "khas_acquisition_status": "Not Marked as Khas / Non-Acquired",
        "description": "Standard residential fictional plot with complete simulated documentation and continuous chain of title.",
    },
    {
        "plot_id": "PLOT-1002",
        "demo_district": "Demo District A",
        "demo_upazila": "Demo Upazila 01",
        "demo_mouza_code": "DEMO-MOUZA-01",
        "khatian_ref": "KH-DEMO-1002",
        "deed_ref": "DEED-DEMO-1002",
        "mutation_status": "Missing",
        "case_info_status": "No Active Litigation Reported in Demo Records",
        "khas_acquisition_status": "Not Marked as Khas / Non-Acquired",
        "description": "Fictional plot missing mutation (namjari) records; triggers incomplete record review.",
    },
    {
        "plot_id": "PLOT-1003",
        "demo_district": "Demo District A",
        "demo_upazila": "Demo Upazila 02",
        "demo_mouza_code": "DEMO-MOUZA-02",
        "khatian_ref": "KH-DEMO-1003",
        "deed_ref": None,
        "mutation_status": "Mutated (Namjari Complete)",
        "case_info_status": "No Active Litigation Reported in Demo Records",
        "khas_acquisition_status": "Not Marked as Khas / Non-Acquired",
        "description": "Synthetic plot without recorded primary deed reference; triggers record completeness warning.",
    },
    {
        "plot_id": "PLOT-1004",
        "demo_district": "Demo District B",
        "demo_upazila": "Demo Upazila 03",
        "demo_mouza_code": "DEMO-MOUZA-03",
        "khatian_ref": "KH-DEMO-1004",
        "deed_ref": "DEED-DEMO-1004-A",
        "mutation_status": "Mutated (Namjari Complete)",
        "case_info_status": "No Active Litigation Reported in Demo Records",
        "khas_acquisition_status": "Not Marked as Khas / Non-Acquired",
        "description": "Simulated double-selling conflict plot. Multiple active sale transactions exist with distinct deeds.",
    },
    {
        "plot_id": "PLOT-1005",
        "demo_district": "Demo District B",
        "demo_upazila": "Demo Upazila 03",
        "demo_mouza_code": "DEMO-MOUZA-03",
        "khatian_ref": "KH-DEMO-1005",
        "deed_ref": "DEED-DEMO-1005-MASTER",
        "mutation_status": "Mutated (Namjari Complete)",
        "case_info_status": "No Active Litigation Reported in Demo Records",
        "khas_acquisition_status": "Not Marked as Khas / Non-Acquired",
        "description": "Plot displaying reference discrepancy between plot master record and active transaction deed reference.",
    },
    {
        "plot_id": "PLOT-1006",
        "demo_district": "Demo District B",
        "demo_upazila": "Demo Upazila 04",
        "demo_mouza_code": "DEMO-MOUZA-04",
        "khatian_ref": "KH-DEMO-1006",
        "deed_ref": "DEED-DEMO-1006",
        "mutation_status": "Mutated (Namjari Complete)",
        "case_info_status": "Unknown / Pending Court Check",
        "khas_acquisition_status": "Not Marked as Khas / Non-Acquired",
        "description": "Synthetic plot where litigation information is unverified, prompting physical court checks.",
    },
    {
        "plot_id": "PLOT-1007",
        "demo_district": "Demo District C",
        "demo_upazila": "Demo Upazila 05",
        "demo_mouza_code": "DEMO-MOUZA-05",
        "khatian_ref": "KH-DEMO-1007",
        "deed_ref": "DEED-DEMO-1007",
        "mutation_status": "Mutated (Namjari Complete)",
        "case_info_status": "No Active Litigation Reported in Demo Records",
        "khas_acquisition_status": "Unknown / Pending Land Office Vetting",
        "description": "Synthetic plot with unverified Khas or acquisition status; prompts AC Land office verification.",
    },
    {
        "plot_id": "PLOT-1008",
        "demo_district": "Demo District C",
        "demo_upazila": "Demo Upazila 05",
        "demo_mouza_code": "DEMO-MOUZA-05",
        "khatian_ref": "KH-DEMO-1008",
        "deed_ref": "DEED-DEMO-1008",
        "mutation_status": "Missing",
        "case_info_status": "Unknown / Pending Court Check",
        "khas_acquisition_status": "Unknown / Pending Land Office Vetting",
        "description": "Multi-warning scenario combining missing mutation, unverified litigation, and unverified acquisition status.",
    },
    {
        "plot_id": "PLOT-1009",
        "demo_district": "Demo District A",
        "demo_upazila": "Demo Upazila 01",
        "demo_mouza_code": "DEMO-MOUZA-01",
        "khatian_ref": "KH-DEMO-1009",
        "deed_ref": "DEED-DEMO-1009-LATEST",
        "mutation_status": "Mutated (Namjari Complete)",
        "case_info_status": "No Active Litigation Reported in Demo Records",
        "khas_acquisition_status": "Not Marked as Khas / Non-Acquired",
        "description": "Clean residential plot with healthy 3-stage chronological chain: inheritance -> gift -> purchase. No duplicate conflict.",
    },
    {
        "plot_id": "PLOT-1010",
        "demo_district": "Demo District A",
        "demo_upazila": "Demo Upazila 02",
        "demo_mouza_code": "DEMO-MOUZA-02",
        "khatian_ref": "KH-DEMO-1010",
        "deed_ref": "DEED-DEMO-1010",
        "mutation_status": "Mutated (Namjari Complete)",
        "case_info_status": "No Active Litigation Reported in Demo Records",
        "khas_acquisition_status": "Not Marked as Khas / Non-Acquired",
        "description": "Commercial simulated plot with complete mutation and verified boundaries in synthetic dataset.",
    },
    {
        "plot_id": "PLOT-1011",
        "demo_district": "Demo District B",
        "demo_upazila": "Demo Upazila 03",
        "demo_mouza_code": "DEMO-MOUZA-03",
        "khatian_ref": "KH-DEMO-1011",
        "deed_ref": "DEED-DEMO-1011",
        "mutation_status": "Pending Mutation Application",
        "case_info_status": "No Active Litigation Reported in Demo Records",
        "khas_acquisition_status": "Not Marked as Khas / Non-Acquired",
        "description": "Agricultural demo plot with a mutation application currently under review at local land office.",
    },
    {
        "plot_id": "PLOT-1012",
        "demo_district": "Demo District B",
        "demo_upazila": "Demo Upazila 04",
        "demo_mouza_code": "DEMO-MOUZA-04",
        "khatian_ref": None,
        "deed_ref": "DEED-DEMO-1012",
        "mutation_status": "Not Provided",
        "case_info_status": "No Active Litigation Reported in Demo Records",
        "khas_acquisition_status": "Not Marked as Khas / Non-Acquired",
        "description": "Fictional plot missing khatian reference and mutation status.",
    },
    {
        "plot_id": "PLOT-1013",
        "demo_district": "Demo District C",
        "demo_upazila": "Demo Upazila 05",
        "demo_mouza_code": "DEMO-MOUZA-05",
        "khatian_ref": "KH-DEMO-1013",
        "deed_ref": "DEED-DEMO-1013",
        "mutation_status": "Mutated (Namjari Complete)",
        "case_info_status": "No Active Litigation Reported in Demo Records",
        "khas_acquisition_status": "Not Marked as Khas / Non-Acquired",
        "description": "Clean plot featuring two past superseded transfers and one active owner.",
    },
    {
        "plot_id": "PLOT-1014",
        "demo_district": "Demo District C",
        "demo_upazila": "Demo Upazila 06",
        "demo_mouza_code": "DEMO-MOUZA-06",
        "khatian_ref": "KH-DEMO-1014",
        "deed_ref": "DEED-DEMO-1014-X",
        "mutation_status": "Mutated (Namjari Complete)",
        "case_info_status": "No Active Litigation Reported in Demo Records",
        "khas_acquisition_status": "Not Marked as Khas / Non-Acquired",
        "description": "Duplicate sale test case: Two distinct deed claims recorded in parallel conflict group CONF-1014.",
    },
    {
        "plot_id": "PLOT-1015",
        "demo_district": "Demo District A",
        "demo_upazila": "Demo Upazila 01",
        "demo_mouza_code": "DEMO-MOUZA-01",
        "khatian_ref": "KH-DEMO-1015",
        "deed_ref": None,
        "mutation_status": "Missing",
        "case_info_status": "No Active Litigation Reported in Demo Records",
        "khas_acquisition_status": "Not Marked as Khas / Non-Acquired",
        "description": "High missing-data plot: lacking both primary registered deed and mutation records.",
    },
    {
        "plot_id": "PLOT-1016",
        "demo_district": "Demo District B",
        "demo_upazila": "Demo Upazila 03",
        "demo_mouza_code": "DEMO-MOUZA-03",
        "khatian_ref": "KH-DEMO-1016",
        "deed_ref": "DEED-DEMO-1016",
        "mutation_status": "Mutated (Namjari Complete)",
        "case_info_status": "No Active Litigation Reported in Demo Records",
        "khas_acquisition_status": "Unknown / Acquisition Notice Inquiry",
        "description": "Plot requiring inquiry at District Land Acquisition branch due to unverified demo acquisition status.",
    },
    {
        "plot_id": "PLOT-1017",
        "demo_district": "Demo District A",
        "demo_upazila": "Demo Upazila 02",
        "demo_mouza_code": "DEMO-MOUZA-02",
        "khatian_ref": "KH-DEMO-1017",
        "deed_ref": "DEED-DEMO-1017",
        "mutation_status": "Mutated (Namjari Complete)",
        "case_info_status": "No Active Litigation Reported in Demo Records",
        "khas_acquisition_status": "Not Marked as Khas / Non-Acquired",
        "description": "Complete benchmark plot with recent e-Namjari entry and clear title history.",
    },
    {
        "plot_id": "PLOT-1018",
        "demo_district": "Demo District C",
        "demo_upazila": "Demo Upazila 05",
        "demo_mouza_code": "DEMO-MOUZA-05",
        "khatian_ref": "KH-DEMO-1018",
        "deed_ref": "DEED-DEMO-1018-ALPHA",
        "mutation_status": "Mutated (Namjari Complete)",
        "case_info_status": "No Active Litigation Reported in Demo Records",
        "khas_acquisition_status": "Not Marked as Khas / Non-Acquired",
        "description": "Reference mismatch scenario: Plot table deed differs from registered transaction deed record.",
    },
    {
        "plot_id": "PLOT-1019",
        "demo_district": "Demo District B",
        "demo_upazila": "Demo Upazila 04",
        "demo_mouza_code": "DEMO-MOUZA-04",
        "khatian_ref": "KH-DEMO-1019",
        "deed_ref": "DEED-DEMO-1019",
        "mutation_status": "Mutated (Namjari Complete)",
        "case_info_status": "No Active Litigation Reported in Demo Records",
        "khas_acquisition_status": "Not Marked as Khas / Non-Acquired",
        "description": "Multi-heir synthetic plot with executed partition deed (Bontonnama) and verified shares.",
    },
    {
        "plot_id": "PLOT-1020",
        "demo_district": "Demo District A",
        "demo_upazila": "Demo Upazila 01",
        "demo_mouza_code": "DEMO-MOUZA-01",
        "khatian_ref": "KH-DEMO-1020",
        "deed_ref": "DEED-DEMO-1020",
        "mutation_status": "Mutated (Namjari Complete)",
        "case_info_status": "Unknown / Court Title Suit Check Required",
        "khas_acquisition_status": "Not Marked as Khas / Non-Acquired",
        "description": "Plot displaying unknown court litigation status; triggers cautionary legal check guidance.",
    },
    {
        "plot_id": "PLOT-1021",
        "demo_district": "Demo District C",
        "demo_upazila": "Demo Upazila 06",
        "demo_mouza_code": "DEMO-MOUZA-06",
        "khatian_ref": "KH-DEMO-1021",
        "deed_ref": "DEED-DEMO-1021",
        "mutation_status": "Mutated (Namjari Complete)",
        "case_info_status": "No Active Litigation Reported in Demo Records",
        "khas_acquisition_status": "Not Marked as Khas / Non-Acquired",
        "description": "Complete demo plot in Mouza 06 with clean historical title chain.",
    },
    {
        "plot_id": "PLOT-1022",
        "demo_district": "Demo District B",
        "demo_upazila": "Demo Upazila 03",
        "demo_mouza_code": "DEMO-MOUZA-03",
        "khatian_ref": "KH-DEMO-1022",
        "deed_ref": "DEED-DEMO-1022",
        "mutation_status": "Pending Mutation Application",
        "case_info_status": "Unknown / Title Check Required",
        "khas_acquisition_status": "Unknown / Vetting Required",
        "description": "Industrial zone demo plot with pending mutation and unverified status flags.",
    },
]

SAMPLE_TRANSACTIONS = [
    # PLOT-1001: Clean Single Active Transaction
    {
        "plot_id": "PLOT-1001",
        "transaction_ref": "TX-1001-01",
        "deed_ref": "DEED-DEMO-1001",
        "transaction_type": "Sale",
        "transaction_date": "2021-04-12",
        "record_status": "Active",
        "conflict_group_id": None,
    },
    # PLOT-1002: Active Transaction but missing mutation
    {
        "plot_id": "PLOT-1002",
        "transaction_ref": "TX-1002-01",
        "deed_ref": "DEED-DEMO-1002",
        "transaction_type": "Sale",
        "transaction_date": "2022-08-19",
        "record_status": "Active",
        "conflict_group_id": None,
    },
    # PLOT-1003: Transaction has deed but plot master is missing it
    {
        "plot_id": "PLOT-1003",
        "transaction_ref": "TX-1003-01",
        "deed_ref": "DEED-DEMO-1003-SUPP",
        "transaction_type": "Sale",
        "transaction_date": "2020-01-15",
        "record_status": "Active",
        "conflict_group_id": None,
    },
    # PLOT-1004: Intentionally Conflicting Active Sale Claims (Double Selling Simulation)
    {
        "plot_id": "PLOT-1004",
        "transaction_ref": "TX-1004-CLAIM-A",
        "deed_ref": "DEED-DEMO-1004-A",
        "transaction_type": "Sale",
        "transaction_date": "2023-02-10",
        "record_status": "Active",
        "conflict_group_id": "CONF-1004",
    },
    {
        "plot_id": "PLOT-1004",
        "transaction_ref": "TX-1004-CLAIM-B",
        "deed_ref": "DEED-DEMO-1004-B",
        "transaction_type": "Simulated Duplicate Sale",
        "transaction_date": "2023-05-18",
        "record_status": "Active",
        "conflict_group_id": "CONF-1004",
    },
    # PLOT-1005: Inconsistent Deed Reference (Plot is MASTER, Tx is ALT)
    {
        "plot_id": "PLOT-1005",
        "transaction_ref": "TX-1005-01",
        "deed_ref": "DEED-DEMO-1005-ALT",
        "transaction_type": "Sale",
        "transaction_date": "2022-11-04",
        "record_status": "Active",
        "conflict_group_id": None,
    },
    # PLOT-1006: Clean Tx, unknown case
    {
        "plot_id": "PLOT-1006",
        "transaction_ref": "TX-1006-01",
        "deed_ref": "DEED-DEMO-1006",
        "transaction_type": "Sale",
        "transaction_date": "2019-06-25",
        "record_status": "Active",
        "conflict_group_id": None,
    },
    # PLOT-1007: Clean Tx, unknown khas
    {
        "plot_id": "PLOT-1007",
        "transaction_ref": "TX-1007-01",
        "deed_ref": "DEED-DEMO-1007",
        "transaction_type": "Sale",
        "transaction_date": "2020-09-30",
        "record_status": "Active",
        "conflict_group_id": None,
    },
    # PLOT-1008: Multi-warning Tx
    {
        "plot_id": "PLOT-1008",
        "transaction_ref": "TX-1008-01",
        "deed_ref": "DEED-DEMO-1008",
        "transaction_type": "Sale",
        "transaction_date": "2021-03-14",
        "record_status": "Active",
        "conflict_group_id": None,
    },
    # PLOT-1009: Legitimate Historical Chain (3 stages: Inheritance 2012 -> Gift 2018 -> Purchase 2022)
    # Must NOT trigger duplicate-sale warning because older ones are 'Superseded'
    {
        "plot_id": "PLOT-1009",
        "transaction_ref": "TX-1009-H1",
        "deed_ref": "DEED-DEMO-1009-HIST1",
        "transaction_type": "Inheritance",
        "transaction_date": "2012-05-10",
        "record_status": "Superseded",
        "conflict_group_id": None,
    },
    {
        "plot_id": "PLOT-1009",
        "transaction_ref": "TX-1009-H2",
        "deed_ref": "DEED-DEMO-1009-HIST2",
        "transaction_type": "Gift (Heba)",
        "transaction_date": "2018-09-12",
        "record_status": "Superseded",
        "conflict_group_id": None,
    },
    {
        "plot_id": "PLOT-1009",
        "transaction_ref": "TX-1009-ACT",
        "deed_ref": "DEED-DEMO-1009-LATEST",
        "transaction_type": "Sale",
        "transaction_date": "2022-12-01",
        "record_status": "Active",
        "conflict_group_id": None,
    },
    # PLOT-1010
    {
        "plot_id": "PLOT-1010",
        "transaction_ref": "TX-1010-01",
        "deed_ref": "DEED-DEMO-1010",
        "transaction_type": "Sale",
        "transaction_date": "2021-07-20",
        "record_status": "Active",
        "conflict_group_id": None,
    },
    # PLOT-1011
    {
        "plot_id": "PLOT-1011",
        "transaction_ref": "TX-1011-01",
        "deed_ref": "DEED-DEMO-1011",
        "transaction_type": "Purchase",
        "transaction_date": "2023-01-11",
        "record_status": "Active",
        "conflict_group_id": None,
    },
    # PLOT-1012
    {
        "plot_id": "PLOT-1012",
        "transaction_ref": "TX-1012-01",
        "deed_ref": "DEED-DEMO-1012",
        "transaction_type": "Sale",
        "transaction_date": "2020-04-18",
        "record_status": "Active",
        "conflict_group_id": None,
    },
    # PLOT-1013: 2 superseded + 1 active
    {
        "plot_id": "PLOT-1013",
        "transaction_ref": "TX-1013-OLD",
        "deed_ref": "DEED-DEMO-1013-OLD",
        "transaction_type": "Sale",
        "transaction_date": "2015-06-10",
        "record_status": "Superseded",
        "conflict_group_id": None,
    },
    {
        "plot_id": "PLOT-1013",
        "transaction_ref": "TX-1013-CURR",
        "deed_ref": "DEED-DEMO-1013",
        "transaction_type": "Sale",
        "transaction_date": "2022-03-22",
        "record_status": "Active",
        "conflict_group_id": None,
    },
    # PLOT-1014: Duplicate Sale Simulation
    {
        "plot_id": "PLOT-1014",
        "transaction_ref": "TX-1014-CLAIM-1",
        "deed_ref": "DEED-DEMO-1014-X",
        "transaction_type": "Sale",
        "transaction_date": "2023-04-05",
        "record_status": "Active",
        "conflict_group_id": "CONF-1014",
    },
    {
        "plot_id": "PLOT-1014",
        "transaction_ref": "TX-1014-CLAIM-2",
        "deed_ref": "DEED-DEMO-1014-Y",
        "transaction_type": "Simulated Duplicate Sale",
        "transaction_date": "2023-06-18",
        "record_status": "Active",
        "conflict_group_id": "CONF-1014",
    },
    # PLOT-1016
    {
        "plot_id": "PLOT-1016",
        "transaction_ref": "TX-1016-01",
        "deed_ref": "DEED-DEMO-1016",
        "transaction_type": "Sale",
        "transaction_date": "2021-10-10",
        "record_status": "Active",
        "conflict_group_id": None,
    },
    # PLOT-1017: Clean benchmark
    {
        "plot_id": "PLOT-1017",
        "transaction_ref": "TX-1017-01",
        "deed_ref": "DEED-DEMO-1017",
        "transaction_type": "Sale",
        "transaction_date": "2022-05-14",
        "record_status": "Active",
        "conflict_group_id": None,
    },
    # PLOT-1018: Mismatch
    {
        "plot_id": "PLOT-1018",
        "transaction_ref": "TX-1018-01",
        "deed_ref": "DEED-DEMO-1018-BETA",
        "transaction_type": "Sale",
        "transaction_date": "2022-08-08",
        "record_status": "Active",
        "conflict_group_id": None,
    },
    # PLOT-1019
    {
        "plot_id": "PLOT-1019",
        "transaction_ref": "TX-1019-PART",
        "deed_ref": "DEED-DEMO-1019",
        "transaction_type": "Partition (Bontonnama)",
        "transaction_date": "2020-11-20",
        "record_status": "Active",
        "conflict_group_id": None,
    },
    # PLOT-1020
    {
        "plot_id": "PLOT-1020",
        "transaction_ref": "TX-1020-01",
        "deed_ref": "DEED-DEMO-1020",
        "transaction_type": "Sale",
        "transaction_date": "2021-02-15",
        "record_status": "Active",
        "conflict_group_id": None,
    },
    # PLOT-1021: Clean
    {
        "plot_id": "PLOT-1021",
        "transaction_ref": "TX-1021-01",
        "deed_ref": "DEED-DEMO-1021",
        "transaction_type": "Sale",
        "transaction_date": "2023-01-28",
        "record_status": "Active",
        "conflict_group_id": None,
    },
    # PLOT-1022
    {
        "plot_id": "PLOT-1022",
        "transaction_ref": "TX-1022-01",
        "deed_ref": "DEED-DEMO-1022",
        "transaction_type": "Purchase",
        "transaction_date": "2022-07-04",
        "record_status": "Active",
        "conflict_group_id": None,
    },
]


def seed_database(db_path: Optional[str] = None) -> None:
    """Insert seed plots and transactions idempotently."""
    init_db(db_path)
    conn = get_db_connection(db_path)
    try:
        cur = conn.cursor()
        for p in SAMPLE_PLOTS:
            cur.execute("""
                INSERT INTO plots (
                    plot_id, demo_district, demo_upazila, demo_mouza_code,
                    khatian_ref, deed_ref, mutation_status, case_info_status,
                    khas_acquisition_status, description
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(plot_id) DO UPDATE SET
                    demo_district = excluded.demo_district,
                    demo_upazila = excluded.demo_upazila,
                    demo_mouza_code = excluded.demo_mouza_code,
                    khatian_ref = excluded.khatian_ref,
                    deed_ref = excluded.deed_ref,
                    mutation_status = excluded.mutation_status,
                    case_info_status = excluded.case_info_status,
                    khas_acquisition_status = excluded.khas_acquisition_status,
                    description = excluded.description;
            """, (
                p["plot_id"],
                p["demo_district"],
                p["demo_upazila"],
                p["demo_mouza_code"],
                p["khatian_ref"],
                p["deed_ref"],
                p["mutation_status"],
                p["case_info_status"],
                p["khas_acquisition_status"],
                p["description"],
            ))

        # Clear existing transactions before inserting deterministically
        cur.execute("DELETE FROM transactions;")
        for t in SAMPLE_TRANSACTIONS:
            cur.execute("""
                INSERT INTO transactions (
                    plot_id, transaction_ref, deed_ref, transaction_type,
                    transaction_date, record_status, conflict_group_id
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                t["plot_id"],
                t["transaction_ref"],
                t["deed_ref"],
                t["transaction_type"],
                t["transaction_date"],
                t["record_status"],
                t["conflict_group_id"],
            ))
        conn.commit()
    finally:
        conn.close()


if __name__ == "__main__":
    print("Seeding BuyerGuard BD database...")
    seed_database()
    print("Database seeding completed successfully.")
