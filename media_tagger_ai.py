#!/usr/bin/env python3
import sys
import pathlib
import classifier
import os
import time

ext_filter = [".divx", ".mpg", ".flv", ".m4v", ".VOB", ".sfv", ".wmv", ".mp4", ".mkv", ".avi"]

quota_per_min = 5

mkdir_commands = set()
link_commands = []

for path in sys.stdin:
	source = pathlib.PurePath(path.strip())

	# Skip non-video files
	if source.suffix.strip() not in ext_filter:
		continue

	try:
		# AI magic
		ai = classifier.classify_torrent(source.name.strip())
		# Rate limit
		time.sleep(60/quota_per_min)
	except Exception as e:
		print(f"# Failed to classify {source.name.strip()} due to {type(e)}")
		continue

	target = pathlib.Path(f"/tank/multimedia/links/") / ai
	mkdir_commands.add(f'mkdir -p "{target.parent}"')
	link_commands.append(f'ln -sv "{os.path.relpath(source, target.parent)}" "{target}" 2>/dev/null')

for cmd in mkdir_commands:
	print(cmd)

for cmd in link_commands:
	print(cmd)
