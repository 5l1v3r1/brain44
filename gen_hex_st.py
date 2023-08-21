import itertools

hex_chars = '0123456789abcdef'
start_chars = '1'
max_password_length = 7
max_total_length = 64

for start_char in start_chars:
    for length in range(1, max_password_length + 1):
        passwords = itertools.product(hex_chars, repeat=length)
        for password in passwords:
            for shift in range(max_total_length - length + 1):
                password_str = start_char * shift + ''.join(password) + start_char * (max_total_length - shift - length)
                print(password_str)
