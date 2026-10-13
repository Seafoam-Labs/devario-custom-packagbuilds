#!/usr/bin/bash
# SPDX-License-Identifier: GPL-3.0-or-later
set -euo pipefail
if (( $# != 3 )); then
  echo 'Usage: test-theme.sh PLYMOUTH_SOURCE PLYMOUTH_BUILD OUTPUT_DIRECTORY' >&2
  exit 64
fi
source_dir="$(realpath "$1")"
export DEVARIO_PLYMOUTH_BUILD="$(realpath "$2")"
mkdir -p "$3"
output_dir="$(realpath "$3")"
theme_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
export LD_LIBRARY_PATH="$DEVARIO_PLYMOUTH_BUILD/src/libply:$DEVARIO_PLYMOUTH_BUILD/src/libply-splash-core:$DEVARIO_PLYMOUTH_BUILD/src/libply-splash-graphics${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
cc -Wall -Wextra -Werror -rdynamic \
  -I"$source_dir/src/libply" -I"$source_dir/src/libply-splash-core" \
  -I"$source_dir/src/libply-splash-graphics" -I"$source_dir/src/plugins/splash/script" \
  "$theme_dir/test-theme.c" "$DEVARIO_PLYMOUTH_BUILD/src/plugins/splash/script/script.so" \
  -L"$DEVARIO_PLYMOUTH_BUILD/src/libply" -lply \
  -L"$DEVARIO_PLYMOUTH_BUILD/src/libply-splash-core" -lply-splash-core \
  -L"$DEVARIO_PLYMOUTH_BUILD/src/libply-splash-graphics" -lply-splash-graphics \
  -ldl -lpng -o "$output_dir/test-theme"
cd "$output_dir"
./test-theme "$theme_dir/devario.script" "$theme_dir"
