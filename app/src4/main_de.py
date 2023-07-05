import numpy as np

class Node:
    def __init__(self):
        self.prob = None
        self.code = None
        self.data = None
        self.left = None
        self.right = None

def tree(probabilities):
    prq = []
    for color, probability in enumerate(probabilities):
        # Create a leaf node for each character with its respective probability
        leaf = Node()
        leaf.data = chr(color)
        leaf.prob = probability
        prq.append(leaf)

    while len(prq) > 1:
        # Merge nodes with the smallest probabilities to build the Huffman tree
        prq.sort(key=lambda x: x.prob)
        newnode = Node()
        l = prq.pop(0)
        r = prq.pop(0)

        newnode.left = l
        newnode.right = r
        newprob = l.prob + r.prob
        newnode.prob = newprob

        prq.append(newnode)

    return prq[0]


# Prompt the user to enter the input file name
input_file = input("Enter the compressed file name: ")

# Read the compressed file
with open(input_file, 'rb') as file:
    compressed_data = file.read()

# Calculate the histogram from the compressed data
hist = np.bincount(np.frombuffer(compressed_data, dtype=np.uint8), minlength=256)

# Calculate the probabilities from the histogram frequencies
probabilities = hist / np.sum(hist)

# Build the Huffman tree using the probabilities
root_node = tree(probabilities)


# Define a function for traversing the Huffman tree and generating codes
def huffman_traversal(root_node, tmp_array, decompressed_text):
    if root_node.left is not None:
        # Traverse the left branch and update the temporary array
        tmp_array.append(1)
        huffman_traversal(root_node.left, tmp_array, decompressed_text)
        tmp_array.pop()

    if root_node.right is not None:
        # Traverse the right branch and update the temporary array
        tmp_array.append(0)
        huffman_traversal(root_node.right, tmp_array, decompressed_text)
        tmp_array.pop()
    else:
        # Reached a leaf node, write the character to the decompressed text
        bitstream = ''.join(str(cell) for cell in tmp_array[:])
        decompressed_text.append(chr(int(bitstream, 2)))


# Initialize variables and create an empty list for storing the decompressed data
tmp_array = []
decompressed_text = []

# Traverse the Huffman tree and generate the decompressed data
huffman_traversal(root_node, tmp_array, decompressed_text)

# Join the decompressed characters into a string
decompressed_string = ''.join(decompressed_text)

# Write the decompressed data to a file
decompressed_file = input_file.split('.compressed')[0] + '_decompressed.txt'
with open(decompressed_file, 'w') as file:
    file.write(decompressed_string)

print('Decompression completed. The decompressed file is', decompressed_file)
