"""SQLite database manager for flat listings and viewing schedules."""

from pathlib import Path
import sqlite3

DB_PATH = Path(__file__).parent.parent / "listings.db"


def init_db():
    """Initializes the database table schema."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS listings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                address TEXT NOT NULL,
                phone TEXT NOT NULL,
                is_available INTEGER DEFAULT 1,
                available_from_date TEXT,
                bed_bath_count TEXT,
                pet_policy TEXT,
                furnishing_status TEXT,
                parking_available TEXT,
                asking_rent TEXT,
                negotiated_rent TEXT,
                deposit_amount TEXT,
                tour_confirmed INTEGER DEFAULT 0,
                agreed_tour_iso TEXT,
                tier_reached TEXT,
                concessions_granted TEXT,
                landlord_notes TEXT,
                recommended_action TEXT,
                called_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """
        )
        conn.commit()


def save_call_result(phone: str, address: str, result: dict):
    """Saves structured CALL-E agent result into SQLite."""
    init_db()
    outcome = result.get("negotiation_outcome", {})

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO listings (
                address, phone, is_available, available_from_date,
                bed_bath_count, pet_policy, furnishing_status, parking_available,
                asking_rent, negotiated_rent, deposit_amount,
                tour_confirmed, agreed_tour_iso, tier_reached,
                concessions_granted, landlord_notes, recommended_action
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                address,
                phone,
                1 if result.get("is_available") else 0,
                result.get("available_from_date"),
                result.get("bed_bath_count"),
                result.get("pet_policy"),
                result.get("furnishing_status"),
                result.get("parking_available"),
                result.get("asking_rent"),
                result.get("negotiated_rent"),
                result.get("deposit_amount"),
                1 if result.get("tour_confirmed") else 0,
                result.get("agreed_tour_iso"),
                outcome.get("tier_reached"),
                outcome.get("concessions_granted"),
                result.get("landlord_notes"),
                result.get("recommended_action"),
            ),
        )
        conn.commit()