
from cd_src.create_project_structure import create_project_structure
from cd_src.get_course_data import create_course_output
from cd_src.interface import confirm_strict, print_success, shut_down
import cd_src.settings as settings
from cd_src.settings import COURSE_ID
from cd_src.transform_project_data import transform_project_data_fn
from cd_src.transform_for_tableau import transform_for_tableau_fn


def do_it_all():
    create_course_output()
    confirm_strict(f"Please add any New Analytics downloads to {settings.NEWANALYTICS_NEW_FOLDER}. Confirm when complete enter [Y] or exit [N].")
    confirm_strict(f"Please add your Gradebook export to {settings.GRADEBOOK_FOLDER}. Confirm when complete enter [Y] or exit [N].")
    create_project_structure()
    transform_project_data_fn()
    transform_for_tableau_fn()
    print_success("Done!")

if __name__ == "__main__":
    # execute only if run as a script
    do_it_all()
