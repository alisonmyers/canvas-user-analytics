import pandas as pd
from ..file_utils import create_folder
from .. import settings
from . import special_course_details

def clean_columns_from_rename_dict(df, rename_dict, drop_rest=False): 
    # get column information

    og_cols = df.columns.to_list()
    keep_cols = list(rename_dict.keys())
    unlisted_cols = list(set(og_cols) - set(keep_cols))
    has_dropped = False
    
    # changes if dropping 
    if drop_rest:
        # print("DROPPING UNLISTED COLS")
        dropped_cols = unlisted_cols
        # change record
        if dropped_cols:
            has_dropped = True
            dropped_df = pd.DataFrame(dropped_cols)
            dropped_df.columns = ['original']
            dropped_df['change_note'] = 'deleted'

        # changed_cols_df = changed_cols_df.append(dropped_df, ignore_index=True)
        # make change
        df = df[keep_cols].copy() 
    
    else:
        # print("KEEPING UNLISTED COLS")
        unlisted_dict = dict(zip(unlisted_cols, unlisted_cols))
        rename_dict.update(unlisted_dict)
    
    #print(changed_cols_df.to_markdown())
    df.rename(rename_dict, axis=1, inplace=True)
    #return(df, changed_cols_df)
    return(df)
    

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

def transform_course_data():
    create_folder(settings.CLEANEDDATA_FOLDER)
    #create_folder(settings.CLEANDDATA_TRACKING_TRANSFORMATIONS)

    transform_data(special_course_details.ASSIGNMENTS_DICT, True)
    transform_data(special_course_details.MODULEITEMS_DICT, True)
    transform_data(special_course_details.MODULES_DICT, True)
    transform_data(special_course_details.ASSIGNMENTSUBMISSIONS_DICT, True)
    transform_data(special_course_details.ENROLLMENTS_DICT, True) 
    transform_data(special_course_details.NEWANALYTICS_NEW_DICT, True)
    transform_data(special_course_details.GRADEBOOKUSERDATA_DICT, True)

if __name__ == "__main__":
    transform_course_data()