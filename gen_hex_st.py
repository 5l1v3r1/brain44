import itertools
import sys
import threading
import time
import shutil

hex_chars = '0123456789abcdef'

max_password_length = 9  # Максимальная длина пароля
max_total_length = 64    # Максимальная общая длина строки

def get_config_filename(start_char):
    return f"config_{start_char}.txt"

def save_progress(length, password, shift, start_char):
    with open(get_config_filename(start_char), "w") as f:
        f.write(f"{length}\n")
        f.write("".join(password) + "\n")
        f.write(f"{shift}\n")

def load_progress(start_char):
    try:
        with open(get_config_filename(start_char), "r") as f:
            length = int(f.readline().strip())
            password = f.readline().strip()
            shift = int(f.readline().strip())
            return length, password, shift
    except:
        return 1, "", 0

def backup_results(start_char):
    while True:
        with open(f"found_btc_{start_char}", "r") as source, open(f"result_{start_char}", "a") as target:
            content = source.read()
            if content:
                target.write("\n" + content)
        time.sleep(100)

if len(sys.argv) != 2:
    print("Использование: python3 ваш_скрипт.py [начальный символ]")
    sys.exit(1)

start_char = sys.argv[1]

def generate_string(password, shift):
    base_str = start_char * (max_total_length - len(password)) + ''.join(password)
    return base_str[-shift:] + base_str[:-shift]


length_start, password_start, shift_start = load_progress(start_char)

counter = 0

backup_thread = threading.Thread(target=backup_results, args=(start_char,))
backup_thread.daemon = True
backup_thread.start()

for length in range(length_start, max_password_length + 1):
    if length == length_start:
        passwords = itertools.dropwhile(lambda x: "".join(x) != password_start, itertools.product(hex_chars, repeat=length))
    else:
        passwords = itertools.product(hex_chars, repeat=length)

    for password in passwords:
        for shift in range(shift_start, max_total_length + 1):  
            password_str = generate_string(password, shift)
            print(password_str)
            
            counter += 1
            if counter % 300000 == 0:
                save_progress(length, password, shift + 1, start_char)           
            shift_start = 0
        password_start = ""
        