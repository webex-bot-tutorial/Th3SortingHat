from ldap3 import Server, Connection, ALL
import config

def bindServer():
	server = Server('ldap://ds.cisco.com:389', get_info=ALL)
	conn = Connection(server, config.username, config.password,  auto_bind=True)
	conn.open()
	conn.bind()
	return conn;

def searchMailer(conn, mailerName):
	conn.search(config.organizational_base, '(&(objectclass=*)('+mailerName+'))' , attributes=config.attributes)

	if len(conn.entries) < 1:
		conn.search(config.mailer_base, '(&(objectclass=*)('+mailerName+'))' , attributes=config.attributes)
	conn.search=0						
	return conn.entries;

def unbindServer(conn):
	conn.unbind()
	return;

def getMailer(MailerName):
	conn = bindServer()
	cec_list = []
	userList = searchMailer(conn, ("CN="+str(MailerName)))
	userList = userList[0]['member']
	for i in range(len(userList)):
		_ = userList[i]
		start = userList[i].index('=')
		start += 1
		end = userList[i].index(',')
		_ = _[start:end] + "@cisco.com"
		cec_list.append(_)
	unbindServer(conn)
	return cec_list;

def next_term_exists(in_list, indece):
	try:
		in_list[indece+1]
		return True
	except:
		return False

def get_all_people_from_mailer(MailerName):
	conn = bindServer()
	cec_list = []
	userList = searchMailer(conn, ("CN="+str(MailerName)))

	userList = userList[0]['member']

	mailer_list = []

	cec_list = []

	for i in range(len(userList)):
		start = userList[i].index('=')
		start += 1
		end = userList[i].index(',')
		new_data = userList[i][start:end]

		if ('.' in new_data):
			mailer_list.append(new_data)

		else:
			cec_list.append(new_data)

	# While the mailer_list is not empty:
	# run each mailer through until you get all the people

	while(len(mailer_list) > 0):
		conn = bindServer()
		mailer_contents = searchMailer(conn, ("CN="+str(mailer_list[0])))
		mailer_contents = mailer_contents[0]['member']

		for i in range(len(mailer_contents)):

			start = mailer_contents[i].index('=')
			start += 1
			end = mailer_contents[i].index(',')
			new_data = mailer_contents[i][start:end]

			if ('.' in new_data):
				mailer_list.append(new_data)
			else:
				cec_list.append(new_data)

			try:
				del mailer_list[0]
			except:
				None

	return cec_list

def makeEmail(text):
        text2 = text.split(",")
        text3 = text2[0]
        userName = (text3[3:]+"@cisco.com")
        return userName

def translate(strUlist):
        messyData = strUlist[(strUlist.index("member")+7):-1]
        noSpace = messyData.strip()
        print(noSpace)
        splitMessyData = noSpace.split()
        listMessyData =list(splitMessyData)
        myList = []
        for i in range(int(len(splitMessyData)/2)):
                email = makeEmail(splitMessyData[i*2])
                myList.append(email)
        return myList

def translateMailer(userlist):
	emailList = translate(userlist)
	return emailList
