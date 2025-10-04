import pandas as pd
import sys
from .helpers import create_folder
from . import settings
from . import cd_data_details
from .helpers import clean_columns_from_rename_dict



def transform_data(detail_dict, drop_rest=False):
    # TODO ADD DATE TO FILE AS HEADER
    file = f'{detail_dict["name"]}'
    rename_dict = detail_dict["rename_dict"]

    in_file =  f'{settings.ORIGINALDATA_FOLDER}/{file}.csv'
    out_file = f'{settings.CLEANEDDATA_FOLDER}/{file}.csv'

    df = pd.read_csv(in_file)

    df = (df.
         pipe(clean_columns_from_rename_dict, rename_dict=rename_dict, drop_rest=drop_rest))

    #print(f'\nWRITING: {out_file}.csv\n')
    df.to_csv(f'{out_file}', index=False)
    
    return(df)

# MOST OF THESE FOLDERS NEED TO CHANGE

def transform_project_data_fn():
    create_folder(settings.CLEANEDDATA_FOLDER)
    #create_folder(settings.CLEANDDATA_TRACKING_TRANSFORMATIONS)

    transform_data(cd_data_details.ASSIGNMENTS_DICT, True)
    transform_data(cd_data_details.MODULEITEMS_DICT, True)
    transform_data(cd_data_details.MODULES_DICT, True)
    transform_data(cd_data_details.ASSIGNMENTSUBMISSIONS_DICT, True)
    transform_data(cd_data_details.ENROLLMENTS_DICT, True) 
    transform_data(cd_data_details.NEWANALYTICS_NEW_DICT, True)
    transform_data(cd_data_details.GRADEBOOKUSERDATA_DICT, True)

if __name__ == "__main__":
    transform_project_data_fn()