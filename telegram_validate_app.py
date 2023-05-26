import urllib
import telebot
from configs.credentials import telegram_auth_token
from service.service import Service
from repo.repo import Repository
import uuid
from configs.config import dekho_validate_string,validate_selection_string,list_of_tasks,bolo_validate_string,suno_validate_string
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
    #Store user details
    phone_number = str(message.from_user.id)
    #Store task_selected and language_selected = None
    #If an entry with id as phone_number doesn't exist, create one.
    if(service.create_user(phone_number)) == "Already Exists":
                repo.update_entry({"$set":{"task_selected":None,"language_selected":None}},phone_number)
    bot.reply_to(message,validate_selection_string,parse_mode= 'Markdown')

@bot.message_handler(func=lambda incoming_message: True)
def echo_message(incoming_message):
    input = incoming_message.text
    responded = False
    print("INCOMING MESSAGE : ",incoming_message)
    phone_number = str(incoming_message.from_user.id)

    #Get user details from db
    response = service.get_user_details(phone_number)
    db_response = response
    print("DB Response",response)
    if response is None: 
        service.create_user(phone_number)
        response = service.get_user_details(phone_number)

    #If Task is selected in the current incoming text:
    elif response['task_selected'] == None and service.get_task(input) is not None:
        task_selected = service.get_task(input)
        repo.update_entry({"$set":{"task_selected":task_selected}},phone_number)
        if task_selected == "Bolo":
            bot.reply_to(incoming_message, bolo_validate_string,parse_mode= 'Markdown')
        elif task_selected == "Dekho":
            bot.reply_to(incoming_message, dekho_validate_string,parse_mode= 'Markdown')
        elif task_selected == "Suno":
            bot.reply_to(incoming_message, suno_validate_string,parse_mode= 'Markdown')
        responded = True

    #If word is MORE / LANG / CHANGE
    #Input is LANG:     
    elif responded == False and input.lower() == "lang":
        if response["task_selected"] == None:
            bot.reply_to(incoming_message, "Please select a task in order to change the language\n"+validate_selection_string,parse_mode= 'Markdown')
            responded = True
        elif response["task_selected"] == "Bolo":
            service.remove_submitted_false(phone_number)
            bot.reply_to(incoming_message, bolo_validate_string,parse_mode= 'Markdown')
        elif response["task_selected"] == "Dekho":
            service.remove_submitted_false(phone_number)
            bot.reply_to(incoming_message, dekho_validate_string,parse_mode= 'Markdown')
        elif response["task_selected"] == "Suno":
            service.remove_submitted_false(phone_number)
            bot.reply_to(incoming_message, suno_validate_string,parse_mode= 'Markdown')
        responded = True

    #If input is CHANGE
    elif responded == False and input.lower() == "change":
        repo.update_entry({"$set":{"task_selected":None,"language_selected":None}},phone_number)
        bot.reply_to(incoming_message,validate_selection_string,parse_mode= 'Markdown')
        responded = True


    #If language is selected by user as a number Or if MORE is entered as input
    elif responded == False and response['task_selected'] != None and service.get_number_of_input(input) is not None:
        if response['task_selected'] == "Bolo":
            if service.get_number_of_input(input) == 0:
                lang_selected = response["language_selected"]
            else:
                lang_selected = service.get_bolo_language_from_code(input)
            function_response = service.fetch_audio(lang_selected,username)
            if function_response is not None: 
                phone_number = str(incoming_message.from_user.id)
                #(dataset_row_id, contribution, contribution_id, content_url)
                dataset_row_id = function_response[0] #Original Image ID
                contribution = function_response[1] #Text
                contribution_id = function_response[2] #Text ID
                content_url = function_response[3] #URL of Image
                #phone_number = phone_number.replace("whatsapp:+","")
                response = service.get_search_entry(phone_number,lang_selected,dataset_row_id,contribution,contribution_id,content_url,"bolo_validate",input,delete_submitted=True,updateEntry=True)
                repo.update_entry({ "$set" : {"language_selected":lang_selected}},phone_number)
                if response is None:
                    entry = {
                                "_id":phone_number,
                                "content":[
                                    {
                                        "submitted": False,
                                        "dataset_row_id": dataset_row_id,
                                        "contribution": contribution,
                                        "contribution_id": contribution_id,
                                        "content_url": content_url,
                                        "language_code": lang_selected,
                                        "taskOperation": 'validate'
                                    }
                                ]
                            }
                    repo.create_entry(entry)
                try: 
                    f = open("Aud"+phone_number+".wav",'wb')
                    f.write(urllib.request.urlopen(content_url).read())
                    f.close()
                    audio = open("Aud"+phone_number+".wav", 'rb')
                    os.remove("Aud"+phone_number+".wav")
                    bot.send_audio(incoming_message.chat.id, audio, reply_to_message_id=incoming_message.message_id)
                    bot.reply_to(incoming_message, "Transcript of the audio: "+str(contribution)+"""\n\nPlease respond with "*Y*" if the the audio matches the text or "*N*" if it does not match the text.\n\nPlease type "*LANG*" to view the list of languages and select once again.\n Please type "*CHANGE*" to choose the task again""",parse_mode= 'Markdown')
                    responded = True
                except Exception as e:
                    print(e)
            else:
                bot.reply_to(incoming_message, """Unable to fetch the content. Please try again shortly.""",parse_mode= 'Markdown')
                responded = True



        elif response['task_selected'] == "Dekho":
            if service.get_number_of_input(input) == 0:
                lang_selected = response["language_selected"]
            else:
                lang_selected = service.get_dekho_language_from_code(input)
            function_response = service.fetch_ocr(lang_selected,username)
            if function_response is not None: 
                phone_number = str(incoming_message.from_user.id)
                #(dataset_row_id, contribution, contribution_id, content_url)
                dataset_row_id = function_response[0] #Original Image ID
                contribution = function_response[1] #Text
                contribution_id = function_response[2] #Text ID
                content_url = function_response[3] #URL of Image
                #phone_number = phone_number.replace("whatsapp:+","")
                response = service.get_search_entry(phone_number,lang_selected,dataset_row_id,contribution,contribution_id,content_url,"dekho_validate",input,delete_submitted=True,updateEntry=True)
                repo.update_entry({ "$set" : {"language_selected":lang_selected}},phone_number)
                if response is None:
                    entry = {
                                "_id":phone_number,
                                "content":[
                                    {
                                        "submitted": False,
                                        "dataset_row_id": dataset_row_id,
                                        "contribution": contribution,
                                        "contribution_id": contribution_id,
                                        "content_url": content_url,
                                        "language_code": lang_selected,
                                        "taskOperation": 'validate'
                                    }
                                ]
                            }
                    repo.create_entry(entry)
                try: 
                    #Figure out 
                    basewidth = 1000
                    response = requests.get(content_url)
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
                    bot.reply_to(incoming_message, contribution+"\n\n"+"""Please respond with "*Y*" if the the image matches the text or "*N*" if it does not match the text.\n\nPlease type "*LANG*" to view the list of languages and select once again.\n Please type "*CHANGE*" to choose the task again""",parse_mode= 'Markdown')
                    responded = True

                except Exception as e:
                    print(e)
            else:
                bot.reply_to(incoming_message, """Unable to fetch the content. Please try again shortly.""",parse_mode= 'Markdown')
                responded = True


        elif response['task_selected'] == "Suno":
            if service.get_number_of_input(input) == 0:
                lang_selected = response["language_selected"]
            else:
                lang_selected = service.get_bolo_language_from_code(input)
            function_response = service.fetch_suno(lang_selected,username)
            if function_response is not None: 
                phone_number = str(incoming_message.from_user.id)
                #(dataset_row_id, contribution, contribution_id, content_url)
                dataset_row_id = function_response[0] #Original Audio ID
                contribution = function_response[1] #Text
                contribution_id = function_response[2] #Text ID
                content_url = function_response[3] #URL of Audio
                #phone_number = phone_number.replace("whatsapp:+","")
                response = service.get_search_entry(phone_number,lang_selected,dataset_row_id,contribution,contribution_id,content_url,"suno_validate",input,delete_submitted=True,updateEntry=True)
                repo.update_entry({ "$set" : {"language_selected":lang_selected}},phone_number)
                if response is None:
                    entry = {
                                "_id":phone_number,
                                "content":[
                                    {
                                        "submitted": False,
                                        "dataset_row_id": dataset_row_id,
                                        "contribution": contribution,
                                        "contribution_id": contribution_id,
                                        "content_url": content_url,
                                        "language_code": lang_selected,
                                        "taskOperation": 'validate'
                                    }
                                ]
                            }
                    repo.create_entry(entry)
                try: 
                    f = open("Aud"+phone_number+".wav",'wb')
                    f.write(urllib.request.urlopen(content_url).read())
                    f.close()
                    audio = open("Aud"+phone_number+".wav", 'rb')
                    os.remove("Aud"+phone_number+".wav")
                    bot.send_audio(incoming_message.chat.id, audio, reply_to_message_id=incoming_message.message_id)
                    bot.reply_to(incoming_message, "Transcript of the audio: "+str(contribution)+"""\n\nPlease respond with "*Y*" if the the audio matches the text or "*N*" if it does not match the text.\n\nPlease type "*LANG*" to view the list of languages and select once again.\n Please type "*CHANGE*" to choose the task again""",parse_mode= 'Markdown')
                    responded = True
                except Exception as e:
                    print(e)
            else:
                bot.reply_to(incoming_message, """Unable to fetch the content. Please try again shortly.""",parse_mode= 'Markdown')
                responded = True









    #If Response is y or n (For validate / skip)
    elif responded == False and response['task_selected'] != None and response['language_selected'] != None and input.lower() == "y" or input.lower() == "n":
        if response['task_selected'] == "Bolo":
            submitted = False
            function_response1 = function_response2 = None
            phone_number = str(incoming_message.from_user.id)
            response = service.get_search_entry(phone_number,response['language_selected'])
            print("DB Response from get search entry",response)
            if response is not None and "content" in response[0].keys():
                for each_entry in response[0]['content']:
                    if each_entry['submitted'] == False:
                        if(input.lower()=="y"):
                            function_response1 = service.make_submit_true(phone_number,"accept")
                            function_response2 = service.bolo_validate_verify(username,each_entry['language_code'],each_entry['dataset_row_id'],each_entry['contribution_id'])
                        else: 
                            function_response1 = service.make_submit_true(phone_number,"skip")
                            function_response2 = service.bolo_validate_skip(username,each_entry['language_code'],each_entry['dataset_row_id'],each_entry['contribution_id'])
                        if function_response1 is not None and function_response2 is not None:
                            submitted = True
                        else:
                            bot.reply_to(incoming_message, "Unable to submit the response at this moment. Please try again later",parse_mode= 'Markdown')
                            responded = True
                        break
            if response == None or submitted == False:
                if responded == False:
                    bot.reply_to(incoming_message, "Unable to submit the response at this moment. Please try again later",parse_mode= 'Markdown')
                    responded = True
            if responded == False:
                responded = True
                bot.reply_to(incoming_message, """*Success!* Thanks for your contribution to Bhashadhaan.\nTo continue contributing in the same language, type "*MORE*".\nTo change the language, type "*LANG*".\nTo change the task, type "*CHANGE*".\nFor more info, visit: https://bhashini.gov.in/bhashadaan""",parse_mode= 'Markdown')




        elif response['task_selected'] == "Dekho":
            submitted = False
            function_response1 = function_response2 = None
            phone_number = str(incoming_message.from_user.id)
            response = service.get_search_entry(phone_number,response['language_selected'])
            if response is not None and "content" in response[0].keys():
                for each_entry in response[0]['content']:
                    if each_entry['submitted'] == False:
                        if(input.lower()=="y"):
                            function_response1 = service.make_submit_true(phone_number,"accept")
                            function_response2 = service.verify_sentence(username,each_entry['language_code'],each_entry['dataset_row_id'],each_entry['contribution_id'])
                        else: 
                            function_response1 = service.make_submit_true(phone_number,"skip")
                            function_response2 = service.skip_sentence(username,each_entry['language_code'],each_entry['dataset_row_id'],each_entry['contribution_id'])
                        if function_response1 is not None and function_response2 is not None:
                            submitted = True
                        else:
                            bot.reply_to(incoming_message, "Unable to submit the response at this moment. Please try again later",parse_mode= 'Markdown')
                            responded = True
                        break
            if response == None or submitted == False:
                if responded == False:
                    bot.reply_to(incoming_message, "Unable to submit the response at this moment. Please try again later",parse_mode= 'Markdown')
                    responded = True
            if responded == False:
                responded = True
                bot.reply_to(incoming_message, """*Success!* Thanks for your contribution to Bhashadhaan.\nTo continue contributing in the same language, type "*MORE*".\nTo change the language, type "*LANG*".\nTo change the task, type "*CHANGE*".\nFor more info, visit: https://bhashini.gov.in/bhashadaan""",parse_mode= 'Markdown')

                    
                        




        if response['task_selected'] == "Suno":
            submitted = False
            function_response1 = function_response2 = None
            phone_number = str(incoming_message.from_user.id)
            response = service.get_search_entry(phone_number,response['language_selected'])
            print("DB Response from get search entry",response)
            if response is not None and "content" in response[0].keys():
                for each_entry in response[0]['content']:
                    if each_entry['submitted'] == False:
                        if(input.lower()=="y"):
                            function_response1 = service.make_submit_true(phone_number,"accept")
                            function_response2 = service.suno_validate_verify(username,each_entry['language_code'],each_entry['dataset_row_id'],each_entry['contribution_id'])
                        else: 
                            function_response1 = service.make_submit_true(phone_number,"skip")
                            function_response2 = service.suno_validate_skip(username,each_entry['language_code'],each_entry['dataset_row_id'],each_entry['contribution_id'])
                        if function_response1 is not None and function_response2 is not None:
                            submitted = True
                        else:
                            bot.reply_to(incoming_message, "Unable to submit the response at this moment. Please try again later",parse_mode= 'Markdown')
                            responded = True
                        break
            if response == None or submitted == False:
                if responded == False:
                    bot.reply_to(incoming_message, "Unable to submit the response at this moment. Please try again later",parse_mode= 'Markdown')
                    responded = True
            if responded == False:
                responded = True
                bot.reply_to(incoming_message, """*Success!* Thanks for your contribution to Bhashadhaan.\nTo continue contributing in the same language, type "*MORE*".\nTo change the language, type "*LANG*".\nTo change the task, type "*CHANGE*".\nFor more info, visit: https://bhashini.gov.in/bhashadaan""",parse_mode= 'Markdown')


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
        if db_response['task_selected']!=None and db_response['language_selected']!=None:
            response = f"Dear User, your current selected task is {db_response['task_selected']} and language selected is {db_response['language_selected']}\n\nTo continue contributing in the same language, type MORE.\n\nTo change the language, type LANG.\n\nTo change the task, type CHANGE."
            bot.reply_to(incoming_message, response)
        elif db_response['language_selected'] == None and db_response['task_selected']!=None:
            if db_response["task_selected"] == "Bolo":
                bot.reply_to(incoming_message, bolo_validate_string,parse_mode='Markdown')
            elif db_response["task_selected"] == "Dekho":
                bot.reply_to(incoming_message, dekho_validate_string,parse_mode='Markdown')
        else:
            bot.reply_to(incoming_message,validate_selection_string,parse_mode='Markdown')

# @bot.message_handler(content_types=['voice'])
# def voice_processing(incoming_message):
#     responded = False
#     submitted = False
#     phone_number = str(incoming_message.from_user.id)
#     file_info = bot.get_file(incoming_message.voice.file_id)
#     downloaded_file = bot.download_file(file_info.file_path)
#     fid  = str(uuid.uuid4())
#     oggfname = fid+".ogg"
#     with open(oggfname, 'wb') as new_file:
#         new_file.write(downloaded_file)
#         print("FILE_PATH:",file_info.file_path)
#         response = service.get_search_entry(phone_number)
#         if response is not None and "content" in response[0].keys():
#             for each_entry in response[0]['content']:
#                 if each_entry['submitted'] == False:
#                     function_response = service.make_submit_true(phone_number,oggfname)
#                     if function_response is not None:
#                         username = "T_"+phone_number
#                         message = service.submit_audio(oggfname,each_entry['language_code'],each_entry['dataset_row_id'],username,"file")
#                         if message is not None:
#                             submitted = True
#                         else:
#                             bot.reply_to(incoming_message, "Unable to submit the audio at this moment. Please try again later")
#                             responded = True
#                         break
#                     else:
#                         bot.reply_to(incoming_message, "Unable to perform the operation. Kindly try again later")
#                         responded = True
#         if response == None or submitted == False:
#             if responded == False:
#                 bot.reply_to(incoming_message, "Please select a language to obtain text and then respond with the audio")
#             responded = True
#         if responded == False:
#             bot.reply_to(incoming_message, "Success!!! Thanks for contrubution your audio to Bhashadhaan. To continue contributing, choose a language again. For more details, visit: https://bhashini.gov.in/bhashadaan")


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