#!/usr/bin/env python
# coding: utf-8

# In[27]:

# Practice Huffman Coding implementation in python
# Compress and Decompress a String
# Shrinika Telu

String='BCAADDDCCACACAC'

#creating a tree
class TreeNode(object):
    def __init__(self,left=None,right=None):
        self.left=left
        self.right=right
    def children(self):
        return (self.left,self.right)
    def nodes(self):
        return (self.left,self.right)
    def __str__(self):
        return ('%s_%s' % (self.left,self.right))
    
# main function to implement huffman coding   
def Huffman_code_tree(node,left=True,binString=''):
    if type(node) is str:
        return {node:binString}
    (l,r)=node.children()
    d=dict()
    d.update(Huffman_code_tree(l,True,binString+'0'))
    d.update(Huffman_code_tree(r,False,binString+'1'))
    return d


#calculate frequncies
freq={}
for c in String:
    if c in freq:
        freq[c]+=1
    else:
        freq[c]=1
freq=sorted(freq.items(),key=lambda x:x[1],reverse=True)
nodes=freq

#for huffman codes
while len(nodes)>1:
    (key1,c1)=nodes[-1]
    (key2,c2)=nodes[-2]
    
    nodes=nodes[:-2]
    node=TreeNode(key1,key2)
    
    nodes.append((node,c1+c2))
    nodes=sorted(nodes,key=lambda x:x[1],reverse=True)
    
huffmancode=Huffman_code_tree(nodes[0][0])

#output function

print("Char |  Huffman Code")
print("____________________")

for (char,frequencies) in freq:
    print('%-4r | %12s' % (char,huffmancode[char]))


