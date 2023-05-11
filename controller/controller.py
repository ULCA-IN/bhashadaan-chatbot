from flask import Flask, jsonify, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from configs.credentials import account_sid,auth_token
from repo.repo import Repository
from service.service import Service
from werkzeug.datastructures import CombinedMultiDict, ImmutableMultiDict
from configs.config import intro_string

app = Flask(__name__)

client = Client(account_sid, auth_token)

# telegram_bot = telebot.TeleBot(telegram_auth_token)
# telegram_bot.infinity_polling()

service = Service()
repo = Repository()

@app.route('/bot',methods=['POST'])
def whatsapp_bot():
    incoming_msg = request.values.get('Body', '').lower()
    print("Request : ",request.values)
    print("Message : ",incoming_msg)
    print(type(incoming_msg))
    resp = MessagingResponse()
    msg = resp.message()
    responded = False

    if 'MediaContentType0' in request.values.keys():
        phone_number = request.values.get("From")
        phone_number = phone_number.replace("whatsapp:+","")
        audio_url = request.values.get('MediaUrl0')
        submitted = False
        print("AUDIO URL: ",request.values.get('MediaUrl0'))
        response = service.get_search_entry(phone_number)
        print("Response:",response)
        if response is not None and "content" in response[0].keys():
            for each_entry in response[0]['content']:
                if each_entry['submitted'] == False:
                    function_response = service.make_submit_true(phone_number,audio_url)
                    if function_response is not None:
                        username = "W_8133751499"
                        #username = "W_"+phone_number[-10:]
                        message = service.submit_audio(audio_url,each_entry['language_code'],each_entry['dataset_row_id'],username)
                        print("Submit Audio Function Response: ",message)
                        if message is not None:
                            submitted = True
                        else: 
                            msg.body("Unable to submit the audio at this moment. Please try again later")
                            responded = True
                        break
                    else:
                        msg.body("Unable to perform the operation. Kindly try again later")
                        responded = True
        if response == None or submitted == False:
            if responded == False:
                msg.body("Please select a language to obtain text and then respond with the audio.\n\n"+intro_string)
            responded = True
        if responded == False:
            msg.body("Success!!! Thanks for contrubution your audio to Bhashadhaan. To continue contributing, choose a language again. For more details, visit: https://bhashini.gov.in/bhashadaan")
            responded = True

    if responded == False:
        input_msg = service.get_number_of_input(incoming_msg)
        if input_msg is not None and input_msg in range(1,11):
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
        msg.body(intro_string)
    return str(resp)

