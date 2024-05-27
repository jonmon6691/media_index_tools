#!/usr/bin/env python3
""" WARNING: This is a pile of shit """
# I made this to do a bulk job ONCE. no attempt at usability or generality
#       "Your AI is just a bunch of if statements" -Anonymous

# Implements the naming schemes:
#  https://www.plexopedia.com/plex-media-server/general/organize-movie-files-plex/
#  https://support.plex.tv/articles/naming-and-organizing-your-tv-show-files/


__usage__ = """

cat tags.csv | ./media_linker.py > links.sh

"""

import sys
import csv
import os
import re
from collections import defaultdict

def matches(words, tags, tag):
    # Filters [words] based on locations of "tag" in [tags]
    parts = []
    for i, t in enumerate(tags):
        if t == tag:
            parts.append(words[i])
    return parts

def build_name(parts):
    # basically a " ".join(parts) but if there's a 
    #   single "s", it gets added to the last word
    name = ""
    for part in parts:
        if part != 's' and len(name) != 0:
            name += ' '
        name += part
    return name.title()

table = csv.reader(sys.stdin)

# Holds the indexes of words that make up the names
#   global because if name indexes arent updated, then previous ones are used
name_parts = []

# Directories that have to be created with mkdir
dirs = set()

# Holds the mapping of links for the ln command to be run with
# "Generated link name" -> [[csv line number, "original file"], [csv line number, "duplicate original file"]]
links = defaultdict(list)

while True:
    try:
        words = next(table)
        tags = next(table)
    except StopIteration:
        break

    orig_path = words[0]
    ext = os.path.splitext(orig_path)[-1]
    mtype = tags[0]

    if 'n' in tags: # Update the name parts, otherwise the old ones will be used
        name_parts = tags

    # Build the name up using name_parts indexes
    name = build_name(matches(words, name_parts, 'n'))

    # Set the year if it was found
    year = matches(words, tags, 'y')
    if len(year) > 0:
        if year[0].isdecimal() and 1850 < int(year[0]) < 2100:
            year = f" ({year[0]})"
        else:
            sys.stderr.write(f"{table.line_num} Error: Year: {year[0]} {name}")
    else:
        year = ''

    # Process part1, part2, etc tags
    part_tag = ''
    parts = matches(words, tags, 'pt')
    if len(parts) > 0:
        part_tag = f" - part{parts[0]}"

    # Holds the output link name
    new_path = ""

    if mtype == 't': # TV Show
        season = ''
        episode = ''
        special_name = ''

        season_tag = sorted(list(map(str.upper, matches(words, tags, 'st'))))
        if len(season_tag) > 0:
            season_tag = season_tag[0]
            std_tag = re.match("S(\d{1,2})EP?(\d{1,2})$", season_tag) # S06E14
            num_tag = re.match("^(\d{1,2})$", season_tag) # 6
            x_tag = re.match("^(\d+)X(\d+)$", season_tag) # 6X14
            three_tag = re.match("^(\d)(\d\d[AB]?)$", season_tag) # 614
            four_tag = re.match("^(\d\d)(\d\d)$", season_tag) # 0614

            if std_tag:
                season = std_tag.group(1)
                episode = std_tag.group(2)
            elif num_tag:
                season = num_tag.group(1)
            elif x_tag:
                season = x_tag.group(1)
                episode = x_tag.group(2)
            elif three_tag:
                season = three_tag.group(1)
                episode = three_tag.group(2)
            elif four_tag:
                season = four_tag.group(1)
                episode = four_tag.group(2)
            else:
                sys.stderr.write(f"{table.line_num} Error: Season tag: {season_tag} {name}")
        
        special_tag = matches(words, tags, 'sp')
        if len(special_tag) > 0:
            season = '00'
            special_name = build_name(special_tag)
            episode = build_name(matches(words, tags, 'spn'))

        if episode == '':
            eps = matches(words, tags, 'ep')
            if len(eps) == 1:
                episode = re.search("(\d+)", eps[0])
                episode = episode.group(1)
            else:
                print(f"{table.line_num} Error: No Episode: {name} [Season {season}]")

        if season == '' and special_name == '':
            season = '01'
        
        if special_name == '':
            season = f"{int(season):02d}"
            try:
                episode = f"{int(episode):02d}"
            except ValueError:
                pass
            new_path = f"TV Shows/{name}/Season {season}/{name}{year} - s{season}e{episode}{part_tag}{ext}"
        else:
            new_path = f"TV Shows/{name}/Specials/{special_name}/{name}{year} - {episode}{part_tag}{ext}"
        
    elif mtype == 'm': # Movie
        #Easy peasy
        new_path = f"Movies/{name}{year}{part_tag}{ext}"
    else:
        continue
    
    new_path = f"/tank/multimedia/links/{new_path}"
    dirs.add(os.path.dirname(new_path))
    links[new_path].append([table.line_num, orig_path])


for folder in dirs:
    print("mkdir", "-p", f'"{folder}"')


for src in sorted(links.keys()):
    dsts = links[src]
    dst = dsts[0]
    if len(dsts) > 1:
        sizes = list(map(lambda x: os.stat(x[1]).st_size, dsts))
        dst = dsts[sizes.index(max(sizes))]
    print("ln", "-sv", f'"{os.path.relpath(dst[1],os.path.dirname(src))}"', f'"{src}"', "2>/dev/null")
