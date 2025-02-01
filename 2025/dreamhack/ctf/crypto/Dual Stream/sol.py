# Mảng byte_404060 có 15,625 phần tử (byte), mỗi phần chỉ nhận giá trị 0 hoặc 1.
# Dữ liệu được “mã hóa” theo các lệnh db … dup(...) trong mã hợp dịch.
# Lưu ý: Các số dạng “1231h” được hiểu là số hex (ví dụ 0x1231) và “dup(n)” nghĩa là lặp lại n lần.

byte_404060 = (
    # Tại offset 0x404060:
    [1] * 0x1231 +         # 0x1231 dup(1)
    [0] * 9 +              # 9 dup(0)
    [1] * 0x10 +           # 0x10 dup(1)
    [0, 1, 0] +            # 0, 1, 0
    [1] * 0x253 +          # 0x253 dup(1)

    # Tiếp tục tại offset 0x405500:
    [0] +
    [1] * 2 +              # 2 dup(1)
    [0] +
    [1] * 6 +              # 6 dup(1)
    [0] +
    [1] * 0xE +            # 0xE dup(1)
    [0] * 5 +              # 5 dup(0)
    [1] * 9 +              # 9 dup(1)

    # Offset 0x405527:
    [0] +
    [1] * 0x18 +           # 0x18 dup(1)
    [0] +
    [1] * 0x18 +           # 0x18 dup(1)
    [0] +
    [1] * 0x14 +           # 0x14 dup(1)
    [0] * 5 +              # 5 dup(0)

    # Offset 0x405573:
    [1] * 0x14 +           # 0x14 dup(1)
    [0] +
    [1] * 0x18 +           # 0x18 dup(1)
    [0] +
    [1] * 0x18 +           # 0x18 dup(1)
    [0] +
    [1] * 0x1B6 +          # 0x1B6 dup(1)

    # Offset 0x405770:
    [0] * 2 +              # 2 dup(0)
    [1] * 9 +              # 9 dup(1)
    [0] +
    [1] * 7 +              # 7 dup(1)
    [0] +
    [1] * 4 +              # 4 dup(1)
    [0] * 2 +              # 2 dup(0)

    # Offset 0x40578A:
    [1] * 0xE +            # 0xE dup(1)
    [0] +
    [1] * 3 +              # 3 dup(1)
    [0] +
    [1] * 0x18 +           # 0x18 dup(1)
    [0] +
    [1] * 0x18 +           # 0x18 dup(1)

    # Offset 0x4057CE:
    [0] +
    [1] * 0x18 +           # 0x18 dup(1)
    [0] +
    [1] * 0x18 +           # 0x18 dup(1)
    [0] +
    [1] * 0x18 +           # 0x18 dup(1)
    [0] +
    [1] * 0x10 +           # 0x10 dup(1)

    # Offset 0x40582A:
    [0] +
    [1] * 0x1C1 +          # 0x1C1 dup(1)
    [0] +
    [1] * 7 +              # 7 dup(1)
    [0] +
    [1] +                  # 1
    [0] * 4 +              # 4 dup(0)
    [1] * 0xF +            # 0xF dup(1)

    # Offset 0x405A09:
    [0] +
    [1] * 0x80 +           # 0x80 dup(1)
    [0] +
    [1] * 0x10 +           # 0x10 dup(1)
    [0] +
    [1] * 0x1C1 +          # 0x1C1 dup(1)
    [0] +
    [1] * 7 +              # 7 dup(1)

    # Offset 0x405C65:
    [0, 1, 0] +
    [1] * 0x12 +           # 0x12 dup(1)
    [0] +
    [1] * 0x18 +           # 0x18 dup(1)
    [0] +
    [1] * 0x18 +           # 0x18 dup(1)
    [0] +

    # Offset 0x405CAD:
    [1] * 0x18 +           # 0x18 dup(1)
    [0] +
    [1] * 0x18 +           # 0x18 dup(1)
    [0] +
    [1] * 0x18 +           # 0x18 dup(1)
    [0] * 5 +              # 5 dup(0)

    # Offset 0x405CFC:
    [1] * 0x10 +           # 0x10 dup(1)
    [0] +
    [1] * 0x1C1 +          # 0x1C1 dup(1)
    [0] +
    [1] * 7 +              # 7 dup(1)
    [0, 1, 0] +
    [1] * 0xE +            # 0xE dup(1)

    # Offset 0x405EE7:
    [0] +
    [1] * 7 +              # 7 dup(1)
    [0] * 2 +              # 2 dup(0)
    [1] * 0xF +            # 0xF dup(1)
    [0] +
    [1] * 7 +              # 7 dup(1)
    [0] +
    [1] * 0x10 +           # 0x10 dup(1)

    # Offset 0x405F19:
    [0] +
    [1] * 7 +              # 7 dup(1)
    [0] +
    [1] * 0x10 +           # 0x10 dup(1)
    [0] +
    [1] * 7 +              # 7 dup(1)
    [0] +
    [1] * 0x10 +           # 0x10 dup(1)

    # Offset 0x405F4B:
    [0] +
    [1] * 7 +              # 7 dup(1)
    [0] +
    [1] * 0x10 +           # 0x10 dup(1)
    [0] +
    [1] * 7 +              # 7 dup(1)
    [0] +
    [1] * 0x10 +           # 0x10 dup(1)

    # Offset 0x405F7D:
    [0] +
    [1] * 0x1C9 +          # 0x1C9 dup(1)
    [0] +
    [1] * 0x95 +           # 0x95 dup(1)
    [0] +
    [1] * 0x1DA +          # 0x1DA dup(1)
    [0] +
    [1] * 0x95 +           # 0x95 dup(1)

    # Offset 0x40644E:
    [0] +
    [1] * 0x1DA +          # 0x1DA dup(1)
    [0] +
    [1] * 0x95 +           # 0x95 dup(1)
    [0] +
    [1] * 0x1DA +          # 0x1DA dup(1)
    [0] +
    [1] * 0x95 +           # 0x95 dup(1)

    # Offset 0x406930:
    [0] +
    [1] * 0x1DA +          # 0x1DA dup(1)
    [0] +
    [1] * 0x18 +           # 0x18 dup(1)
    [0] +
    [1] * 0x18 +           # 0x18 dup(1)
    [0] +
    [1] * 0x18 +           # 0x18 dup(1)

    # Offset 0x406B56:
    [0] +
    [1] * 0x18 +           # 0x18 dup(1)
    [0] +
    [1] * 0x18 +           # 0x18 dup(1)
    [0] +
    [1] * 0x18 +           # 0x18 dup(1)
    [0] +
    [1] * 0x11C7          # 0x11C7 dup(1)
)

def sub_401348(a1):
    """
    a1: Iterable chứa các giá trị byte (số nguyên 0..255). 
        Duyệt tối đa 256 phần tử, dừng khi gặp giá trị 0.
    Trả về 1 nếu đạt điều kiện, 0 nếu không.
    """
    # Nếu sub_40127A không chấp nhận đầu vào, trả về 0
    if not sub_40127A(a1):
        return 0

    # Khởi tạo các biến theo code C:
    v3 = 24
    v4 = 12
    v5 = 12

    # Gọi sub_401196 với trạng thái ban đầu
    sub_401196(24, 12, 12)

    # Duyệt tối đa 256 byte trong a1
    for j in range(256):
        # Nếu đã hết phần tử hoặc gặp byte 0 (kết thúc chuỗi)
        if j >= len(a1) or a1[j] == 0:
            break

        v2 = a1[j]  # Lấy giá trị byte (số nguyên)
        if v2 == 122:  # 122 là mã của 'z'
            v4 += 1
        else:
            if v2 > 122:
                return 0
            if v2 == 115:  # 115 là mã của 's'
                v5 -= 1
            else:
                if v2 > 115:
                    return 0
                if v2 == ord('K'):  # 'K' có mã 75
                    v3 += 1
                else:
                    if v2 > 75:
                        return 0
                    if v2 == ord('9'):  # '9' có mã 57
                        v3 -= 1
                    else:
                        if v2 > 57:
                            return 0
                        if v2 == 50:  # 50 là mã của '2'
                            v5 += 1
                        else:
                            if v2 != 55:  # 55 là mã của '7'
                                return 0
                            v4 -= 1

        # Nếu trạng thái đạt điều kiện: v3==0, v4==12, v5==12 → trả về 1
        if v3 == 0 and v4 == 12 and v5 == 12:
            return 1

        # Kiểm tra trạng thái hiện tại với sub_4011EB, nếu không hợp lệ thì trả về 0
        if not sub_4011EB(v3, v4, v5):
            print(f"[1] Trạng thái không hợp lệ: {v3}, {v4}, {v5}")
            print(f"Result: {sub_4011EB(v3, v4, v5)}")
            return 0

        # Ghi lại trạng thái hiện tại
        sub_401196(v3, v4, v5)
    print(f"[2] Trạng thái cuối cùng: {v3}, {v4}, {v5}")
    return 0

# --- Ví dụ định nghĩa các hàm hỗ trợ (placeholder) ---
# Bạn cần thay đổi nội dung của các hàm dưới đây theo logic ban đầu của chương trình.

def sub_40127A(a1):
    """
    Kiểm tra xem chuỗi a1 có chỉ chứa các ký tự hợp lệ không.
    Ví dụ: chỉ chấp nhận các ký tự 'K', '9', 'z', '7', '2', 's' (và ký tự 0 kết thúc).
    """
    valid = {ord('K'), ord('9'), ord('z'), ord('7'), ord('2'), ord('s')}
    for b in a1:
        if b == 0:
            break
        if b not in valid:
            return False
    return True

def sub_401196(a, b, c):
    """
    Ghi nhận (hoặc đánh dấu) trạng thái (a, b, c).
    Ở đây ta chỉ in ra để kiểm tra.
    """
    # Ví dụ: in ra trạng thái
    # Trong code thực, trạng thái này được dùng để “đánh dấu” vị trí trong mảng 3D.
    # Bạn có thể bỏ qua hoặc xử lý theo mục đích.
    print(f"sub_401196({a}, {b}, {c})")
    return

def sub_4011EB(a, b, c):
    """
    Kiểm tra trạng thái (a, b, c) có hợp lệ không.
    Ở đây giả sử rằng các giá trị không vượt quá một ngưỡng (ví dụ 24).
    """
    # Ví dụ: Nếu a, b, c <= 24 thì hợp lệ, ngược lại không hợp lệ.
    d = 625 * a + 25 * b + c
    print(f"sub_4011EB({a}, {b}, {c})")
    print(f"Index: {d}")
    if a <= 24 and b <= 24 and c <= 24 and byte_404060[d] != 1:
        return True
    try:
        print(f"byte_404060[{d}] = {byte_404060[d]}")
    except IndexError:
        print(f"Index {d} out of range")
    return False

# --- Ví dụ sử dụng hàm sub_401348 ---
if __name__ == "__main__":
    # Ví dụ: Chuỗi hợp lệ chứa các ký tự hợp lệ (dạng số nguyên), kết thúc bằng 0
    # Giả sử chuỗi: "K9z7" (tương ứng mã: [75, 57, 122, 55]) và kết thúc bởi 0.
    right_input = []
    
    right_char = [57, 75, 122, 55, 50, 115]
    start_status = [24, 12, 12]
    index = 0
    for i in range(len(byte_404060)):
        if byte_404060[i] == 0:
            print(f"Index: {i}")
    
    while index < 256:
        for char in right_char:
            copy_data = start_status.copy()
            if char == 75:
                copy_data[0] += 1
            elif char == 57:
                copy_data[0] -= 1
            elif char == 122:
                copy_data[1] += 1
            elif char == 55:
                copy_data[1] -= 1
            elif char == 50:
                copy_data[2] += 1
            elif char == 115:
                copy_data[2] -= 1
            if sub_4011EB(copy_data[0], copy_data[1], copy_data[2]):
                right_input.append(char)
                print(f"Right input: {right_input}")
                start_status = copy_data
                break
        index += 1
    print(f"Right input: {right_input}")
    