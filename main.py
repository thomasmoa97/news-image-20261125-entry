#!/usr/bin/env python3
"""World News, 25 November 2026 — entrypoint.

Copies the front-page image this repository ships (entry.png) into the
directory the grader names in MAKEFUN_OUTPUT_DIR, verifying the bytes on
the way in and again after the move. Standard library only: no network,
no third-party imports, no drawing at run time — the picture is already
in the repository, this program only delivers it, byte for byte.

Exit codes: 0 delivered and verified, 2 no output directory given,
3 source image missing, 4 checksum mismatch.
"""

import hashlib
import os
import sys
from pathlib import Path

# The exact bytes this repository's entry.png must have. If the picture
# is ever redrawn, this fingerprint has to be regenerated from it.
EXPECTED_SHA256 = "6b6a53e25c45afe362dacc85e07ea15a2c1190dcdeed94342e5be120459b6d58"
MAX_IMAGE_BYTES = 1_048_576
CHUNK = 1 << 16


def source_image() -> Path:
    """The image lives beside this file in the repository root."""
    here = Path(__file__).resolve().parent
    return here / "entry.png"


def fingerprint(path: Path) -> str:
    """SHA-256 of a file, streamed so memory stays flat."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            block = handle.read(CHUNK)
            if not block:
                break
            digest.update(block)
    return digest.hexdigest()


def deliver(source: Path, out_dir: Path) -> Path:
    """Stream source to out_dir/entry.png, checking the digest twice.

    Writes to a temporary sibling first and renames it into place only
    once the streamed digest matches, then re-reads the delivered file
    and checks it again, so a partial or corrupted write can never
    pass as a delivery.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    staging = out_dir / ".entry.png.tmp"
    expected_size = source.stat().st_size

    digest = hashlib.sha256()
    total = 0
    with source.open("rb") as reader, staging.open("wb") as writer:
        while True:
            block = reader.read(CHUNK)
            if not block:
                break
            total += len(block)
            digest.update(block)
            writer.write(block)

    if total > MAX_IMAGE_BYTES:
        staging.unlink(missing_ok=True)
        raise SystemExit(f"entry.png is {total} bytes, over the 1 MiB limit")
    if digest.hexdigest() != EXPECTED_SHA256:
        staging.unlink(missing_ok=True)
        raise SystemExit("source entry.png failed its checksum")

    os.replace(staging, target)

    if target.stat().st_size != expected_size:
        raise SystemExit("delivered entry.png has the wrong size")
    if fingerprint(target) != EXPECTED_SHA256:
        raise SystemExit("delivered entry.png failed its checksum")
    return target


def main(argv) -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    if not out_dir:
        print("MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 2
    if Path(out_dir).exists() and not Path(out_dir).is_dir():
        print(f"MAKEFUN_OUTPUT_DIR is not a directory: {out_dir}", file=sys.stderr)
        return 2

    source = source_image()
    if not source.is_file():
        print(f"missing source image: {source}", file=sys.stderr)
        return 3

    try:
        target = deliver(source, Path(out_dir))
    except SystemExit as problem:
        print(str(problem), file=sys.stderr)
        return 4

    print(f"delivered {target} ({target.stat().st_size} bytes, "
          f"sha256 {EXPECTED_SHA256[:16]}...)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
