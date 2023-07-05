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


def build_tree(probabilities):
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
        character = str(root_node.data)
        wr_str = character + ' ' + bitstream + '\n'
        f.write(wr_str)


def decompress_file(input_file):
    # Read the compressed file
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # Parse the bitstreams and reconstruct the Huffman tree
    probabilities = np.zeros(256)
    for line in lines:
        bitstream = line.strip().split(' ')
        if len(bitstream) == 2:
            character, code = bitstream
            probabilities[ord(character)] = len(code)

    root_node = build_tree(probabilities)

    # Initialize variables and open the output file for writing
    tmp_array = np.ones([256], dtype=int)
    huffman_traversal.output_bits = np.empty(256, dtype=int)
    huffman_traversal.count = 0
    output_file_name = 'output.txt'

    with open(output_file_name, 'w') as output_file:
        # Traverse the Huffman tree and write the characters to the output file
        traverse_node = root_node
        for line in lines:
            bitstream = line.strip().split(' ')
            if len(bitstream) == 2:
                code = bitstream[1]

                for bit in code:
                    if bit == '1':
                        traverse_node = traverse_node.left
                    else:
                        traverse_node = traverse_node.right

                    if traverse_node.data is not None:
                        output_file.write(traverse_node.data)
                        traverse_node = root_node


# Prompt the user to enter the input file name
input_file = input("Enter the compressed file name: ")

# Decompress the file and create the output.txt file
decompress_file(input_file)

print('Decompression complete. The output.txt file has been created.')
