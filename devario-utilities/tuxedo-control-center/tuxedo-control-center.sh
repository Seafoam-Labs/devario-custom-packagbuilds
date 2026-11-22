#!/bin/sh

# The shared Electron binary otherwise reports development mode.
export ELECTRON_FORCE_IS_PACKAGED=1
exec /usr/bin/@ELECTRON@ /usr/lib/tuxedo-control-center/app.asar "$@"
