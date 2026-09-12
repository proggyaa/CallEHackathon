from pathlib import Path

PROMPT_TEMPLATE_PATH = (
    Path(__file__).parent.parent / "prompts" / "prescreen_task_en.txt"
)


def build_prescreen_prompt(
    phone: str,
    address: str,
    max_budget: str,
    max_deposit: str,
    slot_1: str,
    slot_2: str,
    must_haves: str = "None strictly required",
    negotiables: str = "None specified"
) -> str:
    """Loads and formats the external prompt template with runtime variables."""
    if not PROMPT_TEMPLATE_PATH.exists():
        raise FileNotFoundError(
            f"Prompt template missing at {PROMPT_TEMPLATE_PATH}"
        )

    template = PROMPT_TEMPLATE_PATH.read_text(encoding="utf-8")
    return template.format(
        phone=phone,
        address=address,
        max_budget=max_budget,
        max_deposit=max_deposit,
        slot_1=slot_1,
        slot_2=slot_2,
        must_haves=must_haves,
        negotiables=negotiables
    )