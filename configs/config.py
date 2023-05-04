import os

#Mongo Server, DB and Collections
mongo_server_host = os.environ.get('MONGO_CLUSTER_URL', 'mongodb://localhost:27017/?readPreference=primary&ssl=false')
mongo_bhashadaan_db = os.environ.get('MONGO_WFM_DB', 'bhashadaan')
mongo_bolo_col = os.environ.get('MONGO_WFMJOBS_COL', 'bhashadaan_bolo')
