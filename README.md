# Huffman Coding

Lossless text compression in Python, with an interactive browser visualizer.

🎮 **Try it live:** _add your GitHub Pages URL here_

Huffman coding assigns each character a variable-length binary code — the most
frequent characters get the shortest codes — so the encoded bitstream is
smaller than fixed-width (8-bit) encoding, and decodes back perfectly.

## What's here

| File | What it does |
|---|---|
| `huffman.py` | The `HuffmanCoding` class: frequency table → min-heap → binary tree → prefix codes → bit-packed file, and the exact reverse for decompression. |
| `UseHuffman.py` | CLI runner — compresses a file, decompresses it, and verifies the roundtrip. |
| `index.html` | Interactive visualizer (same algorithm in JS) — type text and watch the codes, sizes, and compression ratio update live. |
| `sample.txt` | Sample input (~134 KB). |

## Run the Python version

```bash
python UseHuffman.py            # uses sample.txt
python UseHuffman.py myfile.txt # or any text file
```

On the included sample:

```
Original:     134,398 bytes
Compressed:    71,532 bytes
Reduction:    46.8%
Lossless:     yes
```

## Try the visualizer

Open `index.html` in any browser (or via the live link above). Type text and
watch:

- the **Huffman codes** table — shortest codes go to the most frequent characters
- **size reduction** and **average bits per character** vs fixed 8-bit encoding
- the encoded **bitstream**, decoded back to confirm the roundtrip is lossless

Repetitive text compresses dramatically (~78%); text where every character is
unique compresses little — which is exactly what the algorithm's theory predicts.

## How it works

1. **Frequency table** — count each character.
2. **Min-heap** — order characters by frequency (`heapq`).
3. **Binary tree** — repeatedly merge the two lowest-frequency nodes; rare
   characters end up deeper (longer codes), frequent ones shallower (shorter).
4. **Prefix codes** — left = `0`, right = `1`; no code is a prefix of another,
   so the stream decodes unambiguously.
5. **Bit packing** — pack the bitstring into bytes, with a small header noting
   the padding added to reach a byte boundary.

---

Built by [Shrinika Telu](https://shrinikatelu.github.io/) — [LinkedIn](https://www.linkedin.com/in/shrinikatelu/)
