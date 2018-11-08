import requests
from config import bot_auth_token

### How to update webhooks

def get_webhooks():
    URL = "https://api.ciscospark.com/v1/webhooks"
    HEADERS = {"Content-type":"application/json;charset=utf-8", "Authorization":"Bearer " + bot_auth_token}

    r = requests.get(url=URL, headers=HEADERS)
    data = r.json()

    webhook_info = []

    for i in range(len(data['items'])):
        webhook_dict = {}

        webhook_dict['id'] = data['items'][i]['id']
        webhook_dict['name'] = data['items'][i]['name']
        webhook_dict['resource'] = data['items'][i]['resource']
        webhook_dict['targetUrl'] = data['items'][i]['targetUrl']

        webhook_info.append(webhook_dict)

    return webhook_info

def update_webhooks(webhook_info, url):

    # For Sorting Hat
    url += "/bot_main"

    for i in range(len(webhook_info)):

        URL = "https://api.ciscospark.com/v1/webhooks/"+str(webhook_info[i]['id'])
        HEADERS = {"Content-type":"application/json;charset=utf-8", "Authorization":"Bearer " + bot_auth_token}
        PARAMS = {
        "name":webhook_info[i]['name'],
        "targetUrl":str(url)
        }

        r = requests.put(url=URL, json=PARAMS, headers=HEADERS)
        data = r.json()

        if (r.status_code != 200):
            print("Error:\n\n{}".format(data))
            break

    print("Success")


def main():

    # Put the Webhook Names Here
    webhook_names = []

    # Put the Webhook Id's Here
    webhooks_ids = []

    # Put the new forwarding address here (address that you get from ngrok):

    new_url = ""

    webhook_info = get_webhooks()

    update_webhooks(webhook_info, new_url)

    # Ping And Get All Webhooks that the bot is connected to
    # Copy their names and what resources they are related to
    # Change the url

# main()
