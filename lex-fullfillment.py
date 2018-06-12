import boto3


def close(request):
    slots = request["currentIntent"]["slots"]
    return {
        "dialogAction": {
        "type": "Close",
        "fulfillmentState": "Fulfilled",
        "message": {
            "contentType": "PlainText",
            "content": f'Thank you for that {slots["name"]} we will have your {slots["size"]} {slots["drink"]} ready shortly!'
            }
        }
    }


def send_notification(request):
    sns = boto3.client('sns')
    slots = request["currentIntent"]["slots"]
    response = sns.publish(
        TopicArn='arn:aws:sns:us-west-2:850991872567:lex-drink-bot',
        Message=f'{slots["name"]} would like a {slots["size"]} {slots["drink"]}',
        Subject='Drink Order',
    )
    return close(request)


def dispatch(intent_request):
    intent_name = intent_request['currentIntent']['name']
    if intent_name == 'GetDrinkOrder':
        return send_notification(intent_request)
    raise Exception('Intent with name ' + intent_name + ' not supported')


def lambda_handler(event, context):
    return dispatch(event)
