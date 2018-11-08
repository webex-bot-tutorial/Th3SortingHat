import requests
import config
import json
import os

bot_auth_token = config.bot_token

baseurl = "https://api.ciscospark.com/v1"

headers = {"Content-Type": "application/json",
           "accept": "application/json",
           "Authorization": "Bearer %s" % bot_auth_token
           }

def createRoom(name):
    URL = "https://api.ciscospark.com/v1/rooms"
    HEADERS = {"Content-type":"application/json;charset=utf-8", "Authorization": "Bearer " + bot_auth_token}
    PAYLOAD = {"title":name}

    r = requests.post(url=URL, json=PAYLOAD, headers=HEADERS)
    data = r.json()
    roomId = data['id']

    if(r.status_code == 200):
        print("'"+name+"' has been created!")
    else:
        print("Error making room.")
        print(r.status_code)
    return roomId, r.status_code

def delete_room(room_id):
    URL = "https://api.ciscospark.com/v1/rooms/"+str(room_id)
    HEADERS = {"Content-type":"application/json;charset=utf-8", "Authorization": "Bearer " + bot_auth_token}

    r = requests.delete(url=URL, headers=HEADERS)

    print(r.status_code)
    print(r.text)


def send_message(room, text):
    send_api = "/messages"
    send_url = baseurl + send_api
    send_data = {"roomId": room,
                 "text": text
                 }
    send_resp = requests.post(send_url,
                              headers=headers,
                              json=send_data)

    return send_resp.text

def send_message_markdown(room, text):
    send_api = "/messages"
    send_url = baseurl + send_api
    send_data = {"roomId": room,
                 "markdown": text
                 }
    send_resp = requests.post(send_url,
                              headers=headers,
                              json=send_data)

    return send_resp.text

def send_message_image(room, file):
    data = {
        "roomId": room
    }

    filetype = mimetypes.guess_type(file)[0]
    fname = os.path.abspath(file).rsplit(os.sep)[-1]
    data.update({'files': (fname, open(file, 'rb'), filetype)})
    multipart = MultipartEncoder(fields=data)
    r = requests.post('https://api.ciscospark.com/v1/messages',
                      headers={'Content-type': multipart.content_type,
                               'Authorization': "Bearer %s" % bot_auth_token },
                               data=multipart)
    return r

def send_message_image_text(room, file, message):
    data = {
        "roomId": room,
        "text": message
    }

    filetype = mimetypes.guess_type(file)[0]
    fname = os.path.abspath(file).rsplit(os.sep)[-1]
    data.update({'files': (fname, open(file, 'rb'), filetype)})
    multipart = MultipartEncoder(fields=data)
    r = requests.post('https://api.ciscospark.com/v1/messages',
                      headers={'Content-type': multipart.content_type,
                               'Authorization': "Bearer %s" % bot_auth_token },
                               data=multipart)
    return r

def get_message(mess_id):

    mess_api = "/messages/%s" % mess_id

    mess_url = baseurl + mess_api

    mess_resp = requests.get(url=mess_url, headers=headers)

    mess_r = mess_resp.json()

    message_info = mess_r['text']
    message_words = message_info.split()
    words_no_bot = message_words[1:]
    message_string = (" ").join(words_no_bot)
    return message_string

def getUsersinRoom(roomId):

    URL = "https://api.ciscospark.com/v1/memberships"
    HEADERS = {"Content-type":"application/json; charset=utf-8", "Authorization": "Bearer " + bot_auth_token}
    PARAMS = {"roomId":str(roomId)}

    r = requests.get(url=URL, params=PARAMS, headers=HEADERS )

    data = r.json()
    dataLoad = data['items']
    userList = []
    for i in range(len(dataLoad)):
        userList.append(dataLoad[i]['personEmail'])
    return userList

def get_person_info(cec):

    URL = "https://api.ciscospark.com/v1/people"

    if not("@" in cec):
        cec = str(cec)+"@cisco.com"

    PARAMS = {"email":str(cec)}
    HEADERS = {"Content-type":"application/json;charset=utf-8", "Authorization": "Bearer " + bot_auth_token}

    resp = requests.get(url=URL, params=PARAMS, headers=HEADERS )
    resp = resp.json()

    foo = resp['items'][0]['id']
    return foo

def addPeople(roomId, userList):

    URL = "https://api.ciscospark.com/v1/memberships"
    HEADERS = {"Content-type":"application/json;charset=utf-8", "Authorization": "Bearer " + bot_auth_token}

    for i in range(len(userList)):

        id = get_person_info(userList[i])

        PAYLOAD = {"roomId":roomId, "personId":id}

        r = requests.post(url=URL, json=PAYLOAD, headers=HEADERS)

def addPerson(roomId, userId):
    URL = "https://api.ciscospark.com/v1/memberships"
    HEADERS = {"Content-type":"application/json;charset=utf-8", "Authorization": "Bearer " + bot_auth_token}
    PAYLOAD = {"roomId":roomId, "personId":userId}
    r = requests.post(url=URL, json=PAYLOAD, headers=HEADERS)

    print("\n\n Request for adding someone: {}\n\n".format(r.status_code))
    print("\n\n Request for adding someone: {}\n\n".format(r.text))

def addMod(roomId, userId):
    URL = "https://api.ciscospark.com/v1/memberships"
    HEADERS = {"Content-type":"application/json;charset=utf-8", "Authorization": "Bearer " + bot_auth_token}
    PAYLOAD = {"roomId":roomId, "personId":userId, "isModerator": "true"}
    r = requests.post(url=URL, json=PAYLOAD, headers=HEADERS)

    print("\n\n Request for adding someone: {}\n\n".format(r.status_code))
    print("\n\n Request for adding someone: {}\n\n".format(r.text))

def removePeople(roomId, userList):

    URL = "https://api.ciscospark.com/v1/memberships/"
    HEADERS = {"Content-type":"application/json;charset=utf-8", "Authorization": "Bearer " + bot_auth_token}

    for i in range(len(userList)):

        # Get User Id
        id = get_person_info(userList[i])

        # Get Membership Id
        member_url = "https://api.ciscospark.com/v1/memberships"
        PARAMS = {'roomId':str(roomId), 'personEmail':str(userList[i])}
        r = requests.get(url=member_url, params=PARAMS, headers=HEADERS)

        mem_id = r.json()['items'][0]['id']

        del_URL = "https://api.ciscospark.com/v1/memberships/"+str(mem_id)

        r = requests.delete(url=del_URL, headers=HEADERS)

# Bot must be in the room for this to work
def getRoomID(roomName):
    URL = "https://api.ciscospark.com/v1/rooms"
    HEADERS = {"Content-type":"application/json;charset=utf-8", "Authorization": "Bearer " + bot_auth_token}
    r = requests.get(url=URL, headers=HEADERS)
    data = r.json()['items']

    roomMatch = []

    for i in range(len(data)):
        if data[i]['title'] == roomName:
            roomMatch.append(data[i]['id'])
    if len(roomMatch) == 0:
        return False
    else:
        return roomMatch

def check4Mod(roomId, personEmail):
    URL = "https://api.ciscospark.com/v1/memberships"
    HEADERS = {"Content-type":"application/json;charset=utf-8", "Authorization":"Bearer " + bot_auth_token}
    PARAMS = {"roomId":roomId, "personEmail": personEmail}

    r = requests.get(url=URL, headers=HEADERS, params=PARAMS)
    isMod = json.loads(r.text)['items'][0]['isModerator']
    return isMod, r.text

def get_mods(roomId):
    URL = "https://api.ciscospark.com/v1/memberships"
    HEADERS = {"Content-type":"application/json;charset=utf-8", "Authorization":"Bearer " + bot_auth_token}
    PARAMS = {"roomId": roomId}
    r = requests.get(url=URL, headers=HEADERS, params=PARAMS)
    people = json.loads(r.text)

    mods = []

    for i in range(len(people['items'])):
        print(people['items'][i]['isModerator'])
        print("\n")
        if (people['items'][i]['isModerator']):
            mods.append(people['items'][i]['personEmail'])

    return mods


def validMailer(mailerName):
    resp = ldap.getMailer(mailerName)
    if len(resp) <= 0:
        return False
