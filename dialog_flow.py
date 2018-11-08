import requests
import config
import Webex_Teams as spark

# Session that is created to track the state
# of the conversation
def make_session_id(spark_room_id):
    num = len(spark_room_id)-66
    id = spark_room_id[-15:]
    counter = 0
    for i in range(13):
        number = counter + i
        id += str(number)
    return id

# Contacts Dialog Flow, sends the text session, and langauge
# Receives a response, where the response is the intent of the user
# Returns the name of the intent of the user

def make_dialog_call(input_text, spark_room_id, room_added, language='en'):
    base_url = "https://api.dialogflow.com/v1/"
    post_url = "https://api.dialogflow.com/v1/query?v=20150910"
    CLIENT_ACCESS_TOKEN = config.CLIENT_ACCESS_TOKEN

    HEADERS = {
               "Authorization": "Bearer %s" % CLIENT_ACCESS_TOKEN,
                "Content-Type": "application/json"
               }

    message = input_text

    sessionId = make_session_id(spark_room_id)

    spark_room = sessionId

    PAYLOAD = {
        "lang":language,
        "query":str(message),
        "sessionId":str(spark_room),
        "timezone":"America/San_Jose"
    }

    r = requests.post(url=post_url, json=PAYLOAD, headers=HEADERS)

    response_text = r.json()

    try:

        if (response_text['result']['metadata']['intentName'] == 'Default Welcome Intent'):

            spark.send_message(room_added, response_text['result']['fulfillment']['speech'])

        else:
            return response_text['result']['metadata']['intentName']

    except:

        spark.send_message(room_added, str(response_text))

        if (response_text['result']['source'] == 'domains'):
            print("\nExcept\n")
            spark.send_message(room_added, str(response_text['result']['fulfillment']['speech']))
