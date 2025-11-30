from dotenv import load_dotenv
from .environment_variables import get_course_id
# import os

load_dotenv()
COURSE_ID = get_course_id()

## MODULE PROGRESS 
## TODO IS THIS BROKEN? OR NEEDED?

status = {}
# ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

INST_CODE = 112240000000000000 # WORKS FOR UBC
# project structure folders 
DATA_FOLDER = f'data/{COURSE_ID}'

# top-level folders (project and raw)
PROJECT_FOLDER = f'{DATA_FOLDER}/project_data'
RAW_FOLDER = f'{DATA_FOLDER}/user_input'
# Raw Data

# Project Data
ORIGINALDATA_FOLDER = f'{PROJECT_FOLDER}/original_data'

APIOUTPUT_FOLDER = f'{ORIGINALDATA_FOLDER}' 

#NEWANALYTICS_FOLDER = f'{RAW_FOLDER}/new_analytics_input'
NEWANALYTICS_NEW_FOLDER = f'{RAW_FOLDER}/new_analytics_input'
GRADEBOOK_FOLDER = f'{RAW_FOLDER}/gradebook_input'

CLEANEDDATA_FOLDER = f'{PROJECT_FOLDER}/cleaned_data'

TABLEAU_FOLDER = DATA_FOLDER