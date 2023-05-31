import os

#Mongo Server, DB and Collections
mongo_server_host = os.environ.get('MONGO_CLUSTER_URL', 'mongodb://localhost:27017/?readPreference=primary&ssl=false')
mongo_bhashadaan_db = os.environ.get('MONGO_BHASHADAAN_DB', 'bhashadaan')
mongo_col = os.environ.get('MONGO_COL', 'bhashadaanCollection')

#Tasks List
list_of_tasks = ["bolo","dekho"]

#Validate Selection String
validate_selection_string = """\
Hello User , welcome to Bhashadaan India. Choose a validation task to start contributing.\n
                1 : Bolo 
                2 : Dekho
                3 : Suno
                4 : Likho\n
Selecting Bolo or Suno provides you with an audio and text within a language. You can help by verifying if they match or not.\n               
Selecting Dekho provides you with an image and text within a language. You can help by verifying if they match or not.\n     
Selecting Likho provides you with text within two languages. You can help by verfiying if they match or not.        
"""


#Intro String
bolo_validate_string = """\
Hello User , welcome to Bolo India. Choose a number and select a language to start contributing.\n
                1 : हिंदी
                2 : தமிழ்
                3 : తెలుగు
                4 : മലയാളം
                5 : অসমীয়া
                6 : বাঙ্গালি
                7 : ગુજરાતી
                8 : ಕನ್ನಡ
                9 : मराठी
                10: ଓଡିଆ

"""

suno_validate_string = """\
Hello User , welcome to Suno India. Choose a number and select a language to start contributing.\n
                1 : हिंदी
                2 : தமிழ்
                3 : తెలుగు
                4 : മലയാളം
                5 : অসমীয়া
                6 : বাঙ্গালি
                7 : ગુજરાતી
                8 : ಕನ್ನಡ
                9 : मराठी
                10: ଓଡିଆ

"""

intro_validate_string = """\
Hello User , welcome to Bolo India. Choose a number and select a language to start contributing.\n
                1 : हिंदी
                2 : தமிழ்
                3 : తెలుగు
                4 : മലയാളം
                5 : অসমীয়া
                6 : বাঙ্গালি
                7 : ગુજરાતી
                8 : ಕನ್ನಡ
                9 : मराठी
                10: ଓଡିଆ

"""

dekho_validate_string = """\
Hello User , welcome to Dekho India Validation. Choose a number and select a language to start validating.\n
                1 : English
                2 : हिंदी
                3 : தமிழ்
                4 : తెలుగు
                5 : മലയാളം
                6 : অসমীয়া
                7 : বাঙ্গালি
                8 : ગુજરાતી
                9 : ಕನ್ನಡ
                10 : मराठी
                11: ଓଡିଆ\n
You will receive an image and text in the language chosen. \n\nIf the image matches the text, please respond with "Y". If it does not match, please respond with "N".
"""

likho_source_validate_string = """\
Hello User , welcome to Dekho India Validation. Choose a number and select the source language to start validating.\n
                1 : English
                2 : हिंदी
                3 : தமிழ்
                4 : తెలుగు
                5 : മലയാളം
                6 : অসমীয়া
                7 : বাঙ্গালি
                8 : ગુજરાતી
                9 : ಕನ್ನಡ
                10 : मराठी
                11: ଓଡିଆ\n
You will receive an text in the source and target language chosen. \n\nIf the translated meaning of the text matches, please respond with "Y". If it does not match, please respond with "N".
"""

likho_target_validate_string = """\
Hello User , welcome to Likho India Validation. Choose a number and select the target language to start validating.\n
                1 : English
                2 : हिंदी
                3 : தமிழ்
                4 : తెలుగు
                5 : മലയാളം
                6 : অসমীয়া
                7 : বাঙ্গালি
                8 : ગુજરાતી
                9 : ಕನ್ನಡ
                10 : मराठी
                11: ଓଡିଆ\n
You will receive an text in the source and target language chosen. \n\nIf the translated meaning of the text matches, please respond with "Y". If it does not match, please respond with "N".
"""