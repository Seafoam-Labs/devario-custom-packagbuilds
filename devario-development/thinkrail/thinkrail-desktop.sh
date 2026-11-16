#!/bin/sh
# ThinkRail desktop launcher.
#
# Electrobun's Linux UI host is X11-only, so the desktop app renders through
# XWayland even on Wayland sessions. On NVIDIA systems WebKitGTK's DMABUF
# renderer then fails to create GBM buffers and the window stays black
# ("Failed to create GBM buffer ... Invalid argument", GLXBadWindow).
# WebKitGTK disables the DMABUF renderer whenever WEBKIT_DISABLE_DMABUF_RENDERER
# is set to anything other than "0", falling back to the pre-DMABUF path,
# which renders correctly. Export WEBKIT_DISABLE_DMABUF_RENDERER=0 to use
# the DMABUF renderer anyway (working GPUs, better WebGL performance).
export WEBKIT_DISABLE_DMABUF_RENDERER="${WEBKIT_DISABLE_DMABUF_RENDERER:-1}"
exec /usr/lib/thinkrail-desktop/bin/launcher "$@"
