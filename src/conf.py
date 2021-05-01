USDA_MARKET_BASE_URL = r"https://mymarketnews.ams.usda.gov/"


class UsdaMarketUrl(enumerate):
    ALL_REPORTS_SUMMARY = USDA_MARKET_BASE_URL + "services/v1/public/listPublishedReports/all"
    SEARCH_QUERY = USDA_MARKET_BASE_URL + r"filerepo/reports?field_slug_id_value={field_slug_id_value}" \
                                          r"&name={name}&field_slug_title_value={field_slug_title_value}" \
                                          r"&field_published_date_value={field_published_date_value}" \
                                          r"&field_report_date_end_value={field_report_date_end_value}" \
                                          r"&field_api_market_types_target_id={field_api_market_types_target_id}" \
                                          r"&page={page_number}"


class ReportType(enumerate):
    APPLE_PROCESSING = {'identifier': 'Apple', 'target_id': '66'}
    AUCTION_SALES = {'identifier': 'Produce Auction', 'target_id': '72'}
    PRODUCTION_COST = {'identifier': 'Production Cost', 'target_id': '117'}
    BIOENERGY = {'identifier': None, 'target_id': '73'}
    OTHER = {'identifier': None, 'target_id': 'All'}


class HTMLBalise(enumerate):
    OPEN_TABLE = '<table class'
    CLOSE_TABLE = '</table>'


class StateIdentifier(enumerate):
    IOWA = 'NW'
    ILLINOIS = 'GX'
    NORTH_CAROLINA = 'RA'
    SOUTH_CAROLINA = 'CO'
