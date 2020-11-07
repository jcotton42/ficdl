# Changelog

## v1.8.0

### New features

* PDF output support using wkhtmltopdf <https://wkhtmltopdf.org/>.
  * Custom styling (font family, font size, line height, page size)
    * Settable in File > Preferences in the GUI
    * Via options on the command line
* ficdl can now download and install its own updates.
* The downloader GUI will now suggest naming the story file after the story's title.
* The CLI will infer the filename of the eBook from the title as well if not given.

## v1.7.0

### New features

Added `--dump-html` to the CLI to dump the generated HTML for debugging purposes.

### Bug fixes

Centered text on FanFiction.Net stories now makes it into the eBook (#23).

## v1.6.1

GUI no longer errors when not given a cover path.

## v1.6.0

Support for covers, both scraped from the story and user specified.

## v1.5.0

App can now check for updates.
