import pandas as pd
from .helpers import create_canvas_object
from . import helpers 
from . import settings
from IPython.display import display, HTML
from datetime import datetime
from .utils import shut_down, print_success
import os
from pathlib import Path
from .settings import COURSE_ID
from . import __course_data_details

""" Creates the initial course data which will be output in data/COURSE_ID/raw/api_output 
and creates a new_analytics_input folder for user
"""

def get_course_data(course, output_folder):

    __course_data_details.ENROLLMENTS_DICT = helpers.create_df_and_csv(course.get_enrollments(), __course_data_details.ENROLLMENTS_DICT, output_folder)
    __course_data_details.ASSIGNMENTS_DICT = helpers.create_df_and_csv(course.get_assignments(), __course_data_details.ASSIGNMENTS_DICT, output_folder)
    __course_data_details.ASSIGNMENTSUBMISSIONS_DICT = helpers.create_df_and_csv(course.get_multiple_submissions(student_ids='all'), __course_data_details.ASSIGNMENTSUBMISSIONS_DICT, output_folder)
    
    #modules and module items
    __course_data_details.MODULES_DICT = helpers.create_df_and_csv(course.get_modules(), __course_data_details.MODULES_DICT, output_folder)
    __course_data_details.MODULEITEMS_DICT = helpers.create_df_and_csv(course.get_modules(), __course_data_details.MODULEITEMS_DICT, output_folder, "get_module_items")


def create_course_data():
    # establish canvas connection
    canvas, auth_header = create_canvas_object()
    
    #create a project structure for the new course
    course = canvas.get_course(COURSE_ID)
    
    helpers.create_folder(settings.APIOUTPUT_FOLDER)
    helpers.create_folder(settings.NEWANALYTICS_NEW_FOLDER)
    helpers.create_folder(settings.GRADEBOOK_FOLDER) 

    get_course_data(course, settings.APIOUTPUT_FOLDER)
    
    print_success("Done! Course data downloaded!")

if __name__ == "__main__":
    # execute only if run as a script
    create_course_data()