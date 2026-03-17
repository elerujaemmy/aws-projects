import json

# CPT codes that require prior authorization
AUTH_REQUIRED = {'27447', '44950', '99223', '93306'}

# Medicaid reimbursement rate
MEDICAID_RATE = 0.80

def handler(event, context):
    claim_id = event['claim_id']
    amount   = float(event['amount'])
    copay    = float(event.get('copay', 0.0))
    cpt_code = event.get('cpt_code', '')

    print(f"Calculating payment for {claim_id}: billed=${amount}, copay=${copay}")

    requires_auth = cpt_code in AUTH_REQUIRED
    approved_amount = round((amount - copay) * MEDICAID_RATE, 2)

    result = {
        **event,
        'approved_amount': approved_amount,
        'requires_auth':   requires_auth,
        'outcome':         'PENDING' if requires_auth else 'APPROVED',
    }

    print(f"Payment calculated: approved_amount=${approved_amount}, requires_auth={requires_auth}")
    return result