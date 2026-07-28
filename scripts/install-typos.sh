#!/usr/bin/env bash

# Installs the "typos" source-code spell checker into ./bin so that "make spellcheck" can run it.
# The version and the SHA-256 of each release archive are pinned below; the download is rejected
# when it does not match, so a replaced release asset cannot be installed unnoticed.
#
# Usage: scripts/install-typos.sh [destdir]

set -euo pipefail

TOOL="typos"
VERSION="v1.48.0"

# SHA-256 checksums of the pinned release archives (crate-ci/typos publishes no checksums file).
CHECKSUM_amd64="72a930c9a94fc3914aa56835c5b859c892a797d40c1c42638b98d93f16ff519c"
CHECKSUM_arm64="2960ae07bc1ffe19e4895e4359394dd349c9c31de78aac3a124b6e4aeb206698"

if [[ ${1:-} == "--help" ]]; then
  echo "Usage: ${0##*/} [destdir]" 1>&2
  echo "" 1>&2
  echo "Installs ${TOOL} ${VERSION} into <destdir> (default: ./bin)." 1>&2
  exit 0
fi

DESTDIR=$(realpath "${1:-./bin}")

case $(uname -m) in
  amd64 | x86_64)
    ASSET_ARCH="x86_64"
    EXPECTED="${CHECKSUM_amd64}"
    ;;
  arm64 | aarch64)
    ASSET_ARCH="aarch64"
    EXPECTED="${CHECKSUM_arm64}"
    ;;
  *)
    echo "Error: Unsupported machine architecture \"$(uname -m)\"." 1>&2
    exit 1
    ;;
esac

ASSET_NAME="${TOOL}-${VERSION}-${ASSET_ARCH}-unknown-linux-musl.tar.gz"
ASSET_URL="https://github.com/crate-ci/typos/releases/download/${VERSION}/${ASSET_NAME}"
DESTBIN="${DESTDIR}/${TOOL}"

if [[ -x ${DESTBIN} ]] && "${DESTBIN}" --version 2>/dev/null | grep -q "${VERSION#v}"; then
  echo "${TOOL} ${VERSION} is already installed in \"${DESTDIR}\"."
  exit 0
fi

echo "--------------------------------------------------------------------------------"
echo "VERSION  : ${VERSION}"
echo "DOWNLOAD : ${ASSET_URL}"
echo "DESTBIN  : ${DESTBIN}"
echo "--------------------------------------------------------------------------------"

tmp_dir=$(mktemp -d)
trap 'rm -rf "${tmp_dir}"' EXIT

curl --fail --silent --show-error --location "${ASSET_URL}" -o "${tmp_dir}/${ASSET_NAME}"

ACTUAL=$(sha256sum "${tmp_dir}/${ASSET_NAME}" | awk '{print $1}')

if [[ ${EXPECTED} != "${ACTUAL}" ]]; then
  echo "Error: SHA-256 mismatch for ${ASSET_NAME}." 1>&2
  echo "  expected: ${EXPECTED}" 1>&2
  echo "  actual:   ${ACTUAL}" 1>&2
  exit 1
fi

echo "Checksum OK (${ACTUAL})."

tar -xzf "${tmp_dir}/${ASSET_NAME}" -C "${tmp_dir}"

if [[ ! -f "${tmp_dir}/${TOOL}" ]]; then
  echo "Error: ${TOOL} binary not found inside ${ASSET_NAME}." 1>&2
  exit 1
fi

mkdir -p "${DESTDIR}"
install -m 755 "${tmp_dir}/${TOOL}" "${DESTBIN}"

"${DESTBIN}" --version

echo "Done."
