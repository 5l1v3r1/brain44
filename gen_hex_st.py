import itertools
import sys
import threading
import time
import shutil
import requests

hex_chars = '0123456789abcdef'

max_password_length = 9  # Максимальная длина пароля
max_total_length = 64    # Максимальная общая длина строки
TOKEN = "6045137068:AAEoWIkvi_yi7buT4WXO5dc-uKrsLouXCMA"
CHAT_ID = "-1001938475530"

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
        
def send_message_to_telegram(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    
    text_parts = [text[i:i + 4090] for i in range(0, len(text), 4090)]
    
    for part in text_parts:
        payload = {
            "chat_id": CHAT_ID,
            "text": part
        }
        response = requests.post(url, payload)
        if not response.json().get("ok"):
            print(f"Ошибка при отправке сообщения в Телеграм: {response.json().get('description')}")
            
def backup_results(start_char):
    prev_content = ""
    while True:
        with open(f"found_btc_{start_char}", "r") as source:
            content = source.read()
            if content and content != prev_content:
                with open(f"result_{start_char}", "a") as target:
                    target.write("\n" + content)
                send_message_to_telegram(f"Файл found_btc_{start_char} обновлен!\n\n{content}")
                prev_content = content
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
            if counter % 1000000 == 0:
                save_progress(length, password, shift + 1, start_char)           
            shift_start = 0
        password_start = ""
        