#!/bin/bash
# Fully synchronous one-shot render (no tool-level backgrounding needed).
# Internally uses & for the display/ffmpeg helpers, but the SCRIPT runs in the
# foreground and exits when done, so the calling shell sees a bounded command.
# Usage: ./render_sync.sh <config.sumo.cfg> <output.webm> [duration] [delay]
set -u
CFG="$1"; OUT="$2"; DUR="${3:-197}"; DELAY="${4:-60}"
DISPLAY_NUM=":99"; RES="1520x900x24"

pkill -f "Xvfb ${DISPLAY_NUM}" 2>/dev/null
sleep 1

# Redirect every child's stdio to /dev/null so none keep the caller's pipe open.
Xvfb "${DISPLAY_NUM}" -screen 0 "${RES}" -ac +extension GLX +render -noreset \
     -nolisten unix -listen tcp </dev/null >/dev/null 2>&1 &
XVFB_PID=$!
sleep 3

export DISPLAY="${DISPLAY_NUM}"
export SUMO_HOME="${SUMO_HOME:-/usr/share/sumo}"

ffmpeg -y -f x11grab -video_size 1520x900 -framerate 20 -i "${DISPLAY_NUM}.0" \
       -t "${DUR}" -c:v libvpx -b:v 1M -deadline realtime -cpu-used 5 \
       "${OUT}" </dev/null >/dev/null 2>&1 &
FFMPEG_PID=$!
sleep 2

sumo-gui -c "${CFG}" --window-size 1520,900 --start --quit-on-end true \
         --delay "${DELAY}" --no-step-log true </dev/null >/dev/null 2>&1
sleep 1

kill "${FFMPEG_PID}" 2>/dev/null
wait "${FFMPEG_PID}" 2>/dev/null
kill "${XVFB_PID}" 2>/dev/null
wait "${XVFB_PID}" 2>/dev/null
echo "wrote ${OUT} ($(stat -c%s "${OUT}" 2>/dev/null || echo 0) bytes)"
