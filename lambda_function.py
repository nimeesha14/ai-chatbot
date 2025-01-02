import json

def validate(slots):
    try:
        if not slots['Location']:
            print("Inside Empty Location")
            return {
                'isValid': False,
                'violatedSlot': 'Location'
            }
        
        if not slots['CheckInDate']:
            return {
                'isValid': False,
                'violatedSlot': 'CheckInDate'
            }
        
        if not slots['Nights']:
            return {
                'isValid': False,
                'violatedSlot': 'Nights'
            }
        
        if not slots['RoomType']:
            return {
                'isValid': False,
                'violatedSlot': 'RoomType'
            }
        if not slots['Confirmation']:
             return {
                'isValid': False,
                'violatedSlot': 'Confirmation'
            }
        
        if not slots['ThankYou']:
            return {
                'isValid': False,
                'violatedSlot': 'ThankYou'
            }
        
        return {'isValid': True}

    except Exception as e:
        print(f"Error during validation: {str(e)}")
        raise

def lambda_handler(event, context):
    try:
        print("Received event:", json.dumps(event, indent=2))  # For debugging purposes

        # Extract relevant information from the event
        slots = event['sessionState']['intent']['slots']
        intent = event['sessionState']['intent']['name']
        invocation_source = event['invocationSource']

        print(f"Invocation Source: {invocation_source}")
        print(f"Slots: {json.dumps(slots, indent=2)}")
        print(f"Intent: {intent}")

        if invocation_source == 'DialogCodeHook':
            validation_result = validate(slots)
            print(f"Validation Result: {validation_result}")
            
            if not validation_result['isValid']:
                # Elicit the missing slot
                response = {
                    "sessionState": {
                        "dialogAction": {
                            "type": "ElicitSlot",
                            "slotToElicit": validation_result['violatedSlot']
                        },
                        "intent": {
                            'name': intent,
                            'slots': slots,
                            'state': 'InProgress'
                        }
                    }
                }
                return response  
            response = {
                "sessionState": {
                    "dialogAction": {
                        "type": "Delegate"
                    },
                    "intent": {
                        'name': intent,
                        'slots': slots,
                        'state': 'InProgress'
                    }
                }
            }
            return response

        

    except Exception as e:
        print(f"Unhandled error: {str(e)}")
        return {
            "sessionState": {
                "dialogAction": {
                    "type": "Close",
                    "fulfillmentState": "Failed"
                },
                "intent": {
                    'name': intent,
                    'slots': slots,
                    'state': 'Failed'
                }
            },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": "Thank you.. You booking is successful."
                }
            ]
        }




