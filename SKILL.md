## Prerequisites
- **CALL-E SDK:** `pip install calle-ai`
- **API Key:** `CALLE_API_KEY` exported in environment variables
- **Phone Formatting:** Targets must be formatted in valid E.164 syntax (e.g., `+14155552671` or `+919876543210`).

## Conversational Strategy & Rules
1. **Persona:** Courteous, direct, and pragmatic buyer's representative.
2. **Context Discovery:** State call purpose immediately (referencing the property address/listing).
3. **Availability Gate:** Confirm if the property is actively available. If already rented, conclude gracefully to conserve call budget.
4. **Terms Verification:** Verify monthly rent, security deposit, utility inclusions, and pet constraints.
5. **Viewing Scheduling:** If terms meet the tenant's profile, negotiate available tour slots for the next 24–48 hours.

## Standard Execution Interface

To run a single pre-screening task:

```bash
python -m src.domain.agent_runner