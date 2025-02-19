import json
import boto3
import os
from datetime import datetime

# Initialize DynamoDB
DYNAMODB_TABLE = os.environ.get("DYNAMODB_TABLE", "GolfScores")
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(DYNAMODB_TABLE)

def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))
        player = body.get("player")
        hole = body.get("hole")
        score = body.get("score")
        
        if not player or not hole or not score:
            return {"statusCode": 400, "body": json.dumps("Missing required fields.")}
        
        # Store data in DynamoDB
        response = table.put_item(
            Item={
                "player": player,
                "hole": int(hole),
                "score": int(score),
                "timestamp": datetime.utcnow().isoformat()
            }
        )
        
        return {"statusCode": 200, "body": json.dumps("Score saved successfully.")}
    
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps(str(e))}
