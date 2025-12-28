import sklearn_crfsuite
from sklearn_crfsuite import metrics


class CRFSegmenter:
    # 1. Thêm tham số dictionary vào hàm khởi tạo
    def __init__(self, dictionary=None):
        self.dictionary = dictionary if dictionary else set()
        self.model = sklearn_crfsuite.CRF(
            algorithm='lbfgs',
            c1=0.1,
            c2=0.1,
            max_iterations=100,
            all_possible_transitions=True
        )

    # 2. Nâng cấp hàm rút trích đặc trưng (QUAN TRỌNG NHẤT)
    def _word2features(self, sent, i):
        word = sent[i][0]

        # Đặc trưng cơ bản
        features = {
            'bias': 1.0,
            'word.lower()': word.lower(),
            'word.isupper()': word.isupper(),
            'word.istitle()': word.istitle(),
            'word.isdigit()': word.isdigit(),
        }

        # --- FEATURE MỚI: TỪ ĐIỂN (HYBRID) ---
        # Kiểm tra cụm 2 từ (Bigram) có trong từ điển không?
        if i < len(sent) - 1:
            next_word = sent[i + 1][0]
            bigram = f"{word}_{next_word}"
            features['bigram_in_dict'] = (bigram.lower() in self.dictionary)
        else:
            features['bigram_in_dict'] = False

        # Kiểm tra cụm 3 từ (Trigram)
        if i < len(sent) - 2:
            next_word = sent[i + 1][0]
            next_next_word = sent[i + 2][0]
            trigram = f"{word}_{next_word}_{next_next_word}"
            features['trigram_in_dict'] = (trigram.lower() in self.dictionary)
        else:
            features['trigram_in_dict'] = False
        # -------------------------------------

        # Context: Từ phía trước
        if i > 0:
            word1 = sent[i - 1][0]
            features.update({
                '-1:word.lower()': word1.lower(),
                '-1:word.istitle()': word1.istitle(),
            })
        else:
            features['BOS'] = True

        # Context: Từ phía sau
        if i < len(sent) - 1:
            word1 = sent[i + 1][0]
            features.update({
                '+1:word.lower()': word1.lower(),
                '+1:word.istitle()': word1.istitle(),
            })
        else:
            features['EOS'] = True

        return features

    def _sent2features(self, sent):
        return [self._word2features(sent, i) for i in range(len(sent))]

    def _sent2labels(self, sent):
        return [label for token, label in sent]

    def _convert_to_bi_labels(self, sentences):
        formatted_data = []
        for sent in sentences:
            labeled_sent = []
            for word in sent:
                syllables = word.split('_')
                labeled_sent.append((syllables[0], 'B_W'))
                for s in syllables[1:]:
                    labeled_sent.append((s, 'I_W'))
            formatted_data.append(labeled_sent)
        return formatted_data

    def train(self, train_sentences):
        print(" -> [CRF Hybrid] Đang chuẩn bị dữ liệu & features...")
        # Cập nhật từ điển nếu chưa có
        if not self.dictionary:
            for sent in train_sentences:
                for word in sent:
                    self.dictionary.add(word.lower())

        train_data_bi = self._convert_to_bi_labels(train_sentences)
        X_train = [self._sent2features(s) for s in train_data_bi]
        y_train = [self._sent2labels(s) for s in train_data_bi]

        print(" -> [CRF Hybrid] Đang training model...")
        self.model.fit(X_train, y_train)
        print(" -> [CRF Hybrid] Training hoàn tất!")

    def segment(self, sentence_text):
        tokens = sentence_text.split()
        temp_sent = [(t, 'O') for t in tokens]
        features = self._sent2features(temp_sent)
        pred_labels = self.model.predict_single(features)

        result = []
        current_word = []
        for token, label in zip(tokens, pred_labels):
            if label == 'B_W':
                if current_word:
                    result.append("_".join(current_word))
                current_word = [token]
            elif label == 'I_W':
                current_word.append(token)
            else:
                if current_word:
                    result.append("_".join(current_word))
                current_word = [token]

        if current_word:
            result.append("_".join(current_word))

        return result