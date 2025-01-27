import sys

class Affine:
    def __init__(self, key1, key2):
        if not (isinstance(key1, int) and 1 <= key1 <= 250):
            raise ValueError("key1 phải là số nguyên trong khoảng từ 1 đến 250")
        if not (isinstance(key2, int) and 1 <= key2 <= 250):
            raise ValueError("key2 phải là số nguyên trong khoảng từ 1 đến 250")
        self._key1 = key1
        self._key2 = key2
        self._inverse_key1 = pow(self._key1, -1, 251)

    def encrypt(self, msg):
        msg_enc = b""
        for b in msg:
            msg_enc += bytes([(self._key1 * b + self._key2) % 251])
        return msg_enc

    def decrypt(self, msg):
        msg_dec = b""
        for b in msg:
            decrypted_byte = (self._inverse_key1 * (b - self._key2)) % 251
            msg_dec += bytes([decrypted_byte])
        return msg_dec

def find_keys(ciphertext, known_plaintext):
    ciphertext_length = len(ciphertext)
    plaintext_length = len(known_plaintext)

    for pos in range(ciphertext_length - plaintext_length + 1):
        # Lấy hai cặp byte từ vị trí hiện tại
        x1 = known_plaintext[0]
        x2 = known_plaintext[1]
        y1 = ciphertext[pos]
        y2 = ciphertext[pos + 1]

        delta_x = (x2 - x1) % 251
        delta_y = (y2 - y1) % 251

        try:
            delta_x_inv = pow(delta_x, -1, 251)
        except ValueError:
            # delta_x không có nghịch đảo, bỏ qua cặp này
            continue

        a = (delta_y * delta_x_inv) % 251
        b = (y1 - a * x1) % 251

        # Kiểm tra nếu a và b nằm trong khoảng từ 1 đến 250
        if not (1 <= a <= 250 and 1 <= b <= 250):
            continue

        # Tạo đối tượng Affine với khóa tìm được
        try:
            cipher = Affine(a, b)
        except ValueError:
            # Nếu vẫn gặp lỗi, bỏ qua cặp này
            continue

        decrypted = cipher.decrypt(ciphertext)

        # Kiểm tra xem phần đã giải mã có chứa known_plaintext không
        if known_plaintext in decrypted:
            return a, b, decrypted

    return None, None, None

def main():
    # Nhập thông điệp mã hóa dưới dạng chuỗi hex
    if len(sys.argv) != 2:
        print("Sử dụng: python affine_break.py <ciphertext_hex>")
        sys.exit(1)

    ciphertext_hex = sys.argv[1]
    try:
        ciphertext = bytes.fromhex(ciphertext_hex)
    except ValueError:
        print("Chuỗi hex không hợp lệ.")
        sys.exit(1)

    # Định nghĩa phần văn bản gốc đã biết
    known_plaintext = b'cryptography'

    # Tìm khóa
    key1, key2, decrypted = find_keys(ciphertext, known_plaintext)

    if key1 is not None and key2 is not None:
        print(f"Đã tìm thấy khóa:")
        print(f"key1 (a) = {key1}")
        print(f"key2 (b) = {key2}")
        print("\nThông điệp đã giải mã:")
        try:
            print(decrypted.decode())
        except UnicodeDecodeError:
            print(decrypted.decode(errors='replace'))  # Sử dụng 'replace' để xử lý byte không hợp lệ
    else:
        print("Không tìm thấy khóa phù hợp.")

if __name__ == '__main__':
    main()
