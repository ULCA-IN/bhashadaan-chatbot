import telebot
from configs.credentials import telegram_auth_token
from service.service import Service
from repo.repo import Repository
import uuid

bot = telebot.TeleBot(telegram_auth_token)

service = Service()
repo = Repository()

# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Hello User , welcome to Bolo India. Choose a number and select a language to start contributing.\n
                1 : हिंदी
                2 : தமிழ்
                3 : తెలుగు
                4 : മലയാളം\
""")


@bot.message_handler(func=lambda incoming_message: True)
def echo_message(incoming_message):
    input = incoming_message.text
    responded = False
    print("INCOMING MESSAGE : ",incoming_message)
    if input=='1':
        function_response, dataset_row_id = service.send_sentence(input)
        if dataset_row_id is not None: 
            phone_number = str(incoming_message.from_user.id)
            #phone_number = phone_number.replace("whatsapp:+","")
            response = service.get_search_entry(phone_number,dataset_row_id,"contribute",input,delete_submitted=True,updateEntry=True)
            if response is None:
                entry = {"_id":phone_number,
                        "content":[
                            {
                                    'taskOperation' : 'contribute',
                                    'dataset_row_id' : dataset_row_id,
                                    'language_code': service.get_language_from_code(input),
                                    'submitted': False
                            }
                        ]
                        }
                repo.create_entry(entry)
        bot.reply_to(incoming_message, function_response)
        responded = True

    if input=='2':
        function_response, dataset_row_id = service.send_sentence(input)
        if dataset_row_id is not None: 
            phone_number = str(incoming_message.from_user.id)
            #phone_number = phone_number.replace("whatsapp:+","")
            response = service.get_search_entry(phone_number,dataset_row_id,"contribute",input,delete_submitted=True,updateEntry=True)
            if response is None:
                entry = {"_id":phone_number,
                        "content":[
                            {
                                    'taskOperation' : 'contribute',
                                    'dataset_row_id' : dataset_row_id,
                                    'language_code': service.get_language_from_code(input),
                                    'submitted': False
                            }
                        ]
                        }
                repo.create_entry(entry)
        bot.reply_to(incoming_message, function_response)
        responded = True

    if input=='3':
        function_response, dataset_row_id = service.send_sentence(input)
        if dataset_row_id is not None: 
            phone_number = str(incoming_message.from_user.id)
            #phone_number = phone_number.replace("whatsapp:+","")
            response = service.get_search_entry(phone_number,dataset_row_id,"contribute",input,delete_submitted=True,updateEntry=True)
            if response is None:
                entry = {"_id":phone_number,
                        "content":[
                            {
                                    'taskOperation' : 'contribute',
                                    'dataset_row_id' : dataset_row_id,
                                    'language_code': service.get_language_from_code(input),
                                    'submitted': False
                            }
                        ]
                        }
                repo.create_entry(entry)
        bot.reply_to(incoming_message, function_response)
        responded = True

    if input=='4':
        function_response, dataset_row_id = service.send_sentence(input)
        if dataset_row_id is not None: 
            phone_number = str(incoming_message.from_user.id)
            #phone_number = phone_number.replace("whatsapp:+","")
            response = service.get_search_entry(phone_number,dataset_row_id,"contribute",input,delete_submitted=True,updateEntry=True)
            if response is None:
                entry = {"_id":phone_number,
                        "content":[
                            {
                                    'taskOperation' : 'contribute',
                                    'dataset_row_id' : dataset_row_id,
                                    'language_code': service.get_language_from_code(input),
                                    'submitted': False
                            }
                        ]
                        }
                repo.create_entry(entry)
        bot.reply_to(incoming_message, function_response)
        responded = True

@bot.message_handler(content_types=['voice'])
def voice_processing(incoming_message):
    responded = False
    submitted = False
    phone_number = str(incoming_message.from_user.id)
    file_info = bot.get_file(incoming_message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    fid  = str(uuid.uuid4())
    oggfname = fid+".ogg"
    with open(oggfname, 'wb') as new_file:
        new_file.write(downloaded_file)
        print("FILE_PATH:",file_info.file_path)
        response = service.get_search_entry(phone_number)
        if response is not None and "content" in response[0].keys():
            for each_entry in response[0]['content']:
                if each_entry['submitted'] == False:
                    function_response = service.make_submit_true(phone_number,oggfname)
                    if function_response is not None:
                        service.submit_audio(oggfname,each_entry['language_code'],each_entry['dataset_row_id'],phone_number,"file")
                        submitted = True
                        break
                    else:
                        bot.reply_to(incoming_message, "Unable to perform the operation. Kindly try again later")
                        responded = True
        if response == None or submitted == False:
            bot.reply_to(incoming_message, "Please select a lanaguage to obtain text and then respond with the audio")
            responded = True
        if responded == False:
            bot.reply_to(incoming_message, "Success!!! Thanks for contrubutiong your audio to Bhashadhaan. To continue contributing, choose a language again. For more details, visit: https://bhashini.gov.in/bhashadaan")


# # Handle all other messages with content_type 'text' (content_types defaults to ['text'])
# @bot.message_handler(func=lambda message: True)
# def echo_message(message):
#     print(message)
#     bot.reply_to(message, message.text)

# @bot.message_handler(content_types=['photo'])
# def photo(message):
#     print(message)
#     fileID = message.photo[-1].file_id
#     file_info = bot.get_file(fileID)
#     downloaded_file = bot.download_file(file_info.file_path)

#     with open("image.jpg", 'wb') as new_file:
#         new_file.write(downloaded_file)
# @bot.message_handler(content_types=['voice'])
# def voice_processing(message):
#     file_info = bot.get_file(message.voice.file_id)
#     downloaded_file = bot.download_file(file_info.file_path)
#     with open('new_file.ogg', 'wb') as new_file:
#         new_file.write(downloaded_file)
        
bot.infinity_polling()