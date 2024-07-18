# from celery import shared_task
# from alerts_api.models import Alert
# import json
# import importlib

# @shared_task
# def process_alert_notification(alert_id):
#     """
#     Worker task
#     """
#     alert_instance = Alert.objects.get(pk=alert_id)
#     matching_rule = find_matching_rule(alert_instance)
#     if matching_rule:
#         send_notifications(alert_instance, matching_rule)

# def find_matching_rule(alert):
#     """
#     Find the first matching rule for the given alert.
#     """
#     rules = load_rules_from_file('notification_config/rules.json')  # Implement a function to read rules from the file
#     for rule in rules:
#         if evaluate_rule(alert, rule):
#             return rule

#     return None

# def load_rules_from_file(file_path):
#     """
#     Read rules in json
#     """
#     with open(file_path, 'r') as file:
#         rules = json.load(file)

#     # Convert the JSON structure to a dictionary list
#     converted_rules = []
#     for rule in rules:
#         converted_rule = {
#             'source': rule.get('source', 'Any'),
#             'location': rule.get('location', 'Any'),
#             'severity': rule.get('severity', 'Any'),
#             'targets': rule.get('targets', [])
#         }
#         converted_rules.append(converted_rule)

#     return converted_rules

# def evaluate_rule(alert, rule):
#     """
#     Evaluate if the alert matches the given rule.
#     """
#     source_match = rule['source'] == 'Any' or alert.source == rule['source']
#     location_match = rule['location'] == 'Any' or alert.location == rule['location']
#     severity_match = rule['severity'] == 'Any' or alert.severity == rule['severity']

#     return source_match and location_match and severity_match

# def send_notifications(alert, rule):
#     """
#     Send the notifications to the right targets
#     """
#     for target in rule['targets']:
#         try:
#             target_name = target.get('name')
#             if target_name:
#                 # Dynamically import the notification module
#                 module_path = f'alerts_notificator.notification_modules.{target_name}'
#                 notification_module = importlib.import_module(module_path)

#                 # Get additional parameters from the target dictionary
#                 additional_params = target.get('additional_params', {})

#                 # Call the send_notification function from the module with additional parameters
#                 getattr(notification_module, 'send_notification')(alert, **additional_params)
#             else:
#                 print("Target name not specified in the rule.")
            
#         except ImportError:
#             print(f"Unsupported target: {target}")
#         except AttributeError:
#             print(f"Method 'send_notification' not found in module for target: {target}")


from celery import shared_task
from alerts_api.models import Alert
import json
import importlib

@shared_task
def process_alert_notification(alert_id):
    """
    Worker task
    """
    alert_instance = Alert.objects.get(pk=alert_id)
    with open('notification_config/rules.json', 'r') as file:
        rules = json.load(file)
 
    for rule in rules:
        if evaluate_and_send_notification(alert_instance, rule):
            break  # Break after the first matching rule

def evaluate_and_send_notification(alert, rule):
    """
    Evaluate if the alert matches the given rule and send the notification.
    Return True if a notification is sent, otherwise False.
    """
    source_match = rule['source'] == 'Any' or alert.source == rule['source']
    location_match = rule['location'] == 'Any' or alert.location == rule['location']
    severity_match = rule['severity'] == 'Any' or alert.severity == rule['severity']

    if source_match and location_match and severity_match:
        for target in rule.get('targets', []):
            try:
                target_name = target.get('name')
                if target_name:
                    # Dynamically import the notification module
                    module_path = f'alerts_notificator.notification_modules.{target_name}'
                    notification_module = importlib.import_module(module_path)

                    # Get additional parameters from the target dictionary
                    additional_params = target.get('additional_params', {})

                    # Call the send_notification function from the module with additional parameters
                    getattr(notification_module, 'send_notification')(alert, **additional_params)
                else:
                    print("Target name not specified in the rule.")

            except ImportError:
                print(f"Unsupported target: {target}")
            except AttributeError:
                print(f"Method 'send_notification' not found in module for target: {target}")

        return True
    
    return False
