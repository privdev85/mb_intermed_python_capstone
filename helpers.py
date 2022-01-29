"""Convert datetimes to and from strings.

NASA's dataset provides timestamps as naive datetimes (corresponding to UTC).

The `cd_to_datetime` function converts a string, formatted as the `cd` field of
NASA's close approach data, into a Python `datetime`

The `datetime_to_str` function converts a Python `datetime` into a string.
Although `datetime`s already have human-readable string representations, those
representations display seconds, but NASA's data (and our datetimes!) don't
provide that level of resolution, so the output format also will not.
"""
import datetime
import numpy as np
import pandas as pd


def booltransform(obj):
    transformdict = {
        "Y": True,
        "N": False,
        "": False,
        None: False,
    }  ### transforming None to False since test would otherwise not pass
    if obj in transformdict.keys():
        return transformdict[obj]
    if isinstance(obj, bool) or obj in [0, 1]:
        return bool(obj)
    else:
        raise ValueError("Cannot transform to Bool")


transformdict = {
    "str": lambda obj: str(obj) if obj not in ["", None] else None,
    "float": lambda obj: float(obj) if obj not in ["", None] else float(np.nan),
    "bool": lambda obj: booltransform(obj),
}


def transform_to_str(cval):
    return str(cval).replace("None", "")


def coerce_input(obj, intended_type, transformdict, required=False):
    try:
        return transformdict[intended_type](obj)
    except:
        if required:
            raise ValueError(
                f"Required param not in correct form what object {obj} was passed with intended type {intended_type}"
            )
        else:
            return None


def cd_to_datetime(calendar_date):
    """Convert a NASA-formatted calendar date/time description into a datetime.

    NASA's format, at least in the `cd` field of close approach data, uses the
    English locale's month names. For example, December 31st, 2020 at noon is:

        2020-Dec-31 12:00

    This will become the Python object `datetime.datetime(2020, 12, 31, 12, 0)`.

    :param calendar_date: A calendar date in YYYY-bb-DD hh:mm format.
    :return: A naive `datetime` corresponding to the given calendar date and time.
    """
    return datetime.datetime.strptime(calendar_date, "%Y-%b-%d %H:%M")


def datetime_to_str(dt):
    """Convert a naive Python datetime into a human-readable string.

    The default string representation of a datetime includes seconds; however,
    our data isn't that precise, so this function only formats the year, month,
    date, hour, and minute values. Additionally, this function provides the date
    in the usual ISO 8601 YYYY-MM-DD format to avoid ambiguities with
    locale-specific month names.

    :param dt: A naive Python datetime.
    :return: That datetime, as a human-readable string without seconds.
    """
    return datetime.datetime.strftime(dt, "%Y-%m-%d %H:%M")


def transform_obs_to_df(obs_list, idxname):
    """
    Transform NEO and approaches objects to a pandas dataframe.
    """
    df = pd.DataFrame(
        [element.__dict__.values() for element in obs_list],
        columns=obs_list[0].__dict__.keys(),
    )
    df[idxname] = df.index
    return df


def feature_to_index_dict(feature, obs_list):
    return dict(
        zip([getattr(obj, feature) for obj in obs_list], range(0, len(obs_list)))
    )
