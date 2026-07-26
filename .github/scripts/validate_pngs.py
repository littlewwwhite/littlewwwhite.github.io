#!/usr/bin/env python3
"""Validate PNG integrity without rejecting unknown ancillary chunks."""

from __future__ import annotations

import binascii
import struct
import sys
import zlib
from pathlib import Path

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


class InvalidPng(ValueError):
    pass


def validate_png(path: Path) -> None:
    data = path.read_bytes()
    if not data.startswith(PNG_SIGNATURE):
        raise InvalidPng("missing PNG signature")

    offset = len(PNG_SIGNATURE)
    inflater: zlib.Decompress | None = None
    saw_idat = False
    saw_iend = False

    while offset < len(data):
        if offset + 12 > len(data):
            raise InvalidPng("truncated chunk header")

        length = struct.unpack_from(">I", data, offset)[0]
        chunk_type = data[offset + 4 : offset + 8]
        chunk_start = offset + 8
        chunk_end = chunk_start + length
        crc_end = chunk_end + 4

        if crc_end > len(data):
            raise InvalidPng(f"truncated {chunk_type.decode('ascii', 'replace')} chunk")

        chunk_data = data[chunk_start:chunk_end]
        expected_crc = struct.unpack_from(">I", data, chunk_end)[0]
        actual_crc = binascii.crc32(chunk_type)
        actual_crc = binascii.crc32(chunk_data, actual_crc) & 0xFFFFFFFF
        if actual_crc != expected_crc:
            raise InvalidPng(
                f"CRC mismatch in {chunk_type.decode('ascii', 'replace')} chunk"
            )

        if chunk_type == b"IDAT":
            saw_idat = True
            if inflater is None:
                inflater = zlib.decompressobj()
            try:
                inflater.decompress(chunk_data)
            except zlib.error as error:
                raise InvalidPng(f"invalid IDAT stream: {error}") from error
        elif chunk_type == b"IEND":
            if length != 0:
                raise InvalidPng("IEND chunk must be empty")
            saw_iend = True
            break

        offset = crc_end

    if not saw_idat or inflater is None:
        raise InvalidPng("missing IDAT chunk")
    if not saw_iend:
        raise InvalidPng("missing IEND chunk")

    try:
        inflater.flush()
    except zlib.error as error:
        raise InvalidPng(f"invalid IDAT stream: {error}") from error
    if not inflater.eof:
        raise InvalidPng("incomplete IDAT stream")


def iter_pngs(inputs: list[Path]):
    for item in inputs:
        candidates = item.rglob("*") if item.is_dir() else (item,)
        for path in candidates:
            if path.is_file():
                with path.open("rb") as file:
                    if file.read(8) == PNG_SIGNATURE:
                        yield path


def main() -> int:
    inputs = [Path(value) for value in sys.argv[1:]]
    if not inputs:
        print("usage: validate_pngs.py PATH [PATH ...]", file=sys.stderr)
        return 2

    failures: list[tuple[Path, str]] = []
    count = 0
    for path in iter_pngs(inputs):
        count += 1
        try:
            validate_png(path)
        except InvalidPng as error:
            failures.append((path, str(error)))

    if failures:
        for path, error in failures:
            print(f"{path}: {error}", file=sys.stderr)
        print(f"Failed: {len(failures)} of {count} PNG files", file=sys.stderr)
        return 1

    print(f"Validated {count} PNG files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
