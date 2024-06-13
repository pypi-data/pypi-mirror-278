# CLI Reference

This page lists the `--help` for `nrc-to-jpg`.

## nrc-to-jpg

Running `nrc-to-jpg --help` or `python -m nrc_to_jpg --help` shows a list of all of the available arguments and options:

<!-- [[[cog
import cog
from nrc_to_jpg import cli
from click.testing import CliRunner
result = CliRunner().invoke(cli.cli, ["--help"], terminal_width=88)
help = result.output.replace("Usage: cli", "Usage: nrc-to-jpg").replace("'", "\\'")
cog.outl(f"\n```sh\nnrc-to-jpg --help\n{help.rstrip()}\n```\n")
]]] -->

```sh
nrc-to-jpg --help
Usage: nrc-to-jpg [OPTIONS]

  Save the NRC front page to a JPG image.

Options:
  -v, --version                   Show the version and exit.
  -d, --date [%Y-%m-%d|%Y-%m-%dT%H:%M:%S|%Y-%m-%d %H:%M:%S]
                                  The date to save that day\'s front page of.  [default:
                                  2024-06-12]
  -n, --page-number INTEGER       The page number to .  [default: 1]
  -o, --output FORMAT-STR         Output file name template. Allowed fields: `year`,
                                  `page_number`, `day`, `month`  [default:
                                  NRC_front_page_{year:04}-{month:02}-{day:02}.jpg]
  -h, --help                      Show this message and exit.
```

<!-- [[[end]]] -->
