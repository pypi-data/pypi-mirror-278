import datetime as dt
from typing import Literal

import pandas as pd

IdType = Literal["ticker", "composite_figi", "cik"]
DateLike = str | dt.date | dt.datetime | pd.Timestamp
DataFrameFormat = Literal["unstacked", "stacked"]
