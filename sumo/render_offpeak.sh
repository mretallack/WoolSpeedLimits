#!/bin/bash
# Render a genuine off-peak SUMO video via sumo-gui under Xvfb + ffmpeg capture.
# Usage: ./render_offpeak.sh <config.sumo.cfg> <output.webm> [duration_secs]
set -u
CFG="$1"
OUT="$2"
DUR="${3:-197}"

DISPLAY_NUM=":99"
RES="1520x900x24"

# Kill any stale Xvfb on :99
pkill -f "Xvfb ${DISPLAY_NUM}" 2>/dev/null
sleep 1

Xvfb "${DISPLAY_NUM}" -screen 0 "${RES}" -ac +extension GLX +render -noreset &
XVFB_PID=$!
sleep 2

export DISPLAY="${DISPLAY_NUM}"
export SUMO_HOME="${SUMO_HOME:-/usr/share/sumo}"

# Start ffmpeg screen capture of the Xvfb display
ffmpeg -y -f x11grab -video_size 1520x900 -framerate 20 -i "${DISPLAY_NUM}.0" \
       -t "${DUR}" -c:v libvpx -b:v 1M -deadline realtime -cpu-used 5 \
       "${OUT}" >/dev/null 2>&1 &
FFMPEG_PID=$!
sleep 2

# Launch sumo-gui fullscreen-ish with the off-peak config
sumo-gui -c "${CFG}" --window-size 1520,900 --start --quit-on-end true \
         --delay 60 --no-step-log true >/dev/null 2>&1 &
SUMO_PID=$!

# Wait for either sim end or the capture duration
wait "${SUMO_PID}" 2>/dev/null
sleep 1

kill "${FFMPEG_PID}" 2>/dev/null
wait "${FFMPEG_PID}" 2>/dev/null
kill "${XVFB_PID}" 2>/dev/null

echo "Wrote ${OUT}"
ls -la "${OUT}"
