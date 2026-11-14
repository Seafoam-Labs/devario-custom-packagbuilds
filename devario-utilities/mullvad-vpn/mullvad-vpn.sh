#!/bin/sh
export NODE_ENV=production
exec electron@_electronver@ /usr/lib/mullvad-vpn/app.asar "$@"
