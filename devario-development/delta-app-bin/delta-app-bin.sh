#!/bin/bash

# Delta is managed by pacman; tell the built-in updater instead of letting it
# replace the root-owned bundle under /opt/delta.
export DELTA_UPDATE_EXPLANATION='Updates are handled by pacman'

# Installed as both /usr/bin/delta and /usr/bin/delta-app; dispatch on the
# invoked name so each entry point reaches its own binary in the bundle.
case "${0##*/}" in
	delta-app) exec /opt/delta/bin/delta-app "$@" ;;
	*) exec /opt/delta/bin/delta "$@" ;;
esac
