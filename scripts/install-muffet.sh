#!/usr/bin/env bash

# Installs the "muffet" link checker into ./bin so that "make muffet" can run it.
#
# muffet crawls a *served* site over HTTP and, unlike "make check-links", it also
# validates in-page anchors. Point it at a local preview rather than production, so
# checks do not show up in the live access logs. The two tools are complementary:
# check-links resolves references against files on disk before anything is published,
# muffet exercises the rendered site as a browser would.
#
# The version and the SHA-256 of each release archive are pinned below; the download is
# rejected when it does not match, so a replaced release asset cannot be installed
# unnoticed. This mirrors how the other pinned tools are installed and avoids requiring
# a Go toolchain, which "go install" would.
#
# Usage: scripts/install-muffet.sh [destdir]

set -euo pipefail

TOOL="muffet"
VERSION="2.11.5"

# SHA-256 checksums as published in muffet_<version>_checksums.txt.
CHECKSUM_amd64="64d4db266f308ea7136fe8060a5061bc8a4eea3be5e36350f94a4fcea45309d2"
CHECKSUM_arm64="3b68e4ad8c857088dd9bd071b97f32a8d20c84c88e470031fc11c97381d63984"

if [[ ${1:-} == "--help" ]]; then
  echo "Usage: ${0##*/} [destdir]" 1>&2
  echo "" 1>&2
  echo "Installs ${TOOL} ${VERSION} into <destdir> (default: ./bin)." 1>&2
  exit 0
fi

DESTDIR=$(realpath "${1:-./bin}")

case $(uname -m) in
  amd64 | x86_64)
    ASSET_ARCH="amd64"
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

ASSET_NAME="${TOOL}_linux_${ASSET_ARCH}.tar.gz"
ASSET_URL="https://github.com/raviqqe/${TOOL}/releases/download/v${VERSION}/${ASSET_NAME}"
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
