from ..canvas_helpers import create_canvas_object
from .. import file_utils 
from .. import settings
from ..utils import print_success
from ..settings import COURSE_ID
from . import special_course_details
from yaspin import  yaspin
import pandas as pd

""" Creates the initial course data which will be output in data/COURSE_ID/raw/api_output 
and creates a new_analytics_input folder for user
"""
def create_df_and_csv(paginatedlist, data_dict, output_folder, iteration_call=None):
    #TODO - figure out "best" structure for this kind of data
    
    """given a list of objects or paginatedlist return a dataframe
    
    Args:
        paginatedlist (a Canvas PaginatedList)
        output_file (str)
        filter_to_columns (None or list)
        keep (bool)
    
    Returns:
        df (dataframe) 
        
    Output:
        csv in output_path if data available
        
    """
    output_file = f'{output_folder}/{data_dict["name"]}.csv'

    try:
        if iteration_call:
            iteration_list = []

            with yaspin(text=f"Generating: {output_file}"):
                for i in paginatedlist:
                    items = getattr(i, iteration_call)

                    for j in items():
                        j_dict = j.__dict__
                        iteration_list.append(j_dict)
            
            df = pd.DataFrame(iteration_list)


        else:            
            with yaspin(text=f"Generating: {output_file}"):
                df = pd.DataFrame([i.__dict__ for i in paginatedlist])


        print_success(f"Generated: {output_file}")
        data_dict.update({"raw_csv": output_file})
        df.to_csv(f'{output_file}')
        data_dict.update({'df': df})
        return(data_dict)
    
    except Exception as e:
        print(f'{e}')
        return(data_dict.update({"df": None, "raw_csv": None}))

def get_course_data(course, output_folder):

    special_course_details.ENROLLMENTS_DICT = create_df_and_csv(course.get_enrollments(), special_course_details.ENROLLMENTS_DICT, output_folder)
    special_course_details.ASSIGNMENTS_DICT = create_df_and_csv(course.get_assignments(), special_course_details.ASSIGNMENTS_DICT, output_folder)
    special_course_details.ASSIGNMENTSUBMISSIONS_DICT = create_df_and_csv(course.get_multiple_submissions(student_ids='all'), special_course_details.ASSIGNMENTSUBMISSIONS_DICT, output_folder)
    
    #modules and module items
    special_course_details.MODULES_DICT = create_df_and_csv(course.get_modules(), special_course_details.MODULES_DICT, output_folder)
    special_course_details.MODULEITEMS_DICT = create_df_and_csv(course.get_modules(), special_course_details.MODULEITEMS_DICT, output_folder, "get_module_items")


def create_course_data():
    # establish canvas connection
    canvas, auth_header = create_canvas_object()
    
    #create a project structure for the new course
    course = canvas.get_course(COURSE_ID)
    
    file_utils.create_folder(settings.APIOUTPUT_FOLDER)
    file_utils.create_folder(settings.NEWANALYTICS_NEW_FOLDER)
    file_utils.create_folder(settings.GRADEBOOK_FOLDER) 

    get_course_data(course, settings.APIOUTPUT_FOLDER)
    
    print_success("Done! Course data downloaded!")

if __name__ == "__main__":
    # execute only if run as a script
    create_course_data()