from datetime import datetime
import pytz

# December 31, 2022
OLD_STOCK_THRESHOLD_STR = "2022-12-31"
OLD_STOCK_THRESHOLD = datetime.strptime(
    OLD_STOCK_THRESHOLD_STR, "%Y-%m-%d").replace(tzinfo=pytz.timezone("UTC"))
