#!/usr/bin/env python3

# (1) Định nghĩa mảng dword_4060 (lấy từ IDA):
dword_4060 = [
  0x11A3E, 0x1C6FB, 0xFFFFFFFF, 0xFFFFFFFF, 0xFFFFFFFF, 0xFFFFFFFF, 0xFFFFFFFF, 0xFFFFFFFF,
  # ...
  # Bạn phải chép HẾT từ 0x4060.. đến hết (như trong phần .data).
  # Dữ liệu rất dài, cần cẩn thận!
]

# (2) Định nghĩa dword_4020 (16 phần tử):
dword_4020 = [
  0x6E42DB36, 0x50EE7196, 0x66F61F93, 0x58F59D02,
  0x5E4FAE58, 0x6941CEE7, 0x47F8A1AB, 0x59C2E48E,
  0x5764C85A, 0x62CE2FE1, 0x425BCB1A, 0x65430112,
  0x7FE80600, 0x5DBF3584, 0x5210221A, 0x6E30EE7F
]

# (3) Tạo bảng nextState: nextState[st][0 or 1] = dword_4060[2*st + (0 or 1)]
#    Tìm giới hạn st tối đa: = len(dword_4060)//2
#    Giả sử ta kiểm tra st==-1 hoặc st>0x3FFFF => invalid => ta đặt nextState[st][bit] = -2
#    (để đánh dấu đường cụt).
import sys

MAX_STATE = len(dword_4060)//2  # phỏng đoán
nextState = []
for st in range(MAX_STATE):
    n0 = dword_4060[2*st + 0]
    n1 = dword_4060[2*st + 1]
    def fix(x):
        # if x == -1 or x>0x3FFFF => ta coi như -2
        if x == 0xFFFFFFFF or x > 0x3FFFF:
            return -2
        return x
    nextState.append( [ fix(n0), fix(n1) ] )

# (4) Duyệt mọi n = 0..65535 => mô phỏng "LSB trước" => final state
final_map = {}  # final_map[ finalState ] = n

for n in range(65536):
    st = 0
    tmp = n
    valid = True
    for _ in range(16):  # 16 bit
        bit = (tmp & 1)
        tmp >>= 1
        if st < 0 or st >= MAX_STATE:
            valid = False
            break
        st = nextState[st][bit]
        if st == -2:  # đường cụt
            valid = False
            break
    if valid:
        # st là trạng thái cuối
        # Lưu vào map nếu st chưa có
        # (nhiều n có thể cùng ra st => hy vọng challenge set unique)
        if st not in final_map:
            final_map[st] = n

# (5) Giờ, cho i in [0..15], finalState = dword_4020[i],
#     lấy n = final_map[finalState], rồi chuyển n -> 4 hex-digit (uppercase, v.v.)
blocks = []
for fs in dword_4020:
    if fs not in final_map:
        print(f"Không tìm thấy 16-bit sequence dẫn đến state=0x{fs:08X} !", file=sys.stderr)
        sys.exit(1)
    n = final_map[fs]
    # n là [0..65535], đổi ra 4 hex-digit
    block_hex = f"{n:04X}"
    blocks.append(block_hex)

# (6) Ghép 16 block => chuỗi 64 ký tự
answer = "".join(blocks)
print("Final input (64 hex-digit) =", answer)

# Kiểm tra:
#  => Gõ input = answer cho hàm sub_11E0 => vượt check => Done.
