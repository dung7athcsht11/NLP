def load_conll_data(file_path):
    sentences = []
    current_sentence = []

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                if current_sentence:
                    sentences.append(current_sentence)
                    current_sentence = []
                continue

            parts = line.split()
            if len(parts) > 1:
                word = parts[1]
                current_sentence.append(word)

    if current_sentence:
        sentences.append(current_sentence)
    return sentences


def build_dictionary(sentences):
    vocab = set()
    for sentence in sentences:
        for word in sentence:
            vocab.add(word.lower())
    return vocab