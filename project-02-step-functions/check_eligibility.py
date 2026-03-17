import json

def handler(event, context):
    claim_id   = event['claim_id']
    plan_status = event['plan_status']

    print(f"Checking eligibility for {claim_id}, plan_status={plan_status}")

    if plan_status != 'ACTIVE':
        # Return eligible=False — Step Functions Choice state routes to DenyClaim
        return {**event, 'eligible': False, 'denial_reason': 'not_enrolled'}

    return {**event, 'eligible': True}