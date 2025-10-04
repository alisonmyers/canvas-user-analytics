from .canvas_helpers import create_canvas_object, create_df_and_csv
from . import file_utils 
from . import settings
from .utils import print_success
from .settings import COURSE_ID
from . import special_course_details

""" Creates the initial course data which will be output in data/COURSE_ID/raw/api_output 
and creates a new_analytics_input folder for user
"""

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