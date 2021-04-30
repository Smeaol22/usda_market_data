USDA_MARKET_BASE_URL = "https://mymarketnews.ams.usda.gov/services/v1/public/"


class UsdaMarketUrl(enumerate):
    ALL_REPORTS_SUMMARY = USDA_MARKET_BASE_URL + "listPublishedReports/all"


class ReportType(enumerate):
    APPLE_PROCESSING = {'identifier': 'Apple', 'target_id': '66'}
    AUCTION_SALES = {'identifier': 'Produce Auction', 'target_id': '72'}
    PRODUCTION_COST = {'identifier': 'Production Cost', 'target_id': '117'}
    BIOENERGY = {'identifier': None, 'target_id': '13'}
    OTHER = {'identifier': None, 'target_id': 'All'}


class StateIdentifier(enumerate):
    IOWA = 'NW'
    ILLINOIS = 'GX'
    NORTH_CAROLINA = 'RA'
    SOUTH_CAROLINA = 'CO'
