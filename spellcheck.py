import re
from collections import Counter

class spellcheck:


    def words(self, text): return re.findall(r'\w+', text.lower())

    def P(self, word, file):
        path = "dataset/" + str(file)
        WORDS = Counter(self.words(open(path).read()))
        N = sum(WORDS.values())
        "Probability of `word`."
        return WORDS[word] / N


    def correction(self, word, file):
        "Most probable spelling correction for word."
        # p = P(word, file)
        probs=[]
        candi = list(self.candidates(word, file))
        # print("candi: ", candi)
        for w in candi:
            probs.append(self.P(w, file))

        # print("probs: ", probs)
        return candi[probs.index(max(probs))]


    def candidates(self, word, file):
        "Generate possible spelling corrections for word."
        return (self.known([word], file) or self.known(self.edits1(word), file) or self.known(self.edits2(word), file) or [word])


    def known(self, ws, file):
        "The subset of `words` that appear in the dictionary of WORDS."
        path = "dataset/" + str(file)
        WORDS = Counter(self.words(open(path).read()))
        return set(w for w in ws if w in WORDS)


    def edits1(self, word):
        "All edits that are one edit away from `word`."
        letters = 'abcdefghijklmnopqrstuvwxyz'
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes = [L + R[1:] for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
        replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
        inserts = [L + c + R for L, R in splits for c in letters]
        return set(deletes + transposes + replaces + inserts)


    def edits2(self, word):
        "All edits that are two edits away from `word`."
        return (e2 for e1 in self.edits1(word) for e2 in self.edits1(e1))


# sc = spellcheck()
# print(sc.correction('anthrohology', 'Anthropology.txt'))