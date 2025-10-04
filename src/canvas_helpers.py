"""
Canvas API Helpers: Fetching courses, modules, students, and module status.
"""

from canvasapi import Canvas
import pandas as pd
from tqdm import tqdm
import os
from yaspin import yaspin

from .utils import print_success, shut_down
from .data_utils import create_dict_from_object, _list_to_df, _dict_to_cols, _clean_datetime_value

def get_modules(course):
    """Returns all modules from specified course"""
    print("Getting Module Information ...")
    try:
        modules = course.get_modules(include=["items"], per_page=50)
        attrs = [
            "id", "name", "position", "unlock_at", "require_sequential_progress",
            "another item", "publish_final_grade", "prerequisite_module_ids",
            "published", "items_count", "items_url", "items", "course_id",
        ]
        modules_dict = [create_dict_from_object(m, attrs) for m in modules]
        modules_df = pd.DataFrame(modules_dict)
        modules_df = modules_df.rename(
            columns={"id": "module_id", "name": "module_name", "position": "module_position"}
        )
    except Exception:
        raise KeyError("Unable to get modules for course: " + course.name)
    else:
        return modules_df


def get_items(modules_df, cname):
    """Returns expanded modules data"""
    print("Getting item information ...")
    try:
        expanded_items = _list_to_df(
            modules_df[["module_id", "module_name", "course_id", "items"]], "items"
        )
        items_df = _dict_to_cols(expanded_items, "items", "items_")
        items_df = _dict_to_cols(
            items_df.reset_index(drop=True),
            "items_completion_requirement",
            "items_completion_req_",
        )
    except KeyError:
        print('No items to expand ... skipping row ...')
        return None
    else:
        return items_df


def get_student_module_status(course):
    """Returns DataFrame with students' module progress"""
    print("Getting Module Status for students ...")
    students_df = _get_students(course)
    enrollments_df = _get_enrollments(course)

    print("Getting student module info for " + course.name)
    student_module_status = pd.DataFrame()

    num_rows = len(list(students_df.iterrows()))
    with tqdm(total=num_rows) as pbar:
        for i, row in students_df.iterrows():
            pbar.update(1)
            sid = row["id"]
            student_data = course.get_modules(student_id=sid, include=["items"], per_page=50)
            attrs = [
                "id", "name", "position", "unlock_at", "require_sequential_progress",
                "publish_final_grade", "prerequisite_module_ids", "state",
                "completed_at", "items_count", "items_url", "items", "course_id",
            ]
            student_rows_dict = [create_dict_from_object(m, attrs) for m in student_data]
            student_rows = pd.DataFrame(student_rows_dict)
            student_rows["student_id"] = str(sid)
            student_rows["sis_user_id"] = row["sis_user_id"]
            student_rows["student_name"] = row["name"]
            student_rows["sortable_student_name"] = row["sortable_name"]
            student_module_status = pd.concat([student_module_status, student_rows], ignore_index=True, sort=False)

    student_module_status = student_module_status.rename(
        columns={"id": "module_id", "name": "module_name", "position": "module_position"}
    )
    student_module_status_with_enrollment_date = student_module_status.merge(
        enrollments_df, how='left', left_on='student_id', right_on='user_id'
    )
    return student_module_status_with_enrollment_date


def get_student_items_status(course, module_status):
    """Returns expanded student module status data table"""
    try:
        expanded_items = _list_to_df(module_status, "items")
    except KeyError as e:
        raise KeyError("Course has no items completed by students")

    expanded_items = _dict_to_cols(expanded_items, "items", "items_")
    student_items_status = _dict_to_cols(
        expanded_items, "items_completion_requirement", "item_cp_req_"
    ).reset_index(drop=True)
    student_items_status["course_id"] = course.id
    student_items_status["course_name"] = course.name

    items_status_list = student_items_status["completed_at"].values.tolist()
    cleaned = map(_clean_datetime_value, items_status_list)
    student_items_status["completed_at"] = list(cleaned)

    dates = student_items_status["completed_at"].unique()
    print("Max Date:")
    print(max([pd.to_datetime(i) for i in dates if i is not None]).strftime("%Y-%m-%d %H:%M:%S"))

    student_items_status = student_items_status[
        [
            "completed_at", "course_id", "module_id", "items_count",
            "module_name", "module_position", "state", "unlock_at",
            "student_id", "student_name", "items_id", "items_title",
            "items_position", "items_indent", "items_type", "items_module_id",
            "item_cp_req_type", "item_cp_req_completed", "course_name",
        ]
    ]

    return student_items_status


def create_canvas_object(): 
    try:
        url = os.getenv('API_URL')
        token = os.getenv('API_TOKEN')
        auth_header = {'Authorization': f'Bearer {token}'}
        canvas = Canvas(url, token)
        try:
            user = canvas.get_user('self')
            print_success(f'\nHello, {user.name}!')
        except Exception as e:
            shut_down("""
                ERROR: could not get user from server.
                Please ensure token is correct and valid and ensure using the correct instance url.
            """)
        return(canvas, auth_header)
    except Exception as e:
        shut_down(f'{e}: Canvas object not created')
        return(False)

def _get_students(course):
    """Returns DataFrame table with students enrolled in specified course

    Makes a request to Canvas LMS REST API through Canvas Python API Wrapper
    Calls make_dataframe to convert response to Pandas DataFrame. Returns
    DataFrame.

    Args:
        course (canvasapi.course.Course): The course obj.
               from Canvas Python API wrapper

    Returns:
        DataFrame: Students table

    """
    # print("Getting student list")
    students = course.get_users(
        include=["test_student", "email"], enrollment_type=["student"], per_page=50
    )
    attrs = [
        "id",
        "name",
        "created_at",
        "sortable_name",
        "short_name",
        "sis_user_id",
        "integration_id",
        "login_id",
        "pronouns",
    ]

    students_data = [create_dict_from_object(s, attrs) for s in students]
    students_df = pd.DataFrame(students_data)
    return students_df


def _get_enrollments(course):
    """Returns all enrollments from specified course

    Makes a request to Canvas LMS REST API through Canvas Python API Wrapper
    Calls make_dataframe to convert response to Pandas DataFrame. Returns
    DataFrame.

    Args:
        course (canvasapi.course.Course): The course obj.
               from Canvas Python API wrapper

    Returns:
        DataFrame: Students table
    """
    # print("Getting course enrollments")
    enrollments = course.get_enrollments(
       enrollment_type=["student"], per_page=50
    )
    attrs = [
        "created_at",
        "user_id"
    ]

    enrollment_data = [create_dict_from_object(e, attrs) for e in enrollments]
    enrollments_df = pd.DataFrame(enrollment_data)
    enrollments_df['user_id'] = enrollments_df['user_id'].astype(str)
    return enrollments_df

def __clean_datetime_value(datetime_string):
    """Given"""
    if datetime_string is None:
        return datetime_string

    if isinstance(datetime_string, str):
        x = datetime_string.replace("T", " ")
        return x.replace("Z", "")

    raise TypeError("Expected datetime_string to be of type string (or None)")


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