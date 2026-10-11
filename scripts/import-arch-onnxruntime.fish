#!/usr/bin/env fish
# Run as the repository/signing-key owner, with Remora's worker stopped.
# Usage: fish import-arch-onnxruntime.fish /repo/x86_64/devario-development.db.tar.gz KEY_FINGERPRINT
# Set SKIP_ARCH_SIGNATURE=1 to bypass Arch verification; Devario signing still runs.
# Remora's SQLite state and build status are managed separately by the DB admin.

function die
    printf 'Error: %s\n' "$argv" >&2
    exit 1
end

if test (count $argv) -ne 2
    echo 'Usage: fish import-arch-onnxruntime.fish /repo/x86_64/devario-development.db.tar.gz KEY_FINGERPRINT' >&2
    exit 2
end

set -l skip_arch_signature 0
if set -q SKIP_ARCH_SIGNATURE; and test "$SKIP_ARCH_SIGNATURE" = 1
    set skip_arch_signature 1
end
for tool in curl gpg bsdtar shelly realpath mktemp install cmp systemctl
    command -q $tool; or die "Missing required command: $tool"
end

set -l db (realpath -e -- "$argv[1]"); or die 'Repository database does not exist.'
set -l key "$argv[2]"
set -l repo_dir (dirname -- "$db")
set -l db_name (basename -- "$db")
string match -rq '^devario-[a-z0-9-]+\.db\.tar\.(gz|xz|zst)$' -- "$db_name"; or die 'Use an existing devario-*.db.tar.gz/xz/zst database.'
test -w "$repo_dir"; or die 'Run as an account with write access to the binary repository.'
set -l files_name (string replace '.db.tar.' '.files.tar.' -- "$db_name")
test -f "$repo_dir/$files_name"; or die 'The matching repository .files archive is missing.'

function require_stopped_worker
    set -l state (systemctl show --property=ActiveState --value remora.service)
    or die 'Cannot check remora.service; run this on the Remora host.'
    contains -- "$state" inactive failed; or die "Stop remora.service before importing (state: $state)."
end
require_stopped_worker

set -l arch_keyring /usr/share/pacman/keyrings/archlinux.gpg
if test "$skip_arch_signature" = 0
    command -q gpgv; or die 'Missing required command: gpgv'
    test -r "$arch_keyring"; or die 'Install/update archlinux-keyring first.'
end
gpg --batch --list-secret-keys -- "$key" >/dev/null; or die 'Repository signing key is unavailable; check the account and GNUPGHOME.'

# Exact allowlist: no opt variants and no recursive dependency imports.
# Keep Arch's original release; the custom Devario 1.29.0-5 supersedes it.
set -l arch_package_version 1.29.0-3
set -l packages onnxruntime-cpu onnxruntime-cuda onnxruntime-rocm \
    python-onnxruntime-cpu python-onnxruntime-cuda python-onnxruntime-rocm
set -l cache_root "$HOME/.cache"
if set -q XDG_CACHE_HOME; and test -n "$XDG_CACHE_HOME"
    set cache_root "$XDG_CACHE_HOME"
end
set -l cache "$cache_root/devario-arch-stopgap"
mkdir -p -- "$cache"; or die 'Cannot create download cache.'
set -l filenames
echo 'Downloading six ONNX Runtime packages (about 905 MB total; interrupted downloads can resume).'
if test "$skip_arch_signature" = 1
    echo 'Skipping Arch signature verification (SKIP_ARCH_SIGNATURE=1).'
end
for package in $packages
    set -l filename "$package-$arch_package_version-x86_64.pkg.tar.zst"
    set -l initial (string sub -l 1 -- "$package")
    set -l url "https://archive.archlinux.org/packages/$initial/$package/$filename"
    curl --fail --location --retry 3 --continue-at - --output "$cache/$filename" "$url"; or die "Download failed for $package; rerun to resume."
    if test "$skip_arch_signature" = 0
        curl --fail --location --retry 3 --output "$cache/$filename.arch.sig" "$url.sig"; or die "Signature download failed: $package"
        gpgv --keyring "$arch_keyring" "$cache/$filename.arch.sig" "$cache/$filename"; or die "Arch signature verification failed: $package"
    end
    set -l info (bsdtar -xOf "$cache/$filename" .PKGINFO); or die "Cannot read package metadata: $package"
    contains -- "pkgname = $package" $info; or die "Unexpected package name: $package"
    contains -- "pkgver = $arch_package_version" $info; or die "Unexpected package version: $package"
    contains -- 'arch = x86_64' $info; or die "Unexpected package architecture: $package"
    if test -e "$repo_dir/$filename"
        cmp -s -- "$cache/$filename" "$repo_dir/$filename"; or die "A different archive with the same filename already exists: $filename"
    end
    echo "$package dependencies (must already be available to clients):"
    string match 'depend = *' -- $info
    set -a filenames "$filename"
end

# Stage all six together, preserving other database entries, before publishing.
set -l stage (mktemp -d "$repo_dir/.onnxruntime-import.XXXXXX"); or die 'Cannot create staging directory.'
set -g onnxruntime_import_stage "$stage"
function cleanup_onnxruntime_import --on-event fish_exit
    if set -q onnxruntime_import_stage; and test -d "$onnxruntime_import_stage"
        rm -rf -- "$onnxruntime_import_stage"
    end
end
for name in "$db_name" "$files_name"
    cp -- "$repo_dir/$name" "$stage/$name"; or die 'Cannot stage repository metadata.'
end
set -l staged_packages
set -l artifacts
for filename in $filenames
    install -m 644 -- "$cache/$filename" "$stage/$filename"; or die "Cannot stage package: $filename"
    gpg --detach-sign --local-user "$key" --output "$stage/$filename.sig" "$stage/$filename"; or die "Package signing failed: $filename"
    set -a staged_packages "$stage/$filename"
    set -a artifacts "$filename" "$filename.sig"
end
shelly repo-db add --sign --key "$key" "$stage/$db_name" $staged_packages; or die 'Repository update failed.'
set -a artifacts "$db_name" "$db_name.sig" "$files_name" "$files_name.sig"
for name in $artifacts
    test -f "$stage/$name"; or die "Missing staged artifact: $name"
    chmod 644 -- "$stage/$name"; or die 'Cannot make staged artifact readable.'
end
for name in $filenames "$db_name" "$files_name"
    gpg --batch --verify "$stage/$name.sig" "$stage/$name"; or die "Devario signature verification failed: $name"
end
require_stopped_worker
# Publication uses individual renames. Retain remaining files on partial failure.
set -e onnxruntime_import_stage
for name in $artifacts
    mv -f -- "$stage/$name" "$repo_dir/$name"; or die "Publication failed at $name; recovery files remain in $stage."
end
rm -rf -- "$stage"
echo "Added all six ONNX Runtime $arch_package_version packages to $db"
echo 'Have the DB admin update Remora status, then restart remora.service and request the normal mirror sync.'
echo 'Arch CPU flags, GPU targets and package metadata are unchanged; custom v3/four-target settings require a native rebuild.'
echo 'Existing opt entries are preserved; review their migration separately.'
