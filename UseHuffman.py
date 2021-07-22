#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from huffman import HuffmanCoding
import sys

path = "sample.txt"

h = HuffmanCoding(path)
print('Compressing file , please wait !')

output_path = h.compress()
print("Compressed file path: " + output_path)

print()
print('Decompressing file , please wait !')

decom_path = h.decompress(output_path)
print("Decompressed file path: " + decom_path)

