import ast

# Hàm giải hệ phương trình tuyến tính trên GF(2) dùng Gaussian elimination.
def gauss_elim_gf2(mat, vec, ncols):
    n = len(mat)
    # Copy ma trận, vector để không làm thay đổi dữ liệu gốc.
    mat = mat[:]
    vec = vec[:]
    pivot_cols = [-1] * ncols
    row = 0
    for col in range(ncols):
        pivot = -1
        for r in range(row, n):
            if (mat[r] >> col) & 1:
                pivot = r
                break
        if pivot == -1:
            continue
        # Đổi chỗ hàng hiện tại với hàng pivot
        mat[row], mat[pivot] = mat[pivot], mat[row]
        vec[row], vec[pivot] = vec[pivot], vec[row]
        pivot_cols[col] = row
        # Loại bỏ các hàng khác có cột col bằng 1
        for r in range(n):
            if r != row and ((mat[r] >> col) & 1):
                mat[r] ^= mat[row]
                vec[r] ^= vec[row]
        row += 1
        if row == n:
            break
    # Đọc nghiệm: với các biến có pivot, nghiệm = giá trị vector.
    sol = 0
    for col in range(ncols):
        if pivot_cols[col] != -1:
            if vec[pivot_cols[col]] == 1:
                sol |= (1 << col)
    return sol

def main():
    # --- B1. Đọc file output.txt và parse 3 dòng chứa bytes literal
    with open('output.txt', 'r') as f:
        lines = f.read().splitlines()
    # Mỗi dòng có dạng "b'...'" nên dùng ast.literal_eval để chuyển thành bytes
    test_plain   = ast.literal_eval(lines[0])
    test_cipher  = ast.literal_eval(lines[1])
    secret_cipher = ast.literal_eval(lines[2])
    
    # --- B2. Tính keystream của giai đoạn 1 từ file test:
    # Vì ciphertext = plaintext XOR keystream  =>  keystream = plaintext XOR ciphertext
    keystream_bytes = bytes([p ^ c for p, c in zip(test_plain, test_cipher)])
    keystream_bits = []
    for b in keystream_bytes:
        # Chuyển mỗi byte thành dãy 8 bit (chuỗi “0” và “1” chuyển thành list các số 0/1)
        bits = list(map(int, bin(b)[2:].zfill(8)))
        keystream_bits.extend(bits)
    
    # --- B3. Xây dựng hệ phương trình tuyến tính với 64 ẩn
    # Chọn M bước (M >= 64); ở đây dùng M = 128 (hoặc dùng toàn bộ keystream nếu ngắn hơn)
    M = 128
    if len(keystream_bits) < M:
        M = len(keystream_bits)
    
    # Ta mô phỏng “hệ số” của các LFSR dưới GF(2):
    # Với LFSR1, taps = [32,22,2,1] → tương ứng indices: 0, 10, 30, 31.
    # Với LFSR2, taps = [32,31,30,10] → indices: 0, 1, 2, 22.
    taps1_coeff = [0, 10, 30, 31]
    taps2_coeff = [0, 1, 2, 22]
    
    # Khởi tạo trạng thái “hệ số” ban đầu: mỗi vị trí là vector đơn vị (biểu diễn dưới dạng số nguyên 32-bit)
    state1 = [1 << i for i in range(32)]  # LFSR1
    state2 = [1 << i for i in range(32)]  # LFSR2
    coeffs1 = []  # sẽ lưu hệ số của bit xuất ra (LFSR1)
    coeffs2 = []  # tương tự cho LFSR2
    
    for i in range(M):
        # Bit xuất ra là bit LSB của state
        coeffs1.append(state1[0])
        coeffs2.append(state2[0])
        # Tính bit mới (theo công thức: newbit = XOR( các bit ở vị trí tap ) )
        newbit1 = state1[0] ^ state1[10] ^ state1[30] ^ state1[31]
        # Cập nhật state: dịch phải 1 bit, và newbit được đưa vào MSB (index 31)
        state1 = state1[1:] + [newbit1]
        
        newbit2 = state2[0] ^ state2[1] ^ state2[2] ^ state2[22]
        state2 = state2[1:] + [newbit2]
    
    # Xây dựng hệ: mỗi phương trình là
    #    (coeffs1[i] dot s1) XOR (coeffs2[i] dot s2) = keystream_bits[i]
    # Ta biểu diễn hàng (row) dưới dạng số nguyên 64-bit:
    #   - 32 bit thấp: hệ số của LFSR1, 32 bit cao: của LFSR2.
    A = []   # danh sách các hàng (mỗi hàng là số nguyên 64-bit)
    b_vec = []  # vector bên phải
    for i in range(M):
        row = coeffs1[i] | (coeffs2[i] << 32)
        A.append(row)
        b_vec.append(keystream_bits[i])
    
    # --- B4. Giải hệ phương trình mod2 để thu được trạng thái ban đầu (64 bit)
    X = gauss_elim_gf2(A, b_vec, 64)
    init_state1 = X & ((1 << 32) - 1)
    init_state2 = X >> 32
    print("Recovered initial state LFSR1: 0x{:08x}".format(init_state1))
    print("Recovered initial state LFSR2: 0x{:08x}".format(init_state2))
    
    # --- B5. Mô phỏng tiến (simulate) các LFSR của giai đoạn 1 cho đủ số bước đã “sinh” keystream khi mã hóa file test.
    total_steps = len(test_plain) * 8  # số bit sinh ra trong quá trình mã hóa file test
    # Hàm mô phỏng một bước của LFSR (theo cách làm trong challenge)
    def lfsr_step(state, taps):
        newbit = 0
        for tap in taps:
            newbit ^= (state >> (32 - tap)) & 1
        out = state & 1
        new_state = (state >> 1) | (newbit << 31)
        return new_state, out
    # Sử dụng các tap ban đầu:
    #   LFSR1: taps = [32,22,2,1]
    #   LFSR2: taps = [32,31,30,10]
    s1 = init_state1
    s2 = init_state2
    for i in range(total_steps):
        s1, _ = lfsr_step(s1, [32,22,2,1])
        s2, _ = lfsr_step(s2, [32,31,30,10])
    cur_state1 = s1
    cur_state2 = s2
    
    # --- B6. Tính new_iv bằng cách đảo ngược thứ tự bit (32 bit) của cur_state.
    def bit_reverse(x, bits=32):
        s = bin(x)[2:].zfill(bits)
        return int(s[::-1], 2)
    new_iv1 = bit_reverse(cur_state1, 32)
    new_iv2 = bit_reverse(cur_state2, 32)
    print("new_iv1: 0x{:08x}".format(new_iv1))
    print("new_iv2: 0x{:08x}".format(new_iv2))
    
    # --- B7. Khởi tạo DualLFSR “mới” để giải mã file secret.
    # Lưu ý: taps được hoán đổi so với giai đoạn 1:
    #   - LFSR1 khởi tạo với new_iv1 và tap2 = [32,31,30,10]
    #   - LFSR2 khởi tạo với new_iv2 và tap1 = [32,22,2,1]
    class LFSR:
        def __init__(self, state, taps):
            self.state = state
            self.taps = taps
        def get_bit(self):
            out = self.state & 1
            newbit = 0
            for tap in self.taps:
                newbit ^= (self.state >> (32 - tap)) & 1
            self.state = (self.state >> 1) | (newbit << 31)
            return out
    class DualLFSR:
        def __init__(self, state1, state2, taps1, taps2):
            self.l1 = LFSR(state1, taps1)
            self.l2 = LFSR(state2, taps2)
        def get_bit(self):
            return self.l1.get_bit() ^ self.l2.get_bit()
    
    new_stream = DualLFSR(new_iv1, new_iv2, [32,31,30,10], [32,22,2,1])
    
    # Sinh keystream cho file secret (bit-by-bit, 8 bit ghép thành 1 byte)
    secret_keystream = bytearray()
    num_bytes = len(secret_cipher)
    for i in range(num_bytes):
        byte_val = 0
        for j in range(8):
            bit = new_stream.get_bit()
            byte_val = (byte_val << 1) | bit
        secret_keystream.append(byte_val)
    
    # Giải mã: plaintext_secret = secret_cipher XOR secret_keystream
    secret_plain = bytes([c ^ k for c, k in zip(secret_cipher, secret_keystream)])
    print("Secret plaintext:")
    try:
        print(secret_plain.decode())
    except Exception as e:
        print(secret_plain)
    
if __name__ == "__main__":
    main()
