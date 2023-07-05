import numpy as np
import queue

class Node:
    def __init__(self):
        self.prob = None
        self.code = None
        self.data = None
        self.left = None
        self.right = None

    def __lt__(self, other):
        if self.prob < other.prob:
            return 1
        else:
            return 0

    def __ge__(self, other):
        if self.prob > other.prob:
            return 1
        else:
            return 0

def tree(probabilities):
    prq = queue.PriorityQueue()

    for color, probability in enumerate(probabilities):
        # Create a leaf node for each character with its respective probability
        leaf = Node()
        leaf.data = chr(color)
        leaf.prob = probability
        prq.put(leaf)

    while prq.qsize() > 1:
        # Merge nodes with the smallest probabilities to build the Huffman tree
        newnode = Node()
        l = prq.get()
        r = prq.get()

        newnode.left = l
        newnode.right = r
        newprob = l.prob + r.prob
        newnode.prob = newprob

        prq.put(newnode)

    return prq.get()


# Prompt the user to enter the input file name
input_file = input("Enter the input file name: ")

# Read the text file
with open(input_file, 'r') as file:
    text = file.read()

# Compute the histogram of characters in the text
hist = np.bincount(np.frombuffer(text.encode(), dtype=np.uint8), minlength=256)

# Calculate the probabilities from the histogram frequencies
probabilities = hist / np.sum(hist)

# Build the Huffman tree using the probabilities
root_node = tree(probabilities)


# Define a function for traversing the Huffman tree and generating codes
def huffman_traversal(root_node, tmp_array, f):
    if root_node.left is not None:
        # Traverse the left branch and update the temporary array
        tmp_array[huffman_traversal.count] = 1
        huffman_traversal.count += 1
        huffman_traversal(root_node.left, tmp_array, f)
        huffman_traversal.count -= 1

    if root_node.right is not None:
        # Traverse the right branch and update the temporary array
        tmp_array[huffman_traversal.count] = 0
        huffman_traversal.count += 1
        huffman_traversal(root_node.right, tmp_array, f)
        huffman_traversal.count -= 1
    else:
        # Reached a leaf node, record the number of bits for the character and write it to a file
        huffman_traversal.output_bits[ord(root_node.data)] = huffman_traversal.count
        bitstream = ''.join(str(cell) for cell in tmp_array[:huffman_traversal.count])
        f.write(bitstream.encode())


# Initialize variables and open a file for writing codes
tmp_array = np.ones([256], dtype=int)
huffman_traversal.output_bits = np.empty(256, dtype=int)
huffman_traversal.count = 0
compressed_file = input_file.split('.')[0] + '.compressed'
f = open(compressed_file, 'wb')

# Traverse the Huffman tree and write the codes to the file
huffman_traversal(root_node, tmp_array, f)

# Calculate the compression rate
input_bits = len(text) * 8
compression = (1 - np.sum(huffman_traversal.output_bits * hist) / input_bits) * 100

print('Compression is', compression, 'percent')
