import pandas as pd
import urllib3
from bs4 import BeautifulSoup

from src.error import UsdaMarketInternalError, ErrorCode


def convert_report_to_df(report_bytes_content, column_line=None, column=None, missed_lines=None):
    """
        This function is useful to convert report into a dataframe
    Args:
        report_bytes_content (bytes):
        column_line (int): references the line in report_bytes to be used as dataframe column
        column (list): definition of the column for output dataframe
        missed_lines (list): list of lines number to not take into account for dataframe creation

    Returns:
        (dataframe): input report_bytes as dataframe
    """
    if column_line is None and column is None:
        raise UsdaMarketInternalError("column_line or column should be defined", ErrorCode.CONVERSION_ERROR)
    if column_line is not None and column is not None:
        raise UsdaMarketInternalError("column_line and column should not be both defined", ErrorCode.CONVERSION_ERROR)
    inline_report = report_bytes_content.split(b'\n')
    if column_line is not None:
        missed_lines = missed_lines + [column_line]
        columns_list = extract_element_from_inline_bytes(inline_report[column_line])
    else:
        columns_list = column
    report_dict = {}
    for column_label in columns_list:
        report_dict[column_label] = []
    nb_column = len(columns_list)
    for index, line_report in enumerate(inline_report):
        if index not in missed_lines:
            raw_result = extract_element_from_inline_bytes(line_report)
            if len(raw_result) == nb_column:
                for index_res, column_label in enumerate(columns_list):
                    report_dict[column_label] += [raw_result[index_res]]

    return pd.DataFrame(report_dict, columns=columns_list)


def extract_element_from_inline_bytes(line_report):
    """
        This function is useful to extract element from a report line
    Args:
        line_report (bytes): a line array of report

    Returns:
        (list): string list of line_report elements
    """
    str_line_report = str(line_report).replace(')', ') ')
    elt_list = [elt for elt in str_line_report.split('  ') if elt != '']

    elt_list_0 = elt_list[0][2:]
    if elt_list_0 == '':
        elt_list = elt_list[1:]
    else:
        elt_list[0] = elt_list_0
    elt_list[-1] = elt_list[-1][0:-1]
    return elt_list


def retrieve_reports_url_in_html(query_url):
    """
        This function is useful to retrieve reports url from query_url
    Args:
        query_url (str): url request to retrieve all reports

    Returns:
        (list): list of reports url sort by appearance order

    """

    http = urllib3.PoolManager()
    response = http.request('GET', query_url)
    soup = BeautifulSoup(response.data, 'html.parser')
    return [x.find_all('a')[1].attrs['href'] for x in soup.find_all('tr') if x.find_all('a').__len__() < 3]
