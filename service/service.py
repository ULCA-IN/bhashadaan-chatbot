import json
import requests
from repo.repo import Repository
import uuid
import os
from os import path
from pydub import AudioSegment
from configs.credentials import get_sentence_headers,submit_audio_headers, get_sentence_url, submit_audio_url, fetch_ocr_headers, verify_sentence_headers, skip_sentence_headers

repo = Repository()

class Service:

    def get_number_of_input(self,input):
        try: 
            if int(input) in range(1,12):
                return int(input)
        except:
            return None

    def get_language_from_code(self,lang_code):
            if lang_code == "1":
                return "English"
            if lang_code == "2":
                return "Hindi"
            elif lang_code == "3":
                return "Tamil"
            elif lang_code == "4":
                return "Telugu"
            elif lang_code == "5":
                return "Malayalam"
            elif lang_code == "6":
                return "Assamese"
            elif lang_code == "7":
                return "Bengali"
            elif lang_code == "8":
                return "Gujarati"
            elif lang_code == "9":
                return "Kannada"
            elif lang_code == "10":
                return "Marathi"
            elif lang_code == "11":
                return "Odia"
            
    def make_submit_true(self,phone_number,audio_url):
        search_query = {"_id":phone_number}
        response = repo.search_entry(search_query)
        submittable = False
        function_response = None
        if len(response)>0:
            if "content" in response[0].keys():
                for each_entry in response[0]['content']:
                    if each_entry['submitted'] == False:
                        updation = { "$pull": { 'content': { "submitted": False } } }
                        repo.update_entry(updation,phone_number)
                        updation = { "$push": { 'content': { "submitted": True,
                                                            "dataset_row_id": each_entry['dataset_row_id'], 
                                                            "language_code": each_entry['language_code'], 
                                                            "taskOperation": each_entry['taskOperation'],
                                                             "audioUrl": audio_url } } }
                        submittable = True
                        repo.update_entry(updation,phone_number)
                        return "Update Success"
        if len(response) == 0 or submittable == False:
            return None

    def make_dekho_submit_true(self,phone_number,status):
        search_query = {"_id":phone_number}
        response = repo.search_entry(search_query)
        submittable = False
        function_response = None
        if len(response)>0:
            if "content" in response[0].keys():
                for each_entry in response[0]['content']:
                    if each_entry['submitted'] == False:
                        updation = { "$pull": { 'content': { "submitted": False } } }
                        repo.update_entry(updation,phone_number)
                        updation = { "$push": { 'content': {    "submitted": True,
                                                                "dataset_row_id": each_entry['dataset_row_id'], 
                                                                "language_code": each_entry['language_code'], 
                                                                "taskOperation": each_entry['taskOperation'],
                                                                "contribution": each_entry['contribution'],
                                                                "contribution_id": each_entry['contribution_id'],
                                                                "image_url": each_entry['image_url'],
                                                                "status":status,
                                                                "taskOperation": "validate" } } }
                        submittable = True
                        repo.update_entry(updation,phone_number)
                        return "Update Success"
        if len(response) == 0 or submittable == False:
            return None



                             #phone_number,dataset_row_id,contribution,contribution_id,image_url,"validate",input,delete_submitted=True,updateEntry=True
    def get_search_entry(self,phone_number,dataset_row_id=None,contribution=None,contribution_id=None,image_url=None,taskOperation=None,incoming_msg=None,delete_submitted=False,updateEntry=False):
        search_query = {"_id":phone_number}
        response = repo.search_entry(search_query)
        function_response = None
        #If delete_submitted is True, then submitted false will be deleted.
        #If update entry is true, current entiry will be submitted as false.
        if delete_submitted == True and len(response)>0:
            if "content" in response[0].keys():
                for each_entry in response[0]['content']:
                    if each_entry['submitted'] == False:
                        #optimize
                        updation = { "$pull": { 'content': { "submitted": False } } }
                        repo.update_entry(updation,phone_number)
            if updateEntry == True:
                updation = { "$push": { 'content': { "submitted": False,
                                                    "dataset_row_id": dataset_row_id,
                                                    "contribution": contribution,
                                                    "contribution_id": contribution_id,
                                                    "image_url": image_url,
                                                    "language_code": self.get_language_from_code(incoming_msg), 
                                                    "taskOperation": taskOperation } } }
                repo.update_entry(updation,phone_number)
                return "Update Success"
        if len(response)==0:
            return None
        else:
            return response

    def send_sentence(self, lang_code):
            lang_code = self.get_language_from_code(lang_code)

            url = get_sentence_url

            payload = json.dumps({
                "language": lang_code,
                "userName": "aswin"
            })
            headers = get_sentence_headers
            response = requests.request(
                "POST", url, headers=headers, data=payload, verify=False)
            print(response.json())
            if response.status_code >= 200 and response.status_code <= 204:
                print(response.json())
                text = response.json()["data"][0]["media_data"]
                dataset_row_id = response.json()["data"][0]["dataset_row_id"]
                function_response = text + "\n \n \n Kindly read out the above sentence in selected language and send the recording to contribute"
                return function_response, dataset_row_id
            else: 
                return "Unable to obtain the content for now, please try again later", None
            


    def submit_audio(self, audio_url, lang_code, dataset_row_id,username,audio_type = "url"):
        url = submit_audio_url
        fid  = str(uuid.uuid4())

        if audio_type == "url":
            oggfname = fid+".ogg"
            wavfname = fid+".wav"
            r = requests.get(audio_url)
            #print(r.content)
            with open(oggfname,'wb') as output:
                output.write(r.content)
            sound = AudioSegment.from_ogg(oggfname)
            sound.export(wavfname, format="wav")
        else: 
            sound = AudioSegment.from_ogg(audio_url)
            wavfname = audio_url.replace(".ogg",".wav")
            sound.export(wavfname, format="wav")
                    
        username = "W_T_Bots"
        payload = {'language': lang_code,
        'sentenceId': dataset_row_id,
        'country': 'India',
        'state': 'Kerala',
        'audioDuration': '6.719',
        'speakerDetails': '{"userName":'+username+',"age":"upto 10","motherTongue":"Malayalam","gender":"male"}',
        'device': 'Linux null',
        'browser': 'Chrome 100.0.4896.88',
        'type': 'text'}
        files=[
        ('audio_data',(wavfname,open(wavfname,'rb'),'audio/wav'))
        ]
        headers = submit_audio_headers

        response = requests.request("POST", url, headers=headers, data=payload, files=files, verify=False)
        print("Response of bhashadaan store: ",response.status_code,response.text)
        # try: 
        #     os.remove(oggfname)
        #     os.remove(wavfname)
        # except:
        #     print("Exception during removal of file")
        if response.status_code >= 200 and response.status_code <= 204:
            return "Thanks for contrubutiong your audio to Bhashadhaan. To continue contributing, choose a language again. For more details, visit: https://bhashini.gov.in/bhashadaan"
        else: 
            return None
        
    #DEKHO_FUNCTIONS
    def fetch_ocr(self,language,username):
        fetch_url = "https://bhashadaan-api.bhashini.gov.in/contributions/ocr?from="+language+"&to=&username="+username

        payload = ""
        headers = fetch_ocr_headers

        try:
            response = requests.request("GET", fetch_url, headers=headers, data=payload, verify=False)
        except:
            return None 
        
        print("Response from Fetch_OCR",response.status_code,response.text)

        if response.status_code >=200 and response.status_code <= 204 and "data" in response.json().keys() and len(response.json()["data"])>0:
            dataset_row_id = response.json()["data"][0]["dataset_row_id"]
            sentence = response.json()["data"][0]["sentence"]
            contribution = response.json()["data"][0]["contribution"]
            contribution_id = response.json()["data"][0]["contribution_id"]
            image_url = "https://bhashadaan-data.azureedge.net/"+sentence
            return (dataset_row_id, contribution, contribution_id, image_url)
        else: 
            return None
  

    def verify_sentence(self,username,language,dataset_row_id,contribution_id):

        verify_url = "https://bhashadaan-api.bhashini.gov.in/validate/"+str(contribution_id)+"/accept"

        payload = json.dumps({
        "device": "Linux null",
        "browser": "Chrome 100.0.4896.88",
        "userName": username,
        "fromLanguage": language,
        "sentenceId": dataset_row_id,
        "state": "Kerala",
        "country": "India",
        "type": "ocr"
        })
        headers = verify_sentence_headers
        
        try:
            response = requests.request("POST", verify_url, headers=headers, data=payload, verify=False)
        except Exception as e:
            print(e)
            return None

        print("Response from verify_sentence",response.status_code,response.text)

        if response.status_code >=200 and response.status_code <= 204:
            return "Successfully Verified"
        else: 
            return None
  

    def skip_sentence(self,username,language,dataset_row_id,contribution_id):
        skip_url = "https://bhashadaan-api.bhashini.gov.in/validate/"+str(contribution_id)+"/skip"

        payload = json.dumps({
        "device": "Linux null",
        "browser": "Chrome 100.0.4896.88",
        "userName": username,
        "fromLanguage": language,
        "sentenceId": dataset_row_id,
        "state": "Kerala",
        "country": "India",
        "type": "ocr"
        })
        headers = skip_sentence_headers

        try:
            response = requests.request("POST", skip_url, headers=headers, data=payload, verify=False)
        except Exception as e:
            print(e)
            return None

        print("Response from skip_sentence",response.status_code,response.text)

        if response.status_code >=200 and response.status_code <= 204:
            return "Successfully Verified"
        else: 
            return None