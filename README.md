# media_index_tools
Scripts used to build a PLEX-compatible media index out of symlinks

![screenshot of tree command](docs/tree_example.png)

Plex likes to have things... a certain way. Look, I'm just not that
organized, okay! I have a decade or so of content that I've finally cobbled
together from hard drives and machines that have long since been
relegated to nooks and corners. May be you do too? Well now that it's
all in one place, I might as well watch some of it. People told me:
"Use PLEX Jon!", so sure, if its good software, I should be able to
point it at my "data swamp" and let magic take care of the rest.
Nope. No PLEX has a specific structure it would very much like you to
use, and sure you can try the easy way, but its just not that good.

But here's the thing. I'm not doing this manually, and honestly,
I don't want to be mv'ing things all over the place, what if I
screw up? What if I wan't to change the way its organized?

So the idea is to have a tree structure parallel to the data swamp,
organized just how PLEX likes it, and the leaves of this tree?
Symlinks. That's it. Anyway, I like this idea, and it worked out
good for me and I think it will work going forward too.

# How does it work?

1. Transmission Client finished downloading something
2. It calls transmission_target.sh with env vars that describe the torrent
3. The script passes all the files in the torrent directory to media_tagger_ai.py
4. The python script wraps an AI prompt to convert the torrent files names into sensible paths
5. This works unreasonably well
6. The python script prints the commands necessary to so the linking
7. Its up to you to run them, or do it automatically. What could go wrong?

# Installation

1. Get a google cloud account and set everything up
    1. https://cloud.google.com/sdk/docs/install
    2. `pip install --upgrade google-cloud-aiplatform`
    3. `gcloud auth application-default login`
2. Add the `transmission_target_ai.sh` script to Transmission Client
    1. Edit -> Preferences -> Downloading -> Check "Call script...", then choose the script

