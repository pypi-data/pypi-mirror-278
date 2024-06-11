# README #
This package contains utilities which you may use to easily interact with Konverso Kbot application. 
 
In particular, you may:

* Invoke some of the APIs to view / update / create Kbot configuration objects such as Intents, Message, etc.
* Collect metrics showing how the bot is performing.
* Create a Conversation and interact with it, sending message and getting responses

# See also #

## Access Konverso Support
You may contact us: 

* For any commercial inquiry: contact@konverso.ai
* For support: https://konverso.atlassian.net/servicedesk/customer/portals

## Alliance for Open ChatBot
Alternatively, you may also connect using the standard Alliance for Open Chatbot APIs to any Konverso bot: 
See a ready to use python package: https://github.com/konverso-ai/open-chatbot-py-client
 
### Installation ###

You may use pip3 to install the software on your Kbot instance: 

First Navigate to your work-area and then invoke: 

	pip3 install -e git+https://konverso@bitbucket.org/konversoai/kbot-py-client.git#egg=kbot-py-client

# Usage #

You would typically first need to login and then invoke some of the API wrapped methods.

## Login ##

	import json
	
	from kbot_client import Client
	
	cli = Client("mybot.konverso.ai")
	cli.login("myuser", "mysecretpassword")
	

## Collect metrics ##
Once authenticated, you can for example retrieve useful usage metrics, these can be used by a Monitoring application or for some business intelligence rendering: 

	metrics = cli.metric().json()
	print("Collected metrics:")
	print(json.dumps(metrics, indent=4))
	
## Retrieve object details ##
You may retrieve list of defined objects. Note that only objects visibled to the logged in users will be returned.

Here is a sample code that simply checks for a few objects existance: 

# Get list of objects and check if object with name is present in response
	for unit, name in (('intention' ,'Create ticket'),
	                   ('knowledge_base', 'faq'),
	                   ('workflow', 'Transfer to Agent')):
    	print(f"Get list of '{unit}'")
    	objs = cli.unit(unit)
    	if objs:
        	# Create dict with
        	# - key : object name
        	# - value : object json data
        	data = {obj['name']: obj for obj in objs}
        	if name in data:
            	print(f"'{name}' is present")
        	else:
            	print(f"'{name}' is not present")
    	else:
        	print("Get no data")
		
## Conversation test
In this example, we create a conversation between the logged in user and the bot and then sends a sentence, and check if we get some expected text in the response. This could for example be the basis of automated testing of the bot

    	r = cli.conversation(username='bot')
    	if r.status_code == 201:
    	    cid = r.json().get('id')
    	    print("Created conversation with id '%s'" %(cid,))

    	    response = cli.message(cid, 'hello')

    	    # Process bot response
    	    if response:
    	        for resp in response:
    	            for message in resp.get('message', []):
    	                responses.append(message.get('value', '')) # dict {message type: message value}
    	                resp_message = '\n'.join(responses)
                        print("Received response: ", resp_message)
                        if 'I am kbot' in resp_message:
                            print("Excepted response found")
                            break
                    else:
                        print("Did not receive the expected response")
    	    else:
    	        print("Did not receive any response")
    	else:
    	    print("Could not create conversation due to: ", r.text)
	
## Uploading a batch of files to the file manager

### Prerequisites

* An API key
* The UUID of the folder that will receive the files you want to upload

### Code sample
In this example, we simply upload the content of a directory to a folder in the file manager.

        from kbot_client import Client
        from kbot_client.folder_sync import FolderSync

        client = Client("mybot.konverso.ai", api_key="17ebXXXXXXXXXXXXXXXXXXXXX")

        syncer = FolderSync(client)
        syncer.sync("/tmp/my_source_folder/", "1831fXXXXXXXXXXXXXXXXXXXXXXX")
        print("Syncing is done :)")
