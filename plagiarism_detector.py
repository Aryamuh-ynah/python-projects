from difflib import SequenceMatcher


with open('text.txt') as one_file, open('main.txt') as two_file:
    one = one_file.read()
    two = two_file.read()

similarity = SequenceMatcher(None, one, two).ratio()
print(f"Similarity: {similarity*100:.2f}%")