"""Constants for nrc-to-jpg."""

from datetime import datetime, timezone
from pathlib import Path

DATA_URL_TEMPLATE = "https://www.nrc.nl/de/data/NH/{year:04}/{month:02}/{day:02}/"

DEFAULT_DATE = datetime.now(tz=timezone.utc).date()
DEFAULT_PAGE_NUMBER = 1
DEFAULT_OUTPUT_FILE_TEMPLATE = "NRC_front_page_{year:04}-{month:02}-{day:02}.jpg"
DEFAULT_OUTPUT_FILE = Path(
    DEFAULT_OUTPUT_FILE_TEMPLATE.format(
        year=DEFAULT_DATE.year, month=DEFAULT_DATE.month, day=DEFAULT_DATE.day
    )
)

ALLOWED_OUTPUT_FILE_TEMPLATE_FIELDS = {
    "year",
    "month",
    "day",
    "page_number",
}
