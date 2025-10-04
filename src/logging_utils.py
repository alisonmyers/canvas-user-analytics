"""
Logging helpers for module progress status.
"""

import pandas as pd
import datetime
from .settings import status


def log_failure(cid, msg):
    status[str(cid)]["status"] = "Failed"
    status[str(cid)]["message"] = msg

def log_success(cid):
    status[str(cid)]["status"] = "Success"
    status[str(cid)]["message"] = "Course folder has been created in data directory"

def _output_status_table(tableau_path):
    current_dt = datetime.datetime.now()
    cols = ["Course Id", "Course Name", "Status", "Message", "Data Updated On"]
    data = []
    for cid, info in status.items():
        row = [cid, info["cname"], info["status"], info["message"], current_dt]
        data.append(row)
    dataframe = pd.DataFrame(data, columns=cols)
    status_path = tableau_path / "status.csv"
    dataframe.to_csv(status_path, index=False)

# def log_failure_to_table(cid, msg):
#     """Adds failure log to global status object

#     Args:
#         cid (Integer): course id who's status has changed - used to create log entry
#         msg (String): description of the failure
#     """
#     settings.status[str(cid)]["status"] = "Failed"
#     settings.status[str(cid)]["message"] = msg


# def log_success_to_table(cid):
#     """Adds success log to glbal status object

#     Args:
#         cid (Integer): course id who's status has changed - used to create log entry
#     """
#     settings.status[str(cid)]["status"] = "Success"
#     settings.status[str(cid)][
#         "message"
#     ] = "Course folder has been created in data directory"


