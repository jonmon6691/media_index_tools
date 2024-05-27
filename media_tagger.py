#!/usr/bin/env python3
import sys
import csv
import re
import datetime

this_year = datetime.datetime.now().year

ext_filter = ["divx", "mpg", "flv", "m4v", "VOB", "sfv", "wmv", "mp4", "mkv", "avi"]

out = csv.writer(sys.stdout)
for path in sys.stdin:
	path = path.strip()
	words = [path] + re.split("[/.()[\]_ -]+", path)
	ext = words[-1]

	if ext not in ext_filter:
		continue
		
	tags = [''] * len(words)

	tags[0] = 'm' # Movie until proven otherwise
	for i, word in enumerate(words):
		if word.isdecimal() and 1850 < int(word) <= this_year:
			tags[i] = 'y'
	
		if re.match("[Ss]?\d{1,2}[EeXx]\d{1,2}[ab]?$", word):
			tags[i] = 'st'
			tags[0] = 't' # Must be a tv show

	out.writerow(words)
	out.writerow(tags)

