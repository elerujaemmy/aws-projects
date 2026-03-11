import json
import boto3
import os

s3  = boto3.client('s3')
sns = boto3.client('sns')

SNS_APPROVED = os.environ['SNS_APPROVED']
SNS_DENIED   = os.environ['SNS_DENIED']
SNS_PENDING  = os.environ['SNS_PENDING']

TOPIC_MAP = {
    'APPROVED': SNS_APPROVED,
    'DENIED':   SNS_DENIED,
    'PENDING':  SNS_PENDING,
}

def handler(event, context):
    # EventBridge wraps the S3 event - extract bucket and key
    detail = event.get('detail', {})
    bucket = detail.get('bucket', {}).get('name')
    key    = detail.get('object', {}).get('key')

    if not bucket or not key:
        raise ValueError(f"Missing bucket/key in event: {json.dumps(event)}")

    # Read the claim JSON from S3
    response = s3.get_object(Bucket=bucket, Key=key)
    claim    = json.loads(response['Body'].read())

    claim_id = claim.get('claim_id')
    amount   = claim.get('amount')
    status   = claim.get('status')

    # Validate required fields
    if not claim_id or amount is None or not status:
        raise ValueError(f"Missing required fields: claim_id={claim_id}, amount={amount}, status={status}")

    if status not in TOPIC_MAP:
        raise ValueError(f"Unknown status '{status}' — must be APPROVED, DENIED, or PENDING")

    # Route to the correct SNS topic
    topic_arn = TOPIC_MAP[status]
    sns.publish(
        TopicArn=topic_arn,
        Subject=f"Claim {status}: {claim_id}",
        Message=f"Claim ID: {claim_id}\nStatus: {status}\nAmount: ${amount:.2f}",
    )

    print(f"Routed {claim_id} → {status} (${amount:.2f})")
    return {'statusCode': 200, 'claimId': claim_id, 'status': status}
