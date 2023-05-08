import os

#Mongo Server, DB and Collections
mongo_server_host = os.environ.get('MONGO_CLUSTER_URL', 'mongodb://localhost:27017/?readPreference=primary&ssl=false')
mongo_bhashadaan_db = os.environ.get('MONGO_WFM_DB', 'bhashadaan')
mongo_bolo_col = os.environ.get('MONGO_WFMJOBS_COL', 'bhashadaan_bolo')
 
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