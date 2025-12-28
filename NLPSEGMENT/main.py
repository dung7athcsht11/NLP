from utils.data_loader import load_conll_data, build_dictionary
from methods.baseline import LongestMatching

TRAIN_PATH = 'data/train.conll'
TEST_PATH = 'data/test.conll'

# Load dữ liệu Train
train_sentences = load_conll_data(TRAIN_PATH)
print(f"Đã tải {len(train_sentences)} câu train.")

# Load dữ liệu Test
test_sentences = load_conll_data(TEST_PATH)
print(f"Đã tải {len(test_sentences)} câu test.")

# Xây dựng từ điển
vocab = build_dictionary(train_sentences)
print(f"Kích thước từ điển: {len(vocab)} từ.")

# Khởi tạo thuật toán Baseline
lm_model = LongestMatching(vocab)

# Chạy thử nghiệm trên 1 câu mẫu trong tập Test
print("\nTHỬ NGHIỆM")
sample_sentence_list = test_sentences[100]
sample_text = " ".join(sample_sentence_list).replace("_", " ")

print(f"Câu gốc (Input):   {sample_text}")
print(f"Nhãn: {sample_sentence_list}")

# Dự đoán
predicted = lm_model.segment(sample_text)
print(f"Dự đoán (Model):   {predicted}")

# So sánh đơn giản
if predicted == sample_sentence_list:
    print("KẾT QUẢ: ĐÚNG")
else:
    print("KẾT QUẢ: SAI.")