class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.universities = []

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word, university):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
            node.universities.append(university)
        node.is_end_of_word = True

    def search(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        return node.universities