# Maintainer: Bruno Pagani <archange@archlinux.org>
# Maintainer: Carl Smedstad <carsme@archlinux.org>

pkgname=python-fsspec
pkgver=2026.9.0
pkgrel=1
pkgdesc='Specification that python filesystems should adhere to'
arch=(any)
url='https://github.com/intake/filesystem_spec'
license=(BSD-3-Clause)
depends=(python)
makedepends=(
  git
  python-build
  python-hatch-vcs
  python-hatchling
  python-installer
  python-wheel
)
checkdepends=(
  git
  jupyter-notebook
  python-aiohttp
  python-cloudpickle
  python-dask
  python-distributed
  python-fastparquet
  # python-fusepy
  python-jinja
  python-libarchive-c
  python-lz4
  python-msgpack
  python-numpy
  python-pandas
  python-paramiko
  python-pyarrow
  python-pyftpdlib
  python-pygit2
  python-pytest
  python-pytest-asyncio
  python-pytest-mock
  python-pytest-rerunfailures
  python-pytest-vcr
  python-requests
  python-smbprotocol
  python-snappy
  python-tqdm
)
optdepends=(
  'python-aiohttp: HTTP support'
  'python-distributed: Dask support'
  'python-libarchive-c: archives support'
  'python-lz4: LZ4 compression support'
  'python-paramiko: SFTP support'
  'python-pyarrow: Arrow/Parquet support'
  'python-pygit2: git support'
  'python-requests: web protocols support'
  'python-smbprotocol: SMB support'
  'python-snappy: snappy compression support'
  'python-tqdm: progress bar support'
)
source=("$pkgname::git+$url.git#tag=$pkgver")
sha512sums=('767fce05b76f1638920ecc5fcdda75f57c9a764f360d80773aaaa898f91891a3c1feab5504464cfceeb8659a1a68000d30fe2d6fe7b025d89f07b36ec324580e')
b2sums=('950a3156857bfdafc3684fd39a8a70587ff10905344d62df41ac11206f72a99181d093f23953996f323c5e605860083fab122bcc82037b7b519f41e157c2ac9e')

build() {
  cd $pkgname
  export SETUPTOOLS_SCM_PRETEND_VERSION=$pkgver
  python -m build --wheel --no-isolation
}

check() {
  cd $pkgname
  # Deselect failing tests - I think the root cause for most of them is the
  # following requirement: "The full fsspec suite requires a system-level
  # docker, docker-compose, and fuse installation". See:
  # https://github.com/fsspec/filesystem_spec?tab=readme-ov-file#testing
  pytest \
    --deselect fsspec/implementations/tests/test_ftp.py::test_basic \
    --deselect fsspec/implementations/tests/test_ftp.py::test_ls_root_dircache \
    --deselect fsspec/implementations/tests/test_ftp.py::test_not_cached \
    --deselect fsspec/implementations/tests/test_ftp.py::test_tls \
    --deselect fsspec/implementations/tests/test_http.py \
    --deselect fsspec/implementations/tests/test_reference.py::test_defaults \
    --deselect fsspec/implementations/tests/test_reference.py::test_info \
    --deselect fsspec/implementations/tests/test_reference.py::test_simple \
    --deselect fsspec/implementations/tests/test_reference.py::test_simple_ver1 \
    --deselect fsspec/tests/test_caches.py::test_background \
    --deselect fsspec/tests/test_generic.py::test_cat_async \
    --deselect fsspec/tests/test_generic.py::test_cp_async_to_sync \
    --deselect fsspec/tests/test_generic.py::test_remote_async_ops \
    --deselect fsspec/tests/test_spec.py::test_cache_not_pickled
}

package() {
  cd $pkgname
  python -m installer --destdir="$pkgdir" dist/*.whl
  install -vDm644 -t "$pkgdir/usr/share/licenses/$pkgname" LICENSE
}
