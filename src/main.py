from datetime import datetime

import pandas as pd
import requests

from src.conf import UsdaMarketUrl
from src.error import UsdaMarketRequestError, ErrorCode
from src.utils import convert_report_to_df, retrieve_reports_url_in_html


def retrieve_all_published_reports():
    """
        This function is useful to load all possible USDA market data into a dataframe
    Returns:
        (dataframe): with all possible data from UsdaMarketUrl.ALL_REPORTS_SUMMARY
    """
    response = requests.get(UsdaMarketUrl.ALL_REPORTS_SUMMARY)
    if response.status_code >= 200 or response.status_code < 300:
        published_reports_info_df = convert_report_to_df(response.content, column_line=3, missed_lines=[0, 1, 2, 3])
    else:
        raise UsdaMarketRequestError(
            f"Request failed to retrieve all published reports with code {response.status_code}",
            ErrorCode.REQUEST_SUBMISSION_ERROR)
    return published_reports_info_df


def retrieve_published_reports_by_criteria(report_type, field_slug_title_value='', start_date=None, end_date=None,
                                           nb_df_limit=100):
    """
        Retrieve all published report references using criteria:
            - report_type (see ReportType in conf.py)

    Args:
        report_type (ReportType): type of the report
        field_slug_title_value (str): the slug name , more information on usda website
        start_date (timestamp): start date to retrieve report (if None search all report in past)
        end_date (timestamp): last date to retrieve report (if None search until today)
        nb_df_limit (int): limit maximum of page to open

    Returns:
        (dataframe): dataframe with all information extract in the table from usda request pages
    """

    reports_info_frames = []
    try:
        for page_number in range(0, nb_df_limit):
            build_query = UsdaMarketUrl.SEARCH_QUERY.format(field_slug_id_value='', name=field_slug_title_value,
                                                            field_slug_title_value='',
                                                            field_published_date_value='',
                                                            field_report_date_end_value='',
                                                            field_api_market_types_target_id=report_type['target_id'],
                                                            page_number=page_number)
            table_df = pd.read_html(build_query)
            table_df[0]['Report Date'] = pd.Series(
                [datetime.timestamp(datetime.strptime(date, "%Y-%m-%d")) for date in table_df[0]['Report Date']])
            table_df[0]['Document'] = pd.Series(retrieve_reports_url_in_html(build_query))
            reports_info_frames += table_df
    except ValueError as err:
        if err.args[0] == 'No tables found':
            pass
    dataframe_result = pd.concat(reports_info_frames)
    if start_date is not None:
        dataframe_result = dataframe_result[dataframe_result['Report Date'] >= start_date]
    if end_date is not None:
        dataframe_result = dataframe_result[dataframe_result['Report Date'] <= end_date]
    return dataframe_result
