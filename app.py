from flask import Flask, request, jsonify
import boto3
import json

app = Flask(__name__)

# Initialize SQS client
sqs = boto3.client('sqs', region_name='us-east-1', endpoint_url='http://localhost:4566')

# Your SQS queue URL
QUEUE_URL = 'http://localhost:4566/000000000000/my-queue'

# Dummy token for validation
VALID_TOKEN = "$DJISA<$#45ex3RtYr"

def validate_token(token):
    return token == VALID_TOKEN

def validate_payload(data):
    required_fields = ["email_subject", "email_sender", "email_timestream", "email_content"]
    return all(field in data for field in required_fields)

@app.route('/process', methods=['POST'])
def process_request():
    content = request.json
    token = content.get("token")
    data = content.get("data")

    if not validate_token(token):
        return jsonify({"error": "Invalid token"}), 403

    if not validate_payload(data):
        return jsonify({"error": "Invalid payload"}), 400

    response = sqs.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody=json.dumps(data)
    )

    return jsonify({"message": "Message sent to SQS", "message_id": response['MessageId']}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)