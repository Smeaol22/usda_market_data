import pandas as pd

from src.conf import ReportType
from src.main import retrieve_published_reports_by_criteria
from src.utils import extract_element_from_inline_bytes


class ProductionCostStates(enumerate):
    illinois = 'GX_GR210'
    north_carolina = 'RA_GR210'
    south_carolina = 'CO_GR210 '
    iowa = 'NW_GR210'


def list_all_cost_production_url(production_cost_state, start_date=None, end_date=None):
    """
        This function is useful to retrieve all url related to
    Args:
        production_cost_state (ProductionCostStates):
        start_date (timestamp): start date to retrieve report (if None search all report in past)
        end_date (timestamp): last date to retrieve report (if None search until today)
    Returns:
        (list): list all report url
    """

    dataframe_result = retrieve_published_reports_by_criteria(ReportType.PRODUCTION_COST,
                                                              field_slug_title_value=production_cost_state)
    for row in dataframe_result.iterrows():
        build_query = row
    return False


def extract_report_to_df(report_bytes_content, date, columns=['product', 'offer', 'average', 'date'],
                         start_signal=["product", "price"], end_signal="source"):
    """
        This function is useful to convert cost production report into a dataframe
    Args:
        report_bytes_content (bytes): reports upload from usda in bytes
        date (timestamp): date of the reports
        columns (list): column list for the output dataframe
        start_signal (list): list of elements to detect begin of the table
        end_signal (str): string signaling table line after ending

    Returns:
        (dataframe): dataframe obtain from the usda report table
    """

    inline_report = report_bytes_content.split(b'\n')
    start_signal_detected = False
    report_data = {}
    for label in columns:
        report_data[label] = []
    for line_report in inline_report:
        elt = extract_element_from_inline_bytes(line_report)
        if start_signal_detected and elt[0].lower().startswith(end_signal):
            break
        if start_signal_detected and elt[0] != '\\r':
            for index, label in enumerate(columns):
                if label == 'date':
                    report_data[label] = report_data[label] + [date]
                else:
                    report_data[label] = report_data[label] + [elt[index]]
        if not start_signal_detected and elt[0].lower() in start_signal:
            start_signal_detected = True

    return pd.DataFrame(report_data, columns=columns)
