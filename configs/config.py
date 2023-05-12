import os

#Mongo Server, DB and Collections
mongo_server_host = os.environ.get('MONGO_CLUSTER_URL', 'mongodb://localhost:27017/?readPreference=primary&ssl=false')
mongo_bhashadaan_db = os.environ.get('MONGO_WFM_DB', 'bhashadaan')
mongo_bolo_col = os.environ.get('MONGO_BOLO_COL', 'bhashadaan_bolo')
mongo_dekho_col = os.environ.get('MONGO_DEKHO_COL', 'bhashadaan_dekho')

#Intro String
intro_string = """\
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
You will receive an image and text in the language chosen. If the image matches the text, please respond with "Y". If it does not match, please respond with "N".
"""