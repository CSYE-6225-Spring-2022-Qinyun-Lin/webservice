import boto3
import time
import json
from uuid import uuid4


def send_validation(email_address):
    sns_client = boto3.client('sns', region_name='us-east-1')
    dynamodb_table = boto3.resource('dynamodb', region_name='us-east-1')

    token = uuid4()
    item = {"UserId": email_address, "token": token, "ExpireTime": int(time.time() + 300), "sendStatus": "Not sent"}
    message = "{\"email\": \"%s\", \"token\": \"%s\", \"message_type\": \"validation\"}" % (email_address, str(token))

    try:
        dynamodb_table.put_item(Item=item)
        sns_client.publish(TopicArn='arn:aws:sns:us-east-1:399550114864:sns-topic-for-lambda',
                           Message=message)
        return True
    except Exception:
        return False


def verify_token(email_address, token):
    dynamodb_table = boto3.resource('dynamodb', region_name='us-east-1')
    response = dynamodb_table.get_item(Key={"UserId": email_address})
    if "Item" in response.keys():
        item = response['Item']
        true_token = item['token']
        if true_token == token:
            return True
    return False


if __name__ == '__main__':
    table = boto3.resource('dynamodb',
                           region_name='us-east-1',
                           aws_access_key_id="AKIAV2BYK5QYDSJUTQXO",
                           aws_secret_access_key="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"
                           ).Table('csye6225-token')

    email_address = "linqinyun@outlook.com"
    token = str(uuid4())
    item = {"UserId": email_address, "token": token, "ExpireTime": int(time.time() + 300), "sendStatus": "Not sent"}
    message = "{\"email\": \"%s\", \"token\": \"%s\", \"message_type\": \"validation\"}" % (email_address, str(token))
    message = json.loads(message)
    # print(message)

    # response = table.put_item(Item=item)
    # print(response)

    client = boto3.client('sns',
                          region_name='us-east-1',
                          aws_access_key_id="AKIAV2BYK5QYDSJUTQXO",
                          aws_secret_access_key="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")
    res = client.publish(TopicArn='arn:aws:sns:us-east-1:399550114864:sns-topic-for-lambda',
                         Message=message)
    print(res)
