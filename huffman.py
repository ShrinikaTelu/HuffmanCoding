"""Huffman coding — lossless text compression.

Pipeline: frequency table -> min-heap -> binary tree -> variable-length codes
-> bit-packed bytes. Frequent characters get shorter codes, so the encoded
file is smaller than the original. Decompression reverses every step exactly,
so the roundtrip is lossless.
"""
import heapq
import os


class HuffmanCoding:
    def __init__(self, path=None):
        self.path = path
        self.heap = []
        self.codes = {}
        self.reverse_mapping = {}

    class HeapNode:
        def __init__(self, char, freq):
            self.char = char
            self.freq = freq
            self.left = None
            self.right = None

        # min-heap orders by frequency
        def __lt__(self, other):
            return self.freq < other.freq

        def __eq__(self, other):
            if other is None or not isinstance(other, HuffmanCoding.HeapNode):
                return False
            return self.freq == other.freq

    # ---- compression ----

    def make_frequency_dict(self, text):
        frequency = {}
        for char in text:
            frequency[char] = frequency.get(char, 0) + 1
        return frequency

    def make_heap(self, frequency):
        for char, freq in frequency.items():
            heapq.heappush(self.heap, self.HeapNode(char, freq))

    def merge_nodes(self):
        while len(self.heap) > 1:
            n1 = heapq.heappop(self.heap)
            n2 = heapq.heappop(self.heap)
            merged = self.HeapNode(None, n1.freq + n2.freq)
            merged.left, merged.right = n1, n2
            heapq.heappush(self.heap, merged)

    def make_codes_helper(self, root, current_code):
        if root is None:
            return
        if root.char is not None:
            # single-character input edge case: give it code "0"
            self.codes[root.char] = current_code or "0"
            self.reverse_mapping[current_code or "0"] = root.char
            return
        self.make_codes_helper(root.left, current_code + "0")
        self.make_codes_helper(root.right, current_code + "1")

    def make_codes(self):
        root = heapq.heappop(self.heap)
        self.make_codes_helper(root, "")

    def get_encoded_text(self, text):
        return "".join(self.codes[char] for char in text)

    def pad_encoded_text(self, encoded_text):
        extra_padding = 8 - len(encoded_text) % 8
        encoded_text += "0" * extra_padding
        padded_info = "{0:08b}".format(extra_padding)
        return padded_info + encoded_text

    def get_byte_array(self, padded_encoded_text):
        if len(padded_encoded_text) % 8 != 0:
            raise ValueError("Encoded text not padded to a multiple of 8 bits")
        b = bytearray()
        for i in range(0, len(padded_encoded_text), 8):
            b.append(int(padded_encoded_text[i:i + 8], 2))
        return b

    def compress(self, path=None):
        path = path or self.path
        filename, _ = os.path.splitext(path)
        output_path = filename + ".bin"

        with open(path, "r") as file, open(output_path, "wb") as output:
            text = file.read().rstrip()
            self.make_heap(self.make_frequency_dict(text))
            self.merge_nodes()
            self.make_codes()
            encoded = self.get_encoded_text(text)
            padded = self.pad_encoded_text(encoded)
            output.write(bytes(self.get_byte_array(padded)))

        print(f"Compressed -> {output_path}")
        return output_path

    # ---- decompression ----

    def remove_padding(self, padded_encoded_text):
        extra_padding = int(padded_encoded_text[:8], 2)
        text = padded_encoded_text[8:]
        return text[:-extra_padding] if extra_padding else text

    def decode_text(self, encoded_text):
        current, decoded = "", []
        for bit in encoded_text:
            current += bit
            if current in self.reverse_mapping:
                decoded.append(self.reverse_mapping[current])
                current = ""
        return "".join(decoded)

    def decompress(self, input_path):
        filename, _ = os.path.splitext(self.path or input_path)
        output_path = filename + "_decompressed.txt"

        with open(input_path, "rb") as file, open(output_path, "w") as output:
            bit_string = ""
            byte = file.read(1)
            while byte:
                bit_string += bin(ord(byte))[2:].rjust(8, "0")
                byte = file.read(1)
            encoded = self.remove_padding(bit_string)
            output.write(self.decode_text(encoded))

        print(f"Decompressed -> {output_path}")
        return output_path
