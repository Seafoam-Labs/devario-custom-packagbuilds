#!/usr/bin/env fish
# Run as the repository/signing-key owner, with Remora's worker stopped.
# Usage: fish import-arch-hipblaslt.fish /repo/x86_64/devario-libs.db.tar.gz KEY_FINGERPRINT
# GNUPGHOME may be set to the existing repository signing keyring.
# Set SKIP_ARCH_SIGNATURE=1 to bypass Arch verification; Devario signing still runs.

function die
    printf 'Error: %s\n' "$argv" >&2
    exit 1
end

if test (count $argv) -ne 2
    echo 'Usage: fish import-arch-hipblaslt.fish /repo/x86_64/devario-libs.db.tar.gz KEY_FINGERPRINT' >&2
    exit 2
end

set -l skip_arch_signature 0
if set -q SKIP_ARCH_SIGNATURE; and test "$SKIP_ARCH_SIGNATURE" = 1
    set skip_arch_signature 1
end

for tool in curl gpg bsdtar shelly realpath mktemp install cmp
    command -q $tool; or die "Missing required command: $tool"
end

set -l db (realpath -e -- "$argv[1]"); or die 'Repository database does not exist.'
set -l key "$argv[2]"
set -l repo_dir (dirname -- "$db")
set -l db_name (basename -- "$db")
string match -rq '^devario-libs\.db\.tar\.(gz|xz|zst)$' -- "$db_name"; or die 'Use the existing devario-libs.db.tar.gz/xz/zst database.'
test -w "$repo_dir"; or die 'Run as an account with write access to the binary repository.'
if command -q systemctl
    if systemctl is-active --quiet remora.service
        die 'Stop remora.service before importing, to avoid concurrent repository publication.'
    end
end

set -l arch_keyring /usr/share/pacman/keyrings/archlinux.gpg
if test "$skip_arch_signature" = 0
    command -q gpgv; or die 'Missing required command: gpgv'
    test -r "$arch_keyring"; or die 'Install/update archlinux-keyring first.'
end
gpg --batch --list-secret-keys -- "$key" >/dev/null; or die 'Repository signing key is unavailable; check the account and GNUPGHOME.'

# Pin the binary to the ROCm version used by the native recipe.
set -l filename hipblaslt-7.2.4-1-x86_64.pkg.tar.zst
set -l url "https://archive.archlinux.org/packages/h/hipblaslt/$filename"
set -l cache_root "$HOME/.cache"
if set -q XDG_CACHE_HOME; and test -n "$XDG_CACHE_HOME"
    set cache_root "$XDG_CACHE_HOME"
end
set -l cache "$cache_root/devario-arch-stopgap"
mkdir -p -- "$cache"; or die 'Cannot create download cache.'
echo "Downloading $filename (about 1.6 GB; interrupted downloads can resume)..."
curl --fail --location --retry 3 --continue-at - --output "$cache/$filename" "$url"; or die 'Package download failed; rerun to resume.'
if test "$skip_arch_signature" = 1
    echo 'Skipping Arch signature verification (SKIP_ARCH_SIGNATURE=1).'
else
    curl --fail --location --retry 3 --output "$cache/$filename.arch.sig" "$url.sig"; or die 'Signature download failed.'
    gpgv --keyring "$arch_keyring" "$cache/$filename.arch.sig" "$cache/$filename"; or die 'Arch signature verification failed.'
end

set -l info (bsdtar -xOf "$cache/$filename" .PKGINFO); or die 'Cannot read package metadata.'
contains -- 'pkgname = hipblaslt' $info; or die 'Unexpected package name.'
contains -- 'pkgver = 7.2.4-1' $info; or die 'Unexpected package version.'
contains -- 'arch = x86_64' $info; or die 'Unexpected package architecture.'
echo 'Dependencies (must be satisfied by the repository):'
string match 'depend = *' -- $info

# Preserve all other entries; build and sign the database pair before publishing.
set -l stage (mktemp -d "$repo_dir/.hipblaslt-import.XXXXXX"); or die 'Cannot create staging directory.'
set -g hipblaslt_import_stage "$stage"
function cleanup_hipblaslt_import --on-event fish_exit
    if set -q hipblaslt_import_stage; and test -d "$hipblaslt_import_stage"
        rm -rf -- "$hipblaslt_import_stage"
    end
end
set -l files_name (string replace '.db.tar.' '.files.tar.' -- "$db_name")
for name in "$db_name" "$files_name"
    if test -f "$repo_dir/$name"
        cp -- "$repo_dir/$name" "$stage/$name"; or die 'Cannot stage repository metadata.'
    end
end
install -m 644 -- "$cache/$filename" "$stage/$filename"; or die 'Cannot stage package.'
# Re-sign the unchanged Arch archive with the existing Devario key.
gpg --detach-sign --local-user "$key" --output "$stage/$filename.sig" "$stage/$filename"; or die 'Package signing failed.'
shelly repo-db add --sign --key "$key" "$stage/$db_name" "$stage/$filename"; or die 'Repository update failed.'

if test -e "$repo_dir/$filename"
    cmp -s -- "$stage/$filename" "$repo_dir/$filename"; or die 'A different archive with the same filename already exists.'
end
for name in "$filename" "$filename.sig" "$db_name" "$db_name.sig" "$files_name" "$files_name.sig"
    test -f "$stage/$name"; or die "Missing staged artifact: $name"
    chmod 644 -- "$stage/$name"; or die 'Cannot make staged artifact readable.'
end
if command -q systemctl
    if systemctl is-active --quiet remora.service
        die 'Remora restarted during the download; stop its worker before importing.'
    end
end
# Retain the staged files for recovery if a publication rename fails.
set -e hipblaslt_import_stage
for name in "$filename" "$filename.sig" "$db_name" "$db_name.sig" "$files_name" "$files_name.sig"
    mv -f -- "$stage/$name" "$repo_dir/$name"; or die "Publication failed at $name; recovery files remain in $stage."
end
rm -rf -- "$stage"
echo "Added $filename to $db"
echo 'Restart the Remora worker and request the normal mirror sync if applicable.'
echo 'This imports the Arch binary as-is; it does not use the custom GPU target list or disable rocRoller.'
