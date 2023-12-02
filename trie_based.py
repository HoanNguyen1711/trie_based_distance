import time
import sys

DICTIONARY = "/usr/share/dict/words"
TARGET = sys.argv[1]
MAX_COST = int(sys.argv[2])

# Keep some interesting statistics
NodeCount = 0
WordCount = 0


# The Trie data structure keeps a set of words, organized with one node for
# each letter. Each node has a branch for each letter that may follow it in the
# set of words.
class TrieNode:
    def __init__(self):
        self.word = None
        self.children = {}

        global NodeCount
        NodeCount += 1

    def insert(self, input_word):
        node = self
        reversed_word = input_word[::-1]
        for letter in reversed_word:
            if letter not in node.children:
                node.children[letter] = TrieNode()

            node = node.children[letter]

        node.word = input_word

#Example usage with a list of cities and a target city:
cities = ["An Giang", "Bà rịa Vũng Tàu", "Bạc Liêu", "Bắc Giang", "Bắc Kạn", "Bắc Ninh", "Bến Tre", "Bình Dương", "Bình Định", "Bình Phước", "Bình Thuận", "Cà Mau",
          "Cao Bằng", "Cần Thơ", "Đà Nẵng", "Đắk Lắk", "Đắk Nông", "Điện Biên", "Đồng Nai", "Đồng Tháp", "Gia Lai", "Hà Giang", "Hà Nam", "Hà Nội", "Hà Tĩnh", "Hải Dương",
          "Hải Phòng", "Hậu Giang", "Hòa Bình", "Hưng Yên", "Khánh Hòa", "Kiên Giang", "Kon Tum", "Lai Châu", "Lạng Sơn", "Lào Cai", "Lâm Đồng", "Long An", "Nam Định", "Nghệ An",
          "Ninh Bình", "Ninh Thuận", "Phú Thọ", "Phú Yên", "Quảng Bình", "Quảng Nam", "Quảng Ngãi", "Quảng Ninh", "Quảng Trị", "Sóc Trăng", "Sơn La", "Tây Ninh", "Thái Bình",
          "Thái Nguyên", "Thanh Hóa", "Thừa Thiên Huế", "Tiền Giang", "TP Hồ Chí Minh", "Trà Vinh", "Tuyên Quang", "Vĩnh Long", "Vĩnh Phúc", "Yên Bái"]

# read dictionary file into a trie
start = time.time()
trie = TrieNode()
for word in cities:
    WordCount += 1
    trie.insert(word)
end = time.time()

print("Read %d words into %d nodes in %g seconds" % (WordCount, NodeCount, end - start))


# The search function returns a list of all words that are less than the given
# maximum distance from the target word
def search(word, maxCost):
    # build first row
    currentRow = range(len(word) + 1)
    results = []
    word = word[::-1]

    # recursively search each branch of the trie
    for letter in trie.children:
        searchRecursive(trie.children[letter], letter, word, currentRow,
                        results, maxCost)

    return results


# This recursive helper is used by the search function above. It assumes that
# the previousRow has been filled in already.
def searchRecursive(node, letter, word, previousRow, results, maxCost):
    columns = len(word) + 1
    currentRow = [previousRow[0] + 1]

    # Build one row for the letter, with a column for each letter in the target
    # word, plus one for the empty string at column 0
    for column in range(1, columns):

        insertCost = currentRow[column - 1] + 1
        deleteCost = previousRow[column] + 1

        if word[column - 1] != letter:
            replaceCost = previousRow[column - 1] + 1
        else:
            replaceCost = previousRow[column - 1]

        currentRow.append(min(insertCost, deleteCost, replaceCost))

    # if the last entry in the row indicates the optimal cost is less than the
    # maximum cost, and there is a word in this trie node, then add it.
    if currentRow[-1] <= maxCost and node.word != None:
        results.append((node.word, currentRow[-1]))

    # if any entries in the row are less than the maximum cost, then
    # recursively search each branch of the trie
    if min(currentRow) <= maxCost:
        for letter in node.children:
            searchRecursive(node.children[letter], letter, word, currentRow,
                            results, maxCost)


start = time.time()
results = search(TARGET, MAX_COST)
end = time.time()

for result in results:
    print(result)

print("Search took %g s" % (end - start))
