class LongestMatching:
    def __init__(self, dictionary):
        self.dictionary = dictionary
        # Tìm độ dài lớn nhất của một từ trong từ điển (để giới hạn cửa sổ quét)
        self.max_syllables = 0
        for word in dictionary:
            count = len(word.split('_'))
            if count > self.max_syllables:
                self.max_syllables = count

    def segment(self, sentence_text):
        """
        Input: "Học sinh đang học bài" (String)
        Output: ["Học_sinh", "đang", "học", "bài"] (List)
        """
        syllables = sentence_text.split()
        n = len(syllables)
        result = []
        i = 0

        while i < n:
            word_found = False
            # Thử ghép từ dài nhất có thể (từ max_syllables xuống 1)
            for j in range(min(n, i + self.max_syllables), i, -1):
                word_candidate = "_".join(syllables[i:j])

                # Kiểm tra trong từ điển
                if word_candidate.lower() in self.dictionary:
                    result.append(word_candidate)
                    i = j
                    word_found = True
                    break

            # Nếu không tìm thấy từ nào khớp, coi âm tiết hiện tại là 1 từ
            if not word_found:
                result.append(syllables[i])
                i += 1

        return result