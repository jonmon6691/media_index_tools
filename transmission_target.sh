#!/usr/bin/env bash
TOOLS_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
if ! cd $TOOLS_DIR ; then
    logger -p daemon.err -t $0 "Can't find tools directory $TOOLS_DIR"
    exit 1
fi

if [[ -z $TR_TORRENT_DIR || -z $TR_TORRENT_NAME ]]; then
    if [[ -z $1 ]]; then
        logger -p daemon.err -t $0 "Invoked without torrent name!"
        exit 1
    else
        TPATH=$1
    fi
else
    TPATH="$TR_TORRENT_DIR/$TR_TORRENT_NAME"
fi


echo $TPATH
find "$TPATH" -type f | ./media_tagger_ai.py > last_run.sh; rv=$?
cat last_run.sh >> linking_commands.sh

# I personally review the output before running... but,
# If you're brave, uncomment to blindly run code from an LLM and save yourself the hassle
#source linking_commands.sh

# Send a pushbullet notification by lazily hooking ZFS config. Yeah, ZFS is a dependancy, so sue me
# Or if you don't care, uncomment this line to wrap it up early
#exit 0

ZED_ZEDLET_DIR="/etc/zfs/zed.d"

if [[ ! -f "pushbullet_token.sh" ]]; then
    cp "pushbullet_token.sh.template" "pushbullet_token.sh"
    logger -p daemon.err -t $0 "Pushbullet token not configured, place it in ${TOOLS_DIR}/pushbullet_token.sh"
    exit 1
fi

. "pushbullet_token.sh"

if [[ -z $ZED_PUSHBULLET_ACCESS_TOKEN ]]; then
    logger -p daemon.err -t $0 "Pushbullet token not configured, place it in ${TOOLS_DIR}/pushbullet_token.sh"
fi

# Optional channel tag can be used
#ZED_PUSHBULLET_CHANNEL_TAG=""

if [[ ! -f "${ZED_ZEDLET_DIR}/zed-functions.sh" ]]; then
    logger -p daemon.err -t $0 "ZFS not found. Can't send notification."
    exit 1
fi

. "${ZED_ZEDLET_DIR}/zed-functions.sh"

note_subject="Torrent complete"
note_pathname="$(mktemp)"
{
    echo
    echo "   Name: ${TR_TORRENT_NAME}"
    echo 
    echo "   Errors: ${rv}"

} > "${note_pathname}"

zed_notify_pushbullet "${note_subject}" "${note_pathname}"
rm -f "${note_pathname}"
