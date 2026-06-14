"""Command-line runner: compress a text file, then decompress and verify.

Usage:
    python UseHuffman.py [path/to/file.txt]

Defaults to sample.txt if no path is given.
"""
import os
import sys

from huffman import HuffmanCoding


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "sample.txt"
    if not os.path.isfile(path):
        sys.exit(f"File not found: {path}")

    h = HuffmanCoding(path)
    compressed = h.compress()
    decompressed = h.decompress(compressed)

    orig = os.path.getsize(path)
    comp = os.path.getsize(compressed)
    reduction = 100 * (1 - comp / orig) if orig else 0

    # verify lossless roundtrip
    with open(path) as a, open(decompressed) as b:
        identical = a.read().rstrip() == b.read()

    print(f"\nOriginal:     {orig:,} bytes")
    print(f"Compressed:   {comp:,} bytes")
    print(f"Reduction:    {reduction:.1f}%")
    print(f"Lossless:     {'yes' if identical else 'NO — MISMATCH'}")


if __name__ == "__main__":
    main()
