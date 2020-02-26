# fontshop-dl
![Version 1.0](https://img.shields.io/badge/Version-1.0-orange.svg)
![Python 2.7, 3.5](https://img.shields.io/badge/Python-2.7%2C%203.5%2B-3776ab.svg)

[![Support me!](https://www.buymeacoffee.com/assets/img/custom_images/yellow_img.png)](https://www.buymeacoffee.com/dvingerh)

Python script to download Fontshop font files in `.woff` format. Supports Python 2.7 and 3.5.

Because of the inner workings of Fontshop, some fonts will be unavailable to be downloaded.
There are [numerous websites](https://www.google.com/search?q=woff+to+ttf+converter&oq=woff+to+ttf+converter) that can convert `.woff` files to `.ttf` (or any other format you want).

Downloads will be saved to `fontshop-dl/Font Name`. Directories are automatically created if they don't exist yet.

### Requirements

This script requires the `requests` module to be installed.

### Usage

Download font family by name (put the name in quotes):
`python fontshop-dl.py "FF Trixie"`

Download font family by URL:
`python fontshop-dl.py https://www.fontshop.com/families/ff-trixie`

##### Example terminal output

```
$ python fontshop-dl.py "FF Trixie"
---------------------------------------------------------------------------
FONTSHOP-DL (SCRIPT V1.0)
---------------------------------------------------------------------------
Found typeface 'FF Trixie' with 6 fonts:
---------------------------------------------------------------------------
FF Trixie Light
FF Trixie Heavy
FF Trixie Rough Light
FF Trixie Rough Heavy
FF Trixie HD Light (Not downloadable)
FF Trixie HD Heavy (Not downloadable)
---------------------------------------------------------------------------
Downloaded: FF Trixie Light
Downloaded: FF Trixie Heavy
Downloaded: FF Trixie Rough Light
Downloaded: FF Trixie Rough Heavy
---------------------------------------------------------------------------
Finished downloading 4 fonts.
---------------------------------------------------------------------------
```
