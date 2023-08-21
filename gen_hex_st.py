import itertools
import sys

hex_chars = '0123456789abcdef'

max_password_length = 7  # Максимальная длина пароля
max_total_length = 64    # Максимальная общая длина строки

if len(sys.argv) != 2:
    print("Использование: python3 ваш_скрипт.py [начальный символ]")
    sys.exit(1)

start_char = sys.argv[1]

for length in range(1, max_password_length + 1):
    passwords = itertools.product(hex_chars, repeat=length)
    for password in passwords:
        for shift in range(max_total_length - length + 1):
            password_str = start_char * shift + ''.join(password) + start_char * (max_total_length - shift - length)
            print(password_str)
