import json

REQUIRED_FIELDS = ['claim_id', 'cpt_code', 'diagnosis_code', 'amount', 'plan_status']
VALID_STATUSES  = {'ACTIVE', 'INACTIVE', 'TERMINATED'}

def handler(event, context):
    print(f"Validating claim: {json.dumps(event)}")

    # Check required fields
    missing = [f for f in REQUIRED_FIELDS if f not in event]
    if missing:
        raise ValueError(f"Missing required fields: {missing}")

    # Validate amount
    amount = event['amount']
    if not isinstance(amount, (int, float)):
        raise ValueError(f"amount must be a number, got: {type(amount)}")
    if amount < 0:
        raise ValueError(f"amount cannot be negative: {amount}")

    # Validate plan_status is a known value
    if event['plan_status'] not in VALID_STATUSES:
        raise ValueError(f"Unknown plan_status: {event['plan_status']}")

    print(f"Validation passed for claim {event['claim_id']}")
    return event  # pass full claim downstream