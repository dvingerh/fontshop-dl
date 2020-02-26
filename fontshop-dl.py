import requests
import sys
import os
import json
import re
try:
	from urllib.parse import urlparse
except ImportError:
	from urlparse import urlparse

BASE_URL = "https://www.fontshop.com/search_data.json?search_mode=families&q={:s}&size=1&fields=typeface_data,opentype_features"
BASE_CSS = "https://www.fontshop.com/webfonts/{:s}.css"
CDN_REGEX = "(fast[^']*)"
PRINT_SEP = '-' * 75
SCRIPT_VER = "1.0"


def log_separator():
	print(PRINT_SEP)


def banner():
	log_separator()
	print("FONTSHOP-DL (SCRIPT V{:s})".format(SCRIPT_VER))
	log_separator()


class Typeface:
	def __init__(self, name, font_count):
		self.name = name
		self.font_count = font_count
		self.fonts = []

	def add_font(self, font):
		self.fonts.append(font)


class Font:
	def __init__(self, name, weight_name, fontid, available):
		self.name = name
		self.weight_name = weight_name
		self.fontid = fontid
		self.available = available


def download_fonts(typeface):
	download_path = os.path.join(os.getcwd(), "fontshop-dl", typeface.name)
	if not os.path.exists(download_path):
		os.makedirs(download_path)
	downloaded_count = 0
	skipped_count = 0
	for font in typeface.fonts:
		if font.available:
			font_css = requests.get(BASE_CSS.format(font.fontid)).text
			woff_url = re.findall(CDN_REGEX, font_css)
			file_to_save = os.path.join(download_path, (font.name + ".woff"))
			if not os.path.isfile(file_to_save):
				woff_request = requests.get("https://" + woff_url[0], headers={'referer': "https://www.fontshop.com/"})
				open(file_to_save, 'wb').write(woff_request.content)
				print("Downloaded: " + font.name)
				downloaded_count += 1
			else:
				print("Already downloaded: " + font.name)
				skipped_count += 1
			
	log_separator()
	print("Finished downloading {:d} fonts.{:s}".format(downloaded_count, "" if not skipped_count else " (skipped {:d} fonts)".format(skipped_count)))
	log_separator()


def get_fonts(typeface_arg, is_url=False):
	if is_url:
		parsed_url = urlparse(typeface_arg)
		search_url = BASE_URL.format(parsed_url.path.split('/').pop())
	else:
		search_url = BASE_URL.format(typeface_arg)
	search_request = requests.get(search_url).json()
	search_results = search_request.get("families").get("hits")
	if search_results.get("total") != 0:
		font_json = search_results.get("hits")[0].get("_source")
		typeface = Typeface(font_json.get("clean_name"), font_json.get("typeface_count"))
		for font in font_json.get("typeface_data"):
			f_name = font.get("name")
			f_weight_name = font.get("weight_name")
			f_fontid = font.get("layoutfont_id")
			f_available = True if font.get("webfont", None) else False
			font = Font(f_name, f_weight_name, f_fontid, f_available)
			typeface.add_font(font)

		print("Found typeface '{:s}' with {:d} fonts:".format(typeface.name, typeface.font_count))
		log_separator()
		for font in typeface.fonts:
			if font.available:
				print(font.name)
			else:
				print(font.name + " (Not downloadable)")
		log_separator()
		download_fonts(typeface)

	else:
		print("Did not find typeface.")
		log_separator()


if __name__ == "__main__":
	banner()
	if len(sys.argv) > 1:
		typeface_arg = sys.argv[1]
		if "fontshop.com/families/" not in typeface_arg:
			get_fonts(typeface_arg, is_url=False)
		else:
			get_fonts(typeface_arg, is_url=True)
	else:
		print("No font family name or URL was given.")
		log_separator()
