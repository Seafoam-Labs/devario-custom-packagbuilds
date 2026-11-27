#!/bin/bash

# The shell runs data/server.js with Node and reads its location from the
# environment; the private copy lives beside the binary in /usr/lib/stremio.
export SERVER_PATH=/usr/lib/stremio/server.js
# Enable Intel ANV Vulkan video decode/encode, matching upstream's
# .cargo/config.toml. Other drivers ignore the variable.
export ANV_DEBUG="${ANV_DEBUG:-video-decode,video-encode}"
# D-Bus activation can start the service with a minimal environment; prefer the
# packaged node from /usr/bin over any user toolchain.
export PATH="/usr/bin${PATH:+:$PATH}"

exec /usr/lib/stremio/stremio "$@"
