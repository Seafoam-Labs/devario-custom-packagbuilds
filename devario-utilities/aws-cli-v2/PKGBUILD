# Maintainer: Carl Smedstad <carsme@archlinux.org>
# Contributor: Chih-Hsuan Yen <yan12125@archlinux.org>
# Contributor: Marcel Campello <marcel.campello@prafrentex.com.br>
# Contributor: David Birks <david@birks.dev>

pkgname=aws-cli-v2
pkgver=2.37.9
pkgrel=1
pkgdesc='Universal Command Line Interface for Amazon Web Services (version 2)'
arch=('any')
url="https://docs.aws.amazon.com/cli"
_url="https://github.com/aws/aws-cli"
license=('Apache-2.0')
depends=(
  'python'
  'python-awscrt'
  'python-colorama'
  'python-dateutil'
  'python-distro'
  'python-docutils'
  'python-jmespath'
  'python-prompt_toolkit'
  'python-ruamel-yaml'
  'python-urllib3'
)
makedepends=(
  'git'
  'python-build'
  'python-flit-core'
  'python-installer'
  'python-wheel'
)
checkdepends=(
  'python-jsonschema'
  'python-pytest'
  'python-pytest-xdist'
)
provides=(aws-cli)
conflicts=(aws-cli)
install=$pkgname.install
source=(
  "git+$_url#tag=$pkgver"
  "$pkgname-python-prompt-toolkit-3.0.52-compat.patch"
  "$pkgname-pytest-9.1-compat.patch"
)
b2sums=('9ddd398c7e7e9f6de6a897265eb28687e499062c2233f28c570aaf7630863b966883b5d9355e18efcdc11a26c8eeeba034738cd295b3ef72d277f7fa7b2b96a1'
        'd6c778ff47b20a9f48b80931c6972033dca30caff71edd189c4ee857cb911f65c0618b3396ac63f3d57034e3a1f87d34b4e0201bd684715fd5e348c57369c252'
        '8ed841cd47fa04082fe766388492bd2dff69a7ee3642be640301c64adfa5eca2223cca531fbfedcaf7828fd3dc037ed2d068e8f004afd42be3c0b0c9f309b5d6')

prepare() {
  cd ${pkgname%-v2}
  # Fix for python-prompt-toolkit 3.0.52
  patch -Np1 -f < ../$pkgname-python-prompt-toolkit-3.0.52-compat.patch

  # Materialize parametrized test cases for pytest 9.1.
  patch -Np1 < ../$pkgname-pytest-9.1-compat.patch
}

build() {
  cd ${pkgname%-v2}
  python -m build --wheel --no-isolation --skip-dependency-check
}

check() {
  cd ${pkgname%-v2}
  local pytest_args=(
    -vv
    --numprocesses=auto

    # Not relevant to test build back-end and dependency versions, plus these
    # tests take forever and fills up /tmp.
    --ignore=tests/backends
    --ignore=tests/dependencies
    # Takes forever (15+ minutes) to collect.
    --ignore=tests/functional
    # Requires localstub, which is not packaged.
    --ignore=tests/blackbox

    # Depends on urllib3 internals and fails with urllib3 2.X.
    --deselect=tests/unit/botocore/test_awsrequest.py::TestAWSHTTPConnection::test_expect_100_continue_returned
    --deselect=tests/unit/botocore/test_awsrequest.py::TestAWSHTTPConnection::test_expect_100_sends_connection_header
    --deselect=tests/unit/botocore/test_awsrequest.py::TestAWSHTTPConnection::test_expect_100_continue_sends_307
    --deselect=tests/unit/botocore/test_awsrequest.py::TestAWSHTTPConnection::test_handles_expect_100_with_different_reason_phrase
    --deselect=tests/unit/botocore/test_awsrequest.py::TestAWSHTTPConnection::test_expect_100_continue_no_response_from_server
    --deselect=tests/unit/botocore/test_awsrequest.py::TestAWSHTTPConnection::test_state_reset_on_connection_close

    # Fails with:
    # FileNotFoundError: [Errno 2] No such file or directory: 'temp_creds.csv'
    --deselect=tests/unit/customizations/configure/test_importer.py::TestConfigureImportCommand::test_csv_content_from_file_succeeds

    # Calls AWS services and requires credentials.
    --deselect=tests/integration/botocore/test_apigateway.py
    --deselect=tests/integration/botocore/test_client.py
    --deselect=tests/integration/botocore/test_cloudwatch.py
    --deselect=tests/integration/botocore/test_cognito_identity.py
    --deselect=tests/integration/botocore/test_credentials.py
    --deselect=tests/integration/botocore/test_ec2.py
    --deselect=tests/integration/botocore/test_elastictranscoder.py
    --deselect=tests/integration/botocore/test_emr.py
    --deselect=tests/integration/botocore/test_glacier.py
    --deselect=tests/integration/botocore/test_rds.py
    --deselect=tests/integration/botocore/test_route53.py
    --deselect=tests/integration/botocore/test_s3.py
    --deselect=tests/integration/botocore/test_session.py
    --deselect=tests/integration/botocore/test_smoke.py
    --deselect=tests/integration/botocore/test_sts.py
    --deselect=tests/integration/botocore/test_waiters.py
    --deselect=tests/integration/customizations/s3/test_filegenerator.py
    --deselect=tests/integration/customizations/s3/test_plugin.py
    --deselect=tests/integration/customizations/test_waiters.py
    --deselect=tests/integration/customizations/test_waiters.py
    --deselect=tests/integration/s3transfer
    --deselect=tests/integration/test_assume_role.py
    --deselect=tests/integration/test_cli.py
    --deselect=tests/integration/test_ec2.py
    --deselect=tests/integration/test_smoke.py::test_can_make_success_request

    # Fails for some reason
    --deselect=tests/integration/test_smoke.py::test_display_error_message

    # Fails due to Python 3.14 reference counting changes.
    --deselect=tests/unit/botocore/test_utils.py::test_lru_cache_weakref

    # Fails with AWS_ERROR_SYS_CALL_FAILURE when creating CRT EventLoopGroup
    # in the build environment.
    --deselect='tests/unit/s3transfer/test_crt.py::TestCreateS3CRTClient::test_fio_options[fio_options2-False-0.0-True]'
    --deselect='tests/unit/s3transfer/test_crt.py::TestCreateS3CRTClient::test_fio_options[fio_options3-True-8-False]'
    --deselect='tests/unit/s3transfer/test_crt.py::TestCreateS3CRTClient::test_fio_options[fio_options4-True-0.0-True]'
  )
  export AWS_ACCESS_KEY_ID=fake_id
  export AWS_SECRET_ACCESS_KEY=fake_key
  python -m venv --system-site-packages test-env
  test-env/bin/python -m installer dist/*.whl
  PATH="$PWD/test-env/bin:$PATH" \
    test-env/bin/python -m pytest "${pytest_args[@]}"
}

package() {
  cd ${pkgname%-v2}
  python -m installer --destdir="$pkgdir" dist/*.whl
  install -vDm644 bin/aws_bash_completer "$pkgdir/usr/share/bash-completion/completions/aws"
  rm -v "$pkgdir/usr/bin/aws.cmd"
  rm -v "$pkgdir/usr/bin/aws_bash_completer"
}
