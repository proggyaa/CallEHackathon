"""JSON schema definition for CALL-E prescreen agent responses."""

PRESCREEN_RESULT_SCHEMA = {
    "type": "object",
    "required": [
        "is_available",
        "asking_rent",
        "negotiated_rent",
        "deposit_amount",
        "tour_confirmed",
        "recommended_action",
    ],
    "properties": {
        "is_available": {"type": "boolean"},
        "available_from_date": {
            "type": "string",
            "description": "Move-in ready date or immediate",
        },
        "bed_bath_count": {
            "type": "string",
            "description": "Layout details e.g. 2 Bed / 2 Bath",
        },
        "pet_policy": {"type": "string", "description": "Pet policy details"},
        "furnishing_status": {
            "type": "string",
            "description": "Furnished, Semi-Furnished, or Unfurnished",
        },
        "parking_available": {
            "type": "string",
            "description": "Parking details (garage, street, included)",
        },
        "asking_rent": {"type": "string", "description": "Original listing rent"},
        "negotiated_rent": {"type": "string", "description": "Final agreed monthly rent"},
        "deposit_amount": {"type": "string", "description": "Security deposit required"},
        "tour_confirmed": {"type": "boolean"},
        "agreed_tour_iso": {
            "type": "string",
            "description": "ISO timestamp of agreed slot if tour_confirmed is true",
        },
        "negotiation_outcome": {
            "type": "object",
            "properties": {
                "tier_reached": {
                    "type": "string",
                    "enum": [
                        "tier_1_discount",
                        "tier_2_target",
                        "tier_3_concessions",
                        "failed",
                    ],
                },
                "landlord_accepted_counter": {"type": "boolean"},
                "concessions_granted": {
                    "type": "string",
                    "description": "Details on waived fees, included utilities, or lowered deposit",
                },
            },
        },
        "landlord_notes": {"type": "string"},
        "recommended_action": {
            "type": "string",
            "enum": ["book_tour", "reject_terms", "manual_followup"],
        },
    },
}