import telebot
from configs.credentials import telegram_auth_token
from service.service import Service
from repo.repo import Repository
import uuid
from configs.config import dekho_validate_string
import shutil
import requests
from PIL import Image
from io import BytesIO
from math import ceil
import os

bot = telebot.TeleBot(telegram_auth_token)

service = Service()
repo = Repository()

username = "Telegram_Bot"

# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message,dekho_validate_string)


@bot.message_handler(func=lambda incoming_message: True)
def echo_message(incoming_message):
    input = incoming_message.text
    responded = False
    print("INCOMING MESSAGE : ",incoming_message)
    if service.get_number_of_input(input) is not None:
        function_response = service.fetch_ocr(service.get_language_from_code(input),username)
        if function_response is not None: 
            phone_number = str(incoming_message.from_user.id)
            #(dataset_row_id, contribution, contribution_id, image_url)
            dataset_row_id = function_response[0] #Original Image ID
            contribution = function_response[1] #Text
            contribution_id = function_response[2] #Text ID
            image_url = function_response[3] #URL of Image
            #phone_number = phone_number.replace("whatsapp:+","")
            response = service.get_search_entry(phone_number,dataset_row_id,contribution,contribution_id,image_url,"validate",input,delete_submitted=True,updateEntry=True)
            if response is None:
                entry = {"_id":phone_number,
                        "content":[
                            {
                                "submitted": False,
                                "dataset_row_id": dataset_row_id,
                                "contribution": contribution,
                                "contribution_id": contribution_id,
                                "image_url": image_url,
                                "language_code": service.get_language_from_code(input),
                                "taskOperation": 'validate'
                            }
                        ]
                        }
                repo.create_entry(entry)
            try: 
                #Figure out 
                basewidth = 1000
                response = requests.get(image_url)
                img = Image.open(BytesIO(response.content))
                width,height = img.size
                wpercent = (basewidth/float(img.size[0]))
                hsize = int((float(img.size[1])*float(wpercent)))
                img = img.resize((basewidth,hsize), Image.Resampling.LANCZOS)
                width,height = img.size
                newH = ceil(width/20)
                padded = Image.new('RGB', (width,newH), 'black')
                padded.paste(img, (0,int((newH-height)/2)))
                padded.save("Img"+phone_number+".jpg")
                bot.send_photo(incoming_message.chat.id, photo=open("Img"+phone_number+".jpg", 'rb'))
                os.remove("Img"+phone_number+".jpg")
                del response
                bot.reply_to(incoming_message, contribution)
                responded = True

            except Exception as e:
                print(e)
    
    if input.lower() == "yes" or input.lower() == "no":
        submitted = False
        phone_number = str(incoming_message.from_user.id)
        if input.lower() == "yes":
            pass
        if input.lower() == "no":
            pass
            # new_file.write(downloaded_file)
            # print("FILE_PATH:",file_info.file_path)
            # response = service.get_search_entry(phone_number)
            # if response is not None and "content" in response[0].keys():
            #     for each_entry in response[0]['content']:
            #         if each_entry['submitted'] == False:
            #             function_response = service.make_submit_true(phone_number,oggfname)
            #             if function_response is not None:
            #                 username = "T_"+phone_number
            #                 message = service.submit_audio(oggfname,each_entry['language_code'],each_entry['dataset_row_id'],username,"file")
            #                 if message is not None:
            #                     submitted = True
            #                 else:
            #                     bot.reply_to(incoming_message, "Unable to submit the audio at this moment. Please try again later")
            #                     responded = True
            #                 break
            #             else:
            #                 bot.reply_to(incoming_message, "Unable to perform the operation. Kindly try again later")
            #                 responded = True
            # if response == None or submitted == False:
            #     if responded == False:
            #         bot.reply_to(incoming_message, "Please select a language to obtain text and then respond with the audio")
            #     responded = True
            # if responded == False:
            #     bot.reply_to(incoming_message, "Success!!! Thanks for contrubution your audio to Bhashadhaan. To continue contributing, choose a language again. For more details, visit: https://bhashini.gov.in/bhashadaan")

            # pass


    if responded == False: 
            bot.reply_to(incoming_message, dekho_validate_string)

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
                        username = "T_"+phone_number
                        message = service.submit_audio(oggfname,each_entry['language_code'],each_entry['dataset_row_id'],username,"file")
                        if message is not None:
                            submitted = True
                        else:
                            bot.reply_to(incoming_message, "Unable to submit the audio at this moment. Please try again later")
                            responded = True
                        break
                    else:
                        bot.reply_to(incoming_message, "Unable to perform the operation. Kindly try again later")
                        responded = True
        if response == None or submitted == False:
            if responded == False:
                bot.reply_to(incoming_message, "Please select a language to obtain text and then respond with the audio")
            responded = True
        if responded == False:
            bot.reply_to(incoming_message, "Success!!! Thanks for contrubution your audio to Bhashadhaan. To continue contributing, choose a language again. For more details, visit: https://bhashini.gov.in/bhashadaan")


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