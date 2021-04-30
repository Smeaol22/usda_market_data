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
