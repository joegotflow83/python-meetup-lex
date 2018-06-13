def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ElicitSlot',
            'intentName': intent_name,
            'slots': slots,
            'slotToElicit': slot_to_elicit,
            'message': message
        }
    }


def confirm_intent(session_attributes, intent_name, slots, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ConfirmIntent',
            'intentName': intent_name,
            'slots': slots,
            'message': message
        }
    }


def delegate(session_attributes, slots):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Delegate',
            'slots': slots
        }
    }


def close(session_attributes, fulfillment_state, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillmentState,
            'message': message
        }
    }


def validate_size(session_attributes, slots):
    size = slots['size']
    if size.lower() not in ['small', 'medium', 'large']:
        message = {"contentType": "PlainText", "content": "Sorry, that is not an appropiate size. Please choose small, medium, or large."}
        return elicit_slot(session_attributes, 'GetDrinkOrder', slots, 'size', message)
    return delegate(session_attributes, slots)


def get_drink_order(request):
    session_attributes = {}
    slots = request["currentIntent"]["slots"]
    confirmation_status = request['currentIntent']['confirmationStatus']
    if request["invocationSource"] == 'DialogCodeHook':
        if not slots['size']:
            message = {"contentType": "PlainText", "content": "What size would you like?"}
            return elicit_slot(session_attributes, 'GetDrinkOrder', slots, 'size', message)
        else:
            return validate_size(session_attributes, slots)
        if not slots['name']:
            message = {"contentType": "PlainText", "content": "May I have a name for the order?"}
            return elicit_slot(session_attributes, 'GetDrinkOrder', slots, 'name', message)
        elif slots['size'] and slots['drink'] and slots['name']:
            return delegate(session_attributes, slots)
        else:
            message = {"contentType": "PlainText", "content": "I'm sorry, I did not understand what you said. Could you repeat that?"}
            return elicit_slot(session_attributes, 'GetDrinkOrder', slots, 'drink', message)
    return delegate(session_attributes, slots)


def dispatch(intent_request):
    intent_name = intent_request['currentIntent']['name']
    if intent_name == 'GetDrinkOrder':
        return get_drink_order(intent_request)
    raise Exception('Intent with name ' + intent_name + ' not supported')


def lambda_handler(event, context):
    return dispatch(event)
