"""
Module for report generation
"""
import json
from typing import Optional, Union

import pandas as pd

from ..repos.ReportsRepo import ReportsRepo


def generate_report(
    dataframe: Union[dict, pd.DataFrame],
    plot_type: str,
    output: Optional[str] = "report.pdf",
    title: Optional[str] = None,
    text: Optional[str] = None,
    show_table: Optional[bool] = False,
    zip: Optional[bool] = False,
) -> None:
    """
    Generate a report from a dataframe

    Parameters
    ----------
    dataframe : dict
        The dataframe to be used in the report in JSON format
    output : str
        The path to the output file

    Returns
    -------
    None
    """
    reports_repo = ReportsRepo()

    # Convert dataframe to JSON if it is not already
    if isinstance(dataframe, str):
        try:
            dataframe = json.loads(dataframe)
        except TypeError:
            dataframe = dataframe.to_json()
    elif isinstance(dataframe, pd.DataFrame):
        dataframe = dataframe.to_json()

    body = {
        "dataframe": dataframe,
        "title": title,
        "text": text,
        "plot_type": plot_type,
        "show_table": show_table,
        "zip": zip,
    }
    report_bytes = reports_repo.generate(body)
    with open(output, "wb") as file:
        file.write(report_bytes.content)
