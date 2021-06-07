import pandas as pd
import requests

from src.conf import ReportType, USDA_MARKET_BASE_URL
from src.error import ErrorCode, UsdaMarketRequestError
from src.main import retrieve_published_reports_by_criteria
from src.utils import extract_element_from_inline_bytes


class ProductionCostStates(enumerate):
    illinois = 'GX_GR210'
    north_carolina = 'RA_GR210'
    south_carolina = 'CO_GR210 '
    iowa = 'NW_GR210'


def get_cost_production_historic(production_cost_state, start_date=None, end_date=None):
    """
        This function is useful to retrieve all information
    Args:
        production_cost_state (str): ProductionCostStates.{state} see ProductionCostStates
        start_date (timestamp): start date to retrieve report (if None search all report in past)
        end_date (timestamp): last date to retrieve report (if None search until today)
    Returns:
        (list): list all report url
    """

    dataframe_result = retrieve_published_reports_by_criteria(ReportType.PRODUCTION_COST,
                                                              field_slug_title_value=production_cost_state,
                                                              start_date=start_date, end_date=end_date)

    production_cost_df_list = []
    for date, report_url in zip(dataframe_result['Report Date'], dataframe_result['Document']):
        production_cost_df_list.append(extract_cost_report_to_df(USDA_MARKET_BASE_URL + report_url, date))
    return pd.concat(production_cost_df_list, ignore_index=True)


def extract_cost_report_to_df(report_url, date, columns=None,
                              start_signal=None, end_signal="source"):
    """
        This function is useful to convert cost production report into a dataframe
    Args:
        report_url (str): report url
        date (timestamp): date of the reports
        columns (list): column list for the output dataframe
        start_signal (list): list of elements to detect begin of the table
        end_signal (str): string signaling table line after ending

    Returns:
        (dataframe): dataframe obtain from the usda report table
    """
    if columns is None:
        columns = ['product', 'offer', 'average', 'date']
    if start_signal is None:
        start_signal = ["product", "price"]
    report_bytes = requests.get(report_url)
    if report_bytes.status_code >= 300 or report_bytes.status_code < 200:
        raise UsdaMarketRequestError(
            f"Request failed to retrieve published reports with code {report_bytes.status_code}",
            ErrorCode.REQUEST_SUBMISSION_ERROR)
    inline_report = report_bytes.content.split(b'\n')
    start_signal_detected = False
    report_data = {}
    for label in columns:
        report_data[label] = []
    for line_report in inline_report:
        elt = extract_element_from_inline_bytes(line_report)
        if start_signal_detected and elt[0].lower().startswith(end_signal):
            break
        if start_signal_detected and elt[0] not in ['\\r', 'Change\\r']:
            for index, label in enumerate(columns):
                if label == 'date':
                    report_data[label] = report_data[label] + [date]
                else:
                    report_data[label] = report_data[label] + [elt[index]]
        if not start_signal_detected and elt[0].lower() in start_signal:
            start_signal_detected = True

    return pd.DataFrame(report_data, columns=columns)
