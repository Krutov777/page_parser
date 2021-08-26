# page_parser
[![Build Status](https://app.travis-ci.com/Krutov777/page_parser.svg?branch=main)](https://app.travis-ci.com/Krutov777/page_parser)[![Maintainability](https://api.codeclimate.com/v1/badges/379d822e5d6dfb379f86/maintainability)](https://codeclimate.com/github/Krutov777/page_parser/maintainability)[![Test Coverage](https://api.codeclimate.com/v1/badges/379d822e5d6dfb379f86/test_coverage)](https://codeclimate.com/github/Krutov777/page_parser/test_coverage)

CLI utility for downloading webpage

### Installation:
```bash
$ pip3 install --user --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple krutov-pageloader
```

### Usage:
```bash
$ pageloader [-o OUTPUT_DIR] [-l {DEBUG,INFO,WARNING,ERROR}] URL
```

### Usage example:
```bash
$ pageloader --output=/path/to/dir https://page-loader.hexlet.repl.co/ 
```
#### For an existing directory
[![asciicast](https://asciinema.org/a/WrW8AFnBBbDLeRiSh6Zo6DnZr.svg)](https://asciinema.org/a/WrW8AFnBBbDLeRiSh6Zo6DnZr)
#### Download to this directory (by default) and check for downloads by a non-existent url 
[![asciicast](https://asciinema.org/a/dCnGL2sgIDjjV2Zxm7MGKLL1B.svg)](https://asciinema.org/a/dCnGL2sgIDjjV2Zxm7MGKLL1B)