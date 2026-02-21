"""
ContentTrie.py - Implements a Trie data structure for efficient content storage and autocomplete functionality.
This is used for storing course content (titles, keywords, tags) and providing fast prefix-based search.

Time Complexity:
- insertContent: O(m) where m is the length of the content string
- autocomplete: O(m + k) where m is prefix length and k is number of matching words

Space Complexity: O(n * m) where n is number of contents and m is average length
"""

class TrieNode:
    def __init__(self):
        self.children = {}
        self.endOfString = False
        self.contentList = []  # For storing title, keyword, tag at the end of each word

class ContentTrie:
    def __init__(self):
        self.root = TrieNode()

    def insertContent(self, content):
        """Insert content into the trie - O(m) time where m is content length"""
        if not content:
            return
            
        current = self.root
        for letter in content.lower():  # Case insensitive search
            node = current.children.get(letter)
            if node is None:
                node = TrieNode()
                current.children[letter] = node
            current = node
        current.endOfString = True
        if content not in current.contentList:  # Avoid duplicates
            current.contentList.append(content)

    def autocomplete(self, prefix):
        """Find all contents starting with prefix - O(m + k) time"""
        if not prefix:
            return []
            
        currentNode = self.root
        result = []

        # Find the node at the end of the prefix - O(m)
        for letter in prefix.lower():
            node = currentNode.children.get(letter)
            if node is None:
                return result  # If no matches are found
            currentNode = node

        # Find all words starting with prefix - O(k)
        self._findAllWords(currentNode, prefix, result)
        return result

    def _findAllWords(self, node, prefix, result):
        """Recursively find all words from current node - O(k) where k is number of matches"""
        if node.endOfString:
            result.extend(node.contentList)

        for ch, childNode in node.children.items():
            self._findAllWords(childNode, prefix + ch, result)

    def searchExact(self, content):
        """Check if exact content exists - O(m) time"""
        current = self.root
        for letter in content.lower():
            node = current.children.get(letter)
            if node is None:
                return False
            current = node
        return current.endOfString

    def getAllContents(self):
        """Get all contents in trie - O(n) time"""
        result = []
        self._findAllWords(self.root, "", result)
        return result