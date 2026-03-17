import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')
TABLE    = os.environ.get('DYNAMODB_TABLE', 'claims-workflow-state')

def handler(event, context):
    claim_id        = event['claim_id']
    outcome         = event.get('outcome', 'APPROVED')
    approved_amount = event.get('approved_amount', 0.0)
    denial_reason   = event.get('denial_reason', '')
    requires_auth   = event.get('requires_auth', False)

    print(f"Notifying outcome for {claim_id}: {outcome}, approved_amount=${approved_amount}")

    # Write final state to DynamoDB
    table = dynamodb.Table(TABLE)
    table.put_item(Item={
        'claim_id':        claim_id,
        'outcome':         outcome,
        'approved_amount': str(approved_amount),
        'denial_reason':   denial_reason,
        'requires_auth':   requires_auth,
        'cpt_code':        event.get('cpt_code', ''),
        'diagnosis_code':  event.get('diagnosis_code', ''),
        'plan_status':     event.get('plan_status', ''),
    })

    print(f"DynamoDB updated for {claim_id}")
    return {
        'statusCode':      200,
        'claim_id':        claim_id,
        'outcome':         outcome,
        'approved_amount': approved_amount,
    }