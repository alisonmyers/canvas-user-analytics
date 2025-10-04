
from src.cd_check_for_downloads import check_for_canvas_downloads
from src.cd_get_course_data import create_course_output
from src.interface import confirm_strict
from src.utils import print_success, shut_down
import src.settings as settings
from src.settings import COURSE_ID
from src.cd_transform_project_data import transform_project_data_fn
from src.cd_transform_for_tableau import transform_for_tableau_fn


def do_it_all():
    create_course_output()
    confirm_strict(f"Please add any New Analytics downloads to {settings.NEWANALYTICS_NEW_FOLDER}. Confirm when complete enter [Y] or exit [N].")
    confirm_strict(f"Please add your Gradebook export to {settings.GRADEBOOK_FOLDER}. Confirm when complete enter [Y] or exit [N].")
    check_for_canvas_downloads()
    transform_project_data_fn()
    transform_for_tableau_fn()
    print_success("Done!")

if __name__ == "__main__":
    # execute only if run as a script
    do_it_all()
