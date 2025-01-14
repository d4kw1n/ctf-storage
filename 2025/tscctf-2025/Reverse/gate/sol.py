
def sub_13D0(a1, a2):
    result = len(a1)

    if result > 0:
        v3 = 1
        while v3 <= result:
            a2[v3 - 1] = (v3 ^ ord(a1[v3 - 1])) + 5
            v3 += 1

    a2[result] = 0
    print("".join([chr(i) for i in a2]))
    return result
# 6452215056652653662B656A723D4C4E
v4 = "66694134474336797B3B653D7F4B6452215056652653662B656A723D4C4E"
v4 = [int(v4[i:i+2], 16) for i in range(0, len(v4), 2)][::-1]

# Convert to string
v4 = "".join([chr(i) for i in v4])
a2 = [0] * 0x32
print(sub_13D0(v4, a2))