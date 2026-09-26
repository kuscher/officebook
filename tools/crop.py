#!/usr/bin/env python3
"""Crops a PNG to a rectangle, with only the standard library.

  crop.py IN.png OUT.png X Y W H

Used to keep screenshots to the app's header, so no mail content is captured.
"""
import struct
import sys
import zlib


def read_png(path):
    data = open(path, "rb").read()
    assert data[:8] == b"\x89PNG\r\n\x1a\n", "not a PNG"
    pos, idat, ihdr = 8, [], None
    while pos < len(data):
        n = struct.unpack(">I", data[pos:pos + 4])[0]
        kind, body = data[pos + 4:pos + 8], data[pos + 8:pos + 8 + n]
        if kind == b"IHDR":
            ihdr = body
        elif kind == b"IDAT":
            idat.append(body)
        pos += 12 + n
    w, h, depth, color = struct.unpack(">IIBB", ihdr[:10])
    assert depth == 8 and color in (2, 6) and ihdr[12] == 0, "only 8-bit RGB/RGBA, not interlaced"
    return w, h, {2: 3, 6: 4}[color], color, zlib.decompress(b"".join(idat))


def unfilter(raw, w, bpp, rows):
    stride = w * bpp
    out, prev = [], bytearray(stride)
    for y in range(rows):
        f = raw[y * (stride + 1)]
        line = bytearray(raw[y * (stride + 1) + 1:(y + 1) * (stride + 1)])
        if f == 1:
            for i in range(bpp, stride):
                line[i] = (line[i] + line[i - bpp]) & 0xFF
        elif f == 2:
            for i in range(stride):
                line[i] = (line[i] + prev[i]) & 0xFF
        elif f == 3:
            for i in range(stride):
                left = line[i - bpp] if i >= bpp else 0
                line[i] = (line[i] + ((left + prev[i]) >> 1)) & 0xFF
        elif f == 4:
            for i in range(stride):
                a = line[i - bpp] if i >= bpp else 0
                b = prev[i]
                c = prev[i - bpp] if i >= bpp else 0
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                pred = a if pa <= pb and pa <= pc else (b if pb <= pc else c)
                line[i] = (line[i] + pred) & 0xFF
        out.append(line)
        prev = line
    return out


def chunk(kind, body):
    return struct.pack(">I", len(body)) + kind + body + struct.pack(">I", zlib.crc32(kind + body) & 0xFFFFFFFF)


def main():
    src, dst, x, y, w, h = sys.argv[1], sys.argv[2], *map(int, sys.argv[3:7])
    width, height, bpp, color, raw = read_png(src)
    x, y = max(0, x), max(0, y)
    w, h = min(w, width - x), min(h, height - y)
    rows = unfilter(raw, width, bpp, y + h)[y:y + h]
    body = b"".join(b"\x00" + bytes(r[x * bpp:(x + w) * bpp]) for r in rows)
    ihdr = struct.pack(">IIBBBBB", w, h, 8, color, 0, 0, 0)
    with open(dst, "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) + chunk(b"IDAT", zlib.compress(body)) + chunk(b"IEND", b""))


if __name__ == "__main__":
    main()
