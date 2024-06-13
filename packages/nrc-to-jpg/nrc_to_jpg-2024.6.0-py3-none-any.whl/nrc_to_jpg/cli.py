"""Main CLI for nrc-to-jpg."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

import click
from httpx import Client

from . import __version__
from .constants import (
    ALLOWED_OUTPUT_FILE_TEMPLATE_FIELDS,
    DATA_URL_TEMPLATE,
    DEFAULT_DATE,
    DEFAULT_OUTPUT_FILE_TEMPLATE,
    DEFAULT_PAGE_NUMBER,
)
from .utils import get_format_fields, join_wrap

if TYPE_CHECKING:
    from datetime import date


class FormatStr(click.ParamType):
    """The `FormatStr` type checks if the value is a valid format field."""

    name = "format-str"

    def __init__(self, allowed_fields: set[str], *args, **kwargs) -> None:
        """Initialize a new `FormatStr` instance with a set of allowed fields."""
        super().__init__(*args, **kwargs)
        self.allowed_fields = allowed_fields

    def convert(
        self, value: str, param: click.Parameter | None, ctx: click.Context | None
    ) -> str:
        """Convert the value to the correct type. This is not called if the value is None (the missing value)."""
        fields = get_format_fields(value)
        if not fields <= self.allowed_fields:
            self.fail(
                f"`{value}` contains invalid format fields: {join_wrap(fields - self.allowed_fields, ', ', '`')}",
                param,
                ctx,
            )
        return value


@click.command(
    context_settings={"help_option_names": ["-h", "--help"], "show_default": True}
)
@click.version_option(__version__, "-v", "--version")
@click.option(
    "-d",
    "--date",
    "date_",
    type=click.DateTime(),
    default=DEFAULT_DATE.isoformat(),
    help="The date to save that day's front page of.",
)
@click.option(
    "-n",
    "--page-number",
    type=int,
    default=DEFAULT_PAGE_NUMBER,
    help="The page number to .",
)
@click.option(
    "-o",
    "--output",
    "output_template",
    type=FormatStr(ALLOWED_OUTPUT_FILE_TEMPLATE_FIELDS),
    default=DEFAULT_OUTPUT_FILE_TEMPLATE,
    help=f"Output file name template. Allowed fields: {join_wrap(ALLOWED_OUTPUT_FILE_TEMPLATE_FIELDS, ', ', '`')}",
)
def cli(
    date_: date = DEFAULT_DATE,
    page_number: int = DEFAULT_PAGE_NUMBER,
    output_template: str = DEFAULT_OUTPUT_FILE_TEMPLATE,
) -> None:
    """Save the NRC front page to a JPG image."""
    date_ = date_.date() if isinstance(date_, datetime) else date_
    if date_.weekday() == 6:  # noqa: PLR2004
        click.echo(
            "You are trying to get the newspaper for a Sunday. Generally speaking, there is no new paper on Sundays, and this will most likely result in an HTTP error."
        )

    output_file = Path(
        output_template.format(
            year=date_.year, month=date_.month, day=date_.day, page_number=page_number
        )
    )

    with Client() as client:
        data_r = client.get(
            DATA_URL_TEMPLATE.format(year=date_.year, month=date_.month, day=date_.day)
        )
        data_r.raise_for_status()

        data = data_r.json()

        for page in data["pages"]:
            if page["number"] == page_number:
                page_url = page["fullscreen_url_orig"]
                with client.stream("GET", page_url) as page_r:
                    page_r.raise_for_status()
                    with output_file.open("wb") as fh:
                        for chunk in page_r.iter_bytes():
                            fh.write(chunk)
                break
        else:
            click.echo(f"Could not find page {page_number}.")
