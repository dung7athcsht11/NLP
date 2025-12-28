def count_correct_words(pred_sentences, gold_sentences):
    total_correct = 0
    total_gold = 0
    total_pred = 0

    for pred, gold in zip(pred_sentences, gold_sentences):
        p_list = list(pred)
        g_list = list(gold)
        total_pred += len(p_list)
        total_gold += len(g_list)
        gold_counts = {}
        for w in g_list:
            gold_counts[w] = gold_counts.get(w, 0) + 1
        for w in p_list:
            if w in gold_counts and gold_counts[w] > 0:
                total_correct += 1
                gold_counts[w] -= 1
    return total_correct, total_gold, total_pred

def calculate_metrics(total_correct, total_gold, total_pred):
    precision = total_correct / total_pred if total_pred > 0 else 0
    recall = total_correct / total_gold if total_gold > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall > 0 else 0
    return precision, recall, f1
