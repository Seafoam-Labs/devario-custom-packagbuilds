#!/bin/bash

# Forward desktop links and command-line arguments to the packaged application.
export LD_PRELOAD="/usr/lib/libsodium.so${LD_PRELOAD:+:$LD_PRELOAD}"
exec /opt/ente-auth/enteauth "$@"
