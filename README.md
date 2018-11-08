# Th3SortingHat

 This is a repository for anyone who wants to make a Chatbot that leverages DialogFlow. This is also an example of how to make a chatbot in python 3.6.

## Installation

Use the package manager pip to install the following dependencies:

* Flask
* Requests
* Ldap3

 ## app.py

 This is the file that you would run in order to start the app. Most of the interaction comes from two if/elif blocks. These are triggered depending on the name of the Webhook that is pinging the code. If the bot is added to the room, 'membership_webhook' should ping app.py. If someone talks to the bot, 'messages_webhook' should ping app.py. If you add any intents to the code, make sure that your always return '', else your ngrok will constantly give a 500 error.

## dialog_flow.py

Dialog_flow.py serves two functions: To start a conversation and to get the intent of a user during said conversation. The sessionId is generated based upon the id of the spark room that the conversation takes place in.

make_dialog_call is the function that actually makes a call to dialog flow. It has the capacity to support multiple languages.

## ldap.py

ldap.py is an example of how to query active directory via ldap. This file requires credentials in order to used and is meant for internal Cisco use.

## update_webhooks.py

update_webhooks.py is a file that makes updating webhooks a whole lot easier. In the main function, the names of the webhooks that are being used, as well as their corresponding id's need to be added in main().

'new_url' is the new forwarding address for the bot. If you use ngrok to host the bot locally, you would set new_url equal to the new link. App.py requires /bot_main to be added onto whatever the forwarding address is. This is taken care of under update_webhooks() and can be changed if needed.

## Webex_Teams.py

Webex_Teams.py is a file that is meant to make interacting with the webex teams API easier. There is a lot of functionality that has been built in, and all that is needed is an authorization token. There are other libraries similar to this available at a github repo called Spark-API-Demos.

## Contributing

If there is any functionality that one feels is lacking or anything that could be explained better, feel free to submit a pull request or send me an email. My cec is esylvial.

Since I am currently interning, I may go back to school which would result in my technical termination. While my account may not be terminated, I might be a bit slow at responding. :)


## License

[MIT](https://choosealicense.com/licenses/mit/)
