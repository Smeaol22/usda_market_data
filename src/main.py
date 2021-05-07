import pandas as pd
import requests

from src.conf import UsdaMarketUrl
from src.error import UsdaMarketRequestError
from src.utils import convert_report_to_df


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
            f"Request failed to retrieve all published reports with code {response.status_code}")
    return published_reports_info_df


def retrieve_published_reports_by_criteria(report_type, field_slug_title_value='', field_published_date_value=None,
                                           field_report_date_end_value=None, nb_df_limit=100):
    """
        Retrieve all published report references using criteria:
            - report_type (see ReportType in conf.py)

    Args:
        report_type (ReportType): type of the report
        field_slug_title_value (str): the slug name , more information on usda website
        field_published_date_value (timestamp):
        field_report_date_end_value (timestamp):
        nb_df_limit (int):

    Returns:

    """
    if field_published_date_value is None:
        field_published_date_value = ''
    else:
        field_published_date_value = 'aaa'

    if field_report_date_end_value is None:
        field_report_date_end_value = ''
    else:
        field_report_date_end_value = 'aa'
    reports_info_frames = []
    try:
        for page_number in range(0, nb_df_limit):
            build_query = UsdaMarketUrl.SEARCH_QUERY.format(field_slug_id_value='', name='',
                                                            field_slug_title_value=field_slug_title_value,
                                                            field_published_date_value=field_published_date_value,
                                                            field_report_date_end_value=field_report_date_end_value,
                                                            field_api_market_types_target_id=report_type['target_id'],
                                                            page_number=page_number)
            reports_info_frames += pd.read_html(build_query)
    except ValueError as err:
        if err.args[0] == 'No tables found':
            pass
    return pd.concat(reports_info_frames)
