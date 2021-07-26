#!/usr/bin/env python
# coding: utf-8

# In[ ]:


'''    @Shrinika Telu     '''


'''
Huffman Coding

1 --> Making Frequency Dictionary

2 --> Constructing (priority Queue) MinHeap with the help of Frequency Dictionary 

3 --> Constructing Binary Tree out of heap

4 --> Build/Generate Codes to characters

5 --> Encoding Text (replacing character with its code)

6 --> Padding Encoding Text (if overall lenght of bit streams is not multiple of 8, add some padding to text)

7 --> Encoding Text Convert Into Bytes (store padded information in 8bits)

8 --> Compressing File (write result to an output binary file)

__________________________________________

OUTPUT_ DECOMPRESSING TEXT

                     (read binary file)
9 --> Remove Padding

10 --> Decoding Text (read bits replace valid code with character)

11 --> Decompress File (save decoded data into output file)

'''

import heapq
import os

# Class with compressing and decompressing methods 
class HuffmanCoding:
    def __init__(self, path):
        self.path = path
        self.heap = []
        self.codes = {}
        self.reverse_mapping = {}
        
    # Class of heap nodes    
    class HeapNode:
        def __init__(self, char, freq):
            self.char = char
            self.freq = freq
            self.left = None
            self.right = None

        # defining comparators less_than and equals
        def __lt__(self, other):
            return self.freq < other.freq
        
        def __eq__(self, other):
            if(other == None):
                return False
            if(not isinstance(other, HeapNode)):
                return False
            return self.freq == other.freq

        

    '''    functions for compression   ''' 
    
    
    # Method to get the frequencies of characters
    def make_frequency_dict(self, text):
        frequency = {}
        for character in text:
            if not character in frequency:
                frequency[character] = 0
            frequency[character] += 1
        return frequency
    
    
    # Method to construct the heap with the help of frequency dictionary
    def make_heap(self, frequency):
        for key in frequency:
            node = self.HeapNode(key, frequency[key])
            heapq.heappush(self.heap, node)
     
    
    # Method to make tree out of the heap
    def merge_nodes(self):
        while(len(self.heap)>1):
            node1 = heapq.heappop(self.heap)
            node2 = heapq.heappop(self.heap)
            
            merged = self.HeapNode(None, node1.freq + node2.freq)
            merged.left = node1
            merged.right = node2
            
            heapq.heappush(self.heap, merged)
            
            
    # Method to generate codes recursively     
    def make_codes_helper(self, root, current_code):
        if(root == None):
            return
        
        if(root.char != None):
            self.codes[root.char] = current_code
            self.reverse_mapping[current_code] = root.char
            return
        
        self.make_codes_helper(root.left, current_code + "0")
        self.make_codes_helper(root.right, current_code + "1")
        
       
    
    # Method to generate codes and reverse codes    
    def make_codes(self):
        root = heapq.heappop(self.heap)
        current_code = ""
        self.make_codes_helper(root, current_code)


    # Method to get encoded text out of simple text    
    def get_encoded_text(self, text):
        encoded_text = ""
        for character in text:
            encoded_text += self.codes[character]
        return encoded_text
    
    
    # Method to pad encoded text
    def pad_encoded_text(self, encoded_text):
        extra_padding = 8 - len(encoded_text) % 8
        for i in range(extra_padding):
            encoded_text += "0"


        padded_info = "{0:08b}".format(extra_padding)
        encoded_text = padded_info + encoded_text
        return encoded_text



    # Method to get byte form of encoded text
    def get_byte_array(self, padded_encoded_text):
        if(len(padded_encoded_text) % 8 != 0):
            print("Encoded text not padded properly")
            exit(0)

        b = bytearray()
        for i in range(0, len(padded_encoded_text), 8):
            byte = padded_encoded_text[i:i+8]
            b.append(int(byte, 2))
        return b



    # Method to compress the file with path : self.path
    def compress(self):
        filename, file_extension = os.path.splitext(self.path)
        output_path = filename + ".bin"

        with open(self.path, 'r+') as file, open(output_path, 'wb') as output:
            text = file.read()
            text = text.rstrip() # removing unwanted spaces

            frequency = self.make_frequency_dict(text) # Constructing the frequency dictionary of characters in text 
            self.make_heap(frequency) # Construct min heap on the basis of frequency of characters 
            self.merge_nodes() # Construct tree structure using the heap
            self.make_codes() # Generate code for each of the characters

            encoded_text = self.get_encoded_text(text) # Get encoded text out of simple text
            padded_encoded_text = self.pad_encoded_text(encoded_text) # Pad encoded text properly

            b = self.get_byte_array(padded_encoded_text) # Get byte form of encoded text
            output.write(bytes(b)) # Write to the output file


        print("Compressed !")
        return output_path

    
        
        
    '''       functions for decompression     '''
    
    
    # Method to remove padding
    def remove_padding(self, padded_encoded_text):
        padded_info = padded_encoded_text[:8]
        extra_padding = int(padded_info, 2)

        padded_encoded_text = padded_encoded_text[8:] 
        encoded_text = padded_encoded_text[:-1*extra_padding]

        return encoded_text

    
    # Method to decode the text
    def decode_text(self, encoded_text):
        current_code = ""
        decoded_text = ""
        
        for bit in encoded_text:
            current_code += bit
            if(current_code in self.reverse_mapping):
                character = self.reverse_mapping[current_code]
                decoded_text += character
                current_code = ""

        return decoded_text



    # Method to decompress the file with path : self.path
    def decompress(self, input_path):
        filename, file_extension = os.path.splitext(self.path)
        output_path = filename + "_decompressed" + ".txt"

        with open(input_path, 'rb') as file, open(output_path, 'w') as output:
            bit_string = ""

            byte = file.read(1)
            while(len(byte) > 0):
                byte = ord(byte)
                bits = bin(byte)[2:].rjust(8, '0')
                bit_string += bits
                byte = file.read(1)


            encoded_text = self.remove_padding(bit_string)
            decompressed_text = self.decode_text(encoded_text)

            output.write(decompressed_text)


        print("Decompressed !")
        return output_path

