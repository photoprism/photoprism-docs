#!/usr/bin/env bash

# Installs the "vale" prose linter into ./bin so that "make vale" can run it.
# Vale is OPTIONAL and only used to evaluate whether prose-style linting is worth adopting;
# it is not part of "make build" and does not gate anything.
#
# The version and the SHA-256 of each release archive are pinned below; the download is rejected
# when it does not match, so a replaced release asset cannot be installed unnoticed.
#
# Usage: scripts/install-vale.sh [destdir]

set -euo pipefail

TOOL="vale"
VERSION="3.15.2"

# SHA-256 checksums as published in vale_<version>_checksums.txt.
CHECKSUM_amd64="fc72e64454d6bd7af91905d4faebbf411bae3eec17bb572f4101311212bc0d9e"
CHECKSUM_arm64="e8240a3304e2c07b0476d30423f241a80296865cf6d2b78b128fb7e4e14cbb69"

if [[ ${1:-} == "--help" ]]; then
  echo "Usage: ${0##*/} [destdir]" 1>&2
  echo "" 1>&2
  echo "Installs ${TOOL} ${VERSION} into <destdir> (default: ./bin)." 1>&2
  exit 0
fi

DESTDIR=$(realpath "${1:-./bin}")

case $(uname -m) in
  amd64 | x86_64)
    ASSET_ARCH="64-bit"
    EXPECTED="${CHECKSUM_amd64}"
    ;;
  arm64 | aarch64)
    ASSET_ARCH="arm64"
    EXPECTED="${CHECKSUM_arm64}"
    ;;
  *)
    echo "Error: Unsupported machine architecture \"$(uname -m)\"." 1>&2
    exit 1
    ;;
esac

ASSET_NAME="${TOOL}_${VERSION}_Linux_${ASSET_ARCH}.tar.gz"
ASSET_URL="https://github.com/errata-ai/vale/releases/download/v${VERSION}/${ASSET_NAME}"
DESTBIN="${DESTDIR}/${TOOL}"

if [[ -x ${DESTBIN} ]] && "${DESTBIN}" --version 2>/dev/null | grep -q "${VERSION}"; then
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
