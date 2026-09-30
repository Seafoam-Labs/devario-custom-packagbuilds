#!/usr/bin/env bash
# Run inside the same isolated root that will build compiler-rt21.
set -euo pipefail

workdir=$(mktemp -d)
trap 'rm -rf "$workdir"' EXIT

cat > "$workdir/probe.c" <<'EOF'
#include <stdio.h>
#include <pthread.h>
_Static_assert(sizeof(void *) == 4, "expected 32-bit pointers");
static void *worker(void *value) { return value; }
int main(void) {
  pthread_t thread;
  if (pthread_create(&thread, NULL, worker, NULL)) return 1;
  if (pthread_join(thread, NULL)) return 1;
  puts("32-bit C and pthreads work");
  return 0;
}
EOF

cat > "$workdir/probe.cpp" <<'EOF'
#include <iostream>
#include <stdexcept>
#include <thread>
static_assert(sizeof(void *) == 4, "expected 32-bit pointers");
int main() {
  std::thread worker([] {});
  worker.join();
  try { throw std::runtime_error("32-bit C++ and unwinding work"); }
  catch (const std::exception &error) { std::cout << error.what() << '\n'; }
}
EOF

# Arguments select compiler executables; defaults match the GCC bootstrap.
"${1:-gcc}" -m32 -pthread "$workdir/probe.c" -o "$workdir/probe-c"
"${2:-g++}" -m32 -pthread -std=c++17 "$workdir/probe.cpp" -o "$workdir/probe-cxx"
for binary in "$workdir/probe-c" "$workdir/probe-cxx"; do
  LC_ALL=C readelf -h "$binary" | grep -Eq 'Class:[[:space:]]+ELF32'
  "$binary"
done
