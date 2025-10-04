
from src.custom_steps.check_for_user_inputs import check_for_user_input_files
from src.custom_steps.get_course_details_data import create_course_data
from src.interface import confirm_strict
from src.utils import print_success
import src.settings as settings
from src.settings import COURSE_ID
from src.custom_steps.transform_course_details_data import transform_course_data
from src.custom_steps.transform_course_data_for_tableau import transform_course_data_for_tableau

def do_it_all():
    create_course_data()
    confirm_strict(f"Please add any New Analytics downloads to {settings.NEWANALYTICS_NEW_FOLDER}. Confirm when complete enter [Y] or exit [N].")
    confirm_strict(f"Please add your Gradebook export to {settings.GRADEBOOK_FOLDER}. Confirm when complete enter [Y] or exit [N].")
    check_for_user_input_files()
    transform_course_data()
    transform_course_data_for_tableau()
    print_success("Done!")

if __name__ == "__main__":
    # execute only if run as a script
    do_it_all()
