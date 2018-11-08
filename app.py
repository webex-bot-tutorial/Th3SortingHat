import os
import config
import dialog_flow
import Webex_Teams as teams
from flask import Flask, jsonify
from flask import request
from flask import make_response

app = Flask(__name__)

baseurl = "https://api.ciscospark.com/v1"

bot_auth_token = config.bot_token

bot_id = config.spark_bot_id

headers = {"Content-Type": "application/json",
           "accept": "application/json",
           "Authorization": "Bearer %s" % bot_auth_token
           }

@app.route('/bot_main', methods=['GET','POST'])
def bot_main():

    # print("hello world")

    spark_hook = request.json

    room_added = str(spark_hook["data"]["roomId"])

    hook_data = spark_hook["data"]

    sessionid = 0

    ###Code that creates greeting message
    if (str(spark_hook['name']) == 'membership_webhook') and (hook_data["personId"] == bot_id):

        teams.send_message(room_added, "Hello There! I've been added to a room!")

    elif ((str(spark_hook['name']) == 'messages_webhook') and (hook_data["personId"] != bot_id)):

        input_text = mess_content = teams.get_message(hook_data['id'])

        if (len(input_text) == 0):
            return ''

        sessionid = dialog_flow.make_session_id(hook_data["personId"])

        # Send query to DF:
        intent_name = dialog_flow.make_dialog_call(input_text, sessionid, room_added)

        # Put your intent_name here!
        if (intent_name == "example"):

            teams.send_message(room_added, "Hello World!")

            return ''

if (__name__ == '__main__'):
    port = int(os.getenv('PORT', 8080))
    print("Starting App on port %d " %(port))
    # app.run(debug=True, port=port, host="0.0.0.0")
    app.run(debug=True, port=port, host="localhost")
