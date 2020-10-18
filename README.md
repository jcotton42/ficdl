# fzicdl

A Python script for taking stories from fanfic sites and turning them into eBooks for a more comfortable reading experience.

## Usage

### GUI

```bash
python -m ficdl
```

Proper double-clicking support is coming, see issue #7.

### CLI

```bash
python -m ficdl <URL> -o name.epub
```

Run `python -m ficdl --help` for more options.

## Installation

Clone this repository, or download as a zip file. I'll have something on the releases tab eventually.

### Dependencies

* Python 3.8+ (might work on earlier 3.x versions)
* `beautifulsoup4`, `pypandoc`, and `html5lib`
  * Install with `python -m pip install -r requirements.txt`

## Supported services

* FanFiction.net

Others to come as requested (check the issues, or open one).

## Supported formats

* ePub

Kindle support is coming Soon:tm:.
