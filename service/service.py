import json
import requests
from repo.repo import Repository
import uuid
import os
from os import path
from pydub import AudioSegment
from configs.credentials import get_sentence_headers,submit_audio_headers, get_sentence_url, submit_audio_url

repo = Repository()

class Service:

    def get_number_of_input(self,input):
        try: 
            if int(input) in range(1,11):
                return int(input)
        except:
            return None

    def get_language_from_code(self,lang_code):
            if lang_code == "1":
                return "Hindi"
            elif lang_code == "2":
                return "Tamil"
            elif lang_code == "3":
                return "Telugu"
            elif lang_code == "4":
                return "Malayalam"
            elif lang_code == "5":
                return "Assamese"
            elif lang_code == "6":
                return "Bengali"
            elif lang_code == "7":
                return "Gujarati"
            elif lang_code == "8":
                return "Kannada"
            elif lang_code == "9":
                return "Marathi"
            elif lang_code == "10":
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

        pass

    def get_search_entry(self,phone_number,dataset_row_id=None,taskOperation=None,incoming_msg=None,delete_submitted=False,updateEntry=False):
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