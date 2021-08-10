#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from huffman import HuffmanCoding
import sys

path = "/Users/shrinika/Documents/HuffmanCoding_Project/sample.txt"
h = HuffmanCoding(path)

com_path = h.compress()
print("Compressed file path: " + com_path)

decom_path = h.decompress(com_path)
print("Decompressed file path: " + decom_path)

