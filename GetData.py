def load_conll_data(file_path):
    """
    Hàm đọc file .conll và trả về danh sách các câu đã tách từ.
    """
    sentences = []
    current_sentence = []

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()

            # Gặp dòng trống -> Kết thúc một câu
            if not line:
                if current_sentence:
                    sentences.append(current_sentence)
                    current_sentence = []
                continue

            # Bỏ qua các dòng comment (nếu có)
            if line.startswith("#"):
                continue

            # Cắt dòng bằng dấu tab hoặc khoảng trắng
            parts = line.split()

            # Lấy cột thứ 2 (index 1) là từ vựng (Word Form)
            # Ví dụ: parts[0] là ID, parts[1] là từ "Học_sinh"
            if len(parts) > 1:
                word = parts[1]
                current_sentence.append(word)

    # Thêm câu cuối cùng nếu file không kết thúc bằng dòng trống
    if current_sentence:
        sentences.append(current_sentence)

    return sentences


# --- CHẠY THỬ ---
# Thay tên file tương ứng của bạn vào đây (Train, Dev, hoặc Test)
train_file = "NLPSEGMENT/data/train.conll"

# Gọi hàm
try:
    data_train = load_conll_data(train_file)

    print(f"Đã đọc thành công {len(data_train)} câu từ file {train_file}.")
    print("-" * 30)
    print("Ví dụ 2 câu đầu tiên (Dữ liệu chuẩn - Gold Standard):")
    for i in range(2):
        # In ra dạng chuỗi để dễ nhìn
        print(f"Câu {i + 1}: {' '.join(data_train[i])}")

except FileNotFoundError:
    print(f"Lỗi: Không tìm thấy file '{train_file}'. Hãy kiểm tra lại đường dẫn.")