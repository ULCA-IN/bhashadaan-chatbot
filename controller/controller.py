from flask import Flask, jsonify, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from configs.credentials import account_sid,auth_token
from repo.repo import Repository
from service.service import Service
from werkzeug.datastructures import CombinedMultiDict, ImmutableMultiDict

app = Flask(__name__)

client = Client(account_sid, auth_token)

service = Service()
repo = Repository()

@app.route('/bot',methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    print("Request : ",request.values)
    print("Message : ",incoming_msg)
    resp = MessagingResponse()
    msg = resp.message()
    responded = False

    if 'MediaContentType0' in request.values.keys():
        phone_number = request.values.get("From")
        phone_number = phone_number.replace("whatsapp:+","")
        audio_url = request.values.get('MediaUrl0')
        print("AUDIO URL: ",request.values.get('MediaUrl0'))
        response = service.get_search_entry(phone_number)
        if "response" is not None and "content" in response[0].keys():
            for each_entry in response[0]['content']:
                if each_entry['submitted'] == False:
                    function_response = service.make_submit_true(phone_number,audio_url)
                    if function_response is not None:
                        service.submit_audio(audio_url,each_entry['language_code'],each_entry['dataset_row_id'])
                        break
                    else:
                        msg.body("Unable to perform the operation. Kindly try again later")
        else:
            msg.body("Unable to perform the operation. Kindly try again later")
        responded = True
        msg.body("Success!!! Thanks for contrubutiong your audio to Bhashadhaan. To continue contributing, choose a language again. For more details, visit: https://bhashini.gov.in/bhashadaan")

    if incoming_msg=='1':
        function_response, dataset_row_id = service.send_sentence(incoming_msg)
        if dataset_row_id is not None: 
            phone_number = request.values.get("From")
            phone_number = phone_number.replace("whatsapp:+","")
            response = service.get_search_entry(phone_number,dataset_row_id,"contribute",incoming_msg,delete_submitted=True,updateEntry=True)
            if response is None:
                entry = {"_id":phone_number,
                        "content":[
                            {
                                    'taskOperation' : 'contribute',
                                    'dataset_row_id' : dataset_row_id,
                                    'language_code': service.get_language_from_code(incoming_msg),
                                    'submitted': False
                            }
                        ]
                        }
                repo.create_entry(entry)
        msg.body(function_response)
        responded = True

    if incoming_msg=='2':
        function_response, dataset_row_id = service.send_sentence(incoming_msg)
        if dataset_row_id is not None: 
            phone_number = request.values.get("From")
            phone_number = phone_number.replace("whatsapp:+","")
            response = service.get_search_entry(phone_number,dataset_row_id,"contribute",incoming_msg,delete_submitted=True,updateEntry=True)
            if response is None:
                entry = {"_id":phone_number,
                        "content":[
                            {
                                    'taskOperation' : 'contribute',
                                    'dataset_row_id' : dataset_row_id,
                                    'language_code': service.get_language_from_code(incoming_msg),
                                    'submitted': False
                            }
                        ]
                        }
                repo.create_entry(entry)
        msg.body(function_response)
        responded = True

    if incoming_msg=='3':
        function_response, dataset_row_id = service.send_sentence(incoming_msg)
        if dataset_row_id is not None: 
            phone_number = request.values.get("From")
            phone_number = phone_number.replace("whatsapp:+","")
            response = service.get_search_entry(phone_number,dataset_row_id,"contribute",incoming_msg,delete_submitted=True,updateEntry=True)
            if response is None:
                entry = {"_id":phone_number,
                        "content":[
                            {
                                    'taskOperation' : 'contribute',
                                    'dataset_row_id' : dataset_row_id,
                                    'language_code': service.get_language_from_code(incoming_msg),
                                    'submitted': False
                            }
                        ]
                        }
                repo.create_entry(entry)
        msg.body(function_response)
        responded = True

    if incoming_msg=='4':
        function_response, dataset_row_id = service.send_sentence(incoming_msg)
        if dataset_row_id is not None: 
            phone_number = request.values.get("From")
            phone_number = phone_number.replace("whatsapp:+","")
            response = service.get_search_entry(phone_number,dataset_row_id,"contribute",incoming_msg,delete_submitted=True,updateEntry=True)
            if response is None:
                entry = {"_id":phone_number,
                        "content":[
                            {
                                    'taskOperation' : 'contribute',
                                    'dataset_row_id' : dataset_row_id,
                                    'language_code': service.get_language_from_code(incoming_msg),
                                    'submitted': False
                            }
                        ]
                        }
                repo.create_entry(entry)
        msg.body(function_response)
        responded = True

    if not responded:
        msg.body(""" Hello User , welcome to Bolo India. Choose a number and select a language to start contributing.\n
                *1* : हिंदी
                *2* : தமிழ்
                *3* : తెలుగు
                *4* : മലയാളം
                """)
    return str(resp)
