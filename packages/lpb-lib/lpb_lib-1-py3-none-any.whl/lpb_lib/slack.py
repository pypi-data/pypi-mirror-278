import json 
import requests

def sendMessageToSlack(slack_hook, color, title, value):
    """Send a message to a Slack channel using the specified webhook.

    :slack_hook: url of the Slack webhook.
    :color: The color of the message attachment (e.g., "#FF5733" or "good").
    :title: The title of the message attachment.
    :value: The value/content of the message attachment.
    """
    headers = {'content-type': 'application/json'}
    payload = {"attachments":[
                  {
                    "fallback":"",
                    "pretext":"",
                    "color":color,
                    "fields":[
                         {
                             "title":title,
                             "value":value,
                             "short": False
                          }
                       ]
                    }
                 ]
              }
    r = requests.post(slack_hook, data=json.dumps(payload), headers=headers)
    print("Response: " + str(r.status_code) + "," +  str(r.reason))
