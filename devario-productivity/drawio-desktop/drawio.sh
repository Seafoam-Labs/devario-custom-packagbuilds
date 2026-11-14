#!/bin/sh -eu

export NODE_ENV=production
exec electron@_electronver@ /usr/lib/drawio-desktop/app.asar "$@"
