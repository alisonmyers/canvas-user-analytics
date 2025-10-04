"""
DataFrame helpers for Canvas module/course processing.
"""

import pandas as pd
from ast import literal_eval
import re

def create_dict_from_object(theobj, list_of_attributes):
    def get_attribute_if_available(theobj, attrname):
        if hasattr(theobj, attrname):
            return {attrname: getattr(theobj, attrname)}
        else:
            return {attrname: None}
    mydict = {}
    for i in list_of_attributes:
        mydict.update(get_attribute_if_available(theobj, i))
    return mydict

def _dict_to_cols(dataframe, col_to_expand, expand_name):
    dataframe[col_to_expand] = dataframe[col_to_expand].apply(_all_dict_to_str)
    original_df = dataframe.drop([col_to_expand], axis=1)
    extended_df = dataframe[col_to_expand].apply(pd.Series, dtype='object')
    extended_df.columns = [
        i if bool(re.search(expand_name, i)) else "{}{}".format(str(expand_name), str(i))
        for i in extended_df.columns
    ]
    new_df = pd.concat([original_df, extended_df], axis=1, ignore_index=False)
    return new_df

def _list_to_df(dataframe, col_to_expand):
    series = dataframe.apply(lambda x: pd.Series(x[col_to_expand]), axis=1).stack().reset_index(level=1, drop=True)
    series.name = col_to_expand
    new_df = dataframe.drop(col_to_expand, axis=1).join(series)
    return new_df

def _all_dict_to_str(d):
    if isinstance(d, dict):
        new = {k: str(v) for k, v in d.items()}
        return new
    else:
        if pd.isnull(d):
            pass
        else:
            d = literal_eval(d)
            new = {k: str(v) for k, v in d.items()}
            return new

def _clean_datetime_value(datetime_string):
    if datetime_string is None:
        return datetime_string
    if isinstance(datetime_string, str):
        x = datetime_string.replace("T", " ")
        return x.replace("Z", "")
    raise TypeError("Expected datetime_string to be of type string (or None)")
