from ..utils import print_success, shut_down
from ..file_utils import check_for_data
import glob
import pandas as pd
from ..settings import COURSE_ID
from .. import settings

""" 
Once data collected, this script will create a "project_folder"
and reorganize data as appropriate. 
"""
        
# create folder called project_data
def check_for_user_input_files():
    
    if check_for_data(settings.DATA_FOLDER):
        print_success(f'DATA FOLDER FOUND {settings.DATA_FOLDER}\n')
        
        
        print(f'\nAttempting to parse NEW new analytics data...\n')
        if check_for_data(settings.NEWANALYTICS_NEW_FOLDER, '.csv'):
            print_success(f'{settings.NEWANALYTICS_NEW_FOLDER}: New Analytics data found, compiling...')

            # MOVE TO USER_DATA
            #combined new_analytics_input
            analytics_files = glob.glob(f"{settings.NEWANALYTICS_NEW_FOLDER}/*.csv")
            li = []
            for filename in analytics_files:
                df = pd.read_csv(filename)
                df['file'] = filename
                li.append(df)

            df = pd.concat(li, axis=0)
            df.to_csv(f"{settings.ORIGINALDATA_FOLDER}/new_analytics_new.csv")
 
        else:
            print(f'{settings.NEWANALYTICS_NEW_FOLDER}: No csvs found.')

        if check_for_data(settings.GRADEBOOK_FOLDER, '.csv'):
            print_success(f'{settings.GRADEBOOK_FOLDER}: Gradebook data found, compiling...')

            #TODO look for a single csv file in gradebook_folder
            gb_detail = pd.read_csv(f'{settings.GRADEBOOK_FOLDER}/gradebook.csv', nrows=2)
            column_names = list(gb_detail.columns)
            gb_user = pd.read_csv(f'{settings.GRADEBOOK_FOLDER}/gradebook.csv', names = column_names, skiprows=3)

            gb_user.to_csv(f"{settings.ORIGINALDATA_FOLDER}/gradebook_user_data.csv", index=False)
            gb_detail.to_csv(f"{settings.ORIGINALDATA_FOLDER}/gradebook_details.csv", index=False)

        else:
            print(f'{settings.GRADEBOOK_FOLDER}: No csvs found.')

    else:
        shut_down(f'NO DATA FOLDER FOUND FOR: {settings.DATA_FOLDER}')


if __name__ == "__main__":
    check_for_user_input_files()

    # if there is data in new_analytics_input
    # check that all files follow the same structure (column names)
    # given match, create single output