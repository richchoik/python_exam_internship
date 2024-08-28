import argparse
import os
import re
import requests
import html
import sys

EXPLOIT_DIR = './exploit-db' #thư mục lưu trữ exploit

def check_value(value):
    pattern = r'^\d+$'
    return bool(re.match(pattern, value))

def get_id(value): #lấy id từ input
    pattern = r'/(\d+)$' #regex để lấy id từ url
    iden = re.search(pattern, value)
    if iden:
       return iden.group(1)
    else:
        if not check_value(value):
            parser.print_help()
            sys.exit(1)
        else :
            return value

def create_dir():
    if not os.path.exists(EXPLOIT_DIR): 
        os.makedirs(EXPLOIT_DIR)

def exploit_func(value): #xử lý exploit
    exploit_id = get_id(value)
    if exploit_id:
        create_dir()
        filename = os.path.join(EXPLOIT_DIR, f'{exploit_id}.txt') 
        if os.path.exists(filename): #nếu đã có sẵn thì mở
            os.startfile(filename)
        else:
            download_exploit(exploit_id) #ko thì tải về rồi mở
            os.startfile(filename)

def download_exploit(exploit_id): 
    url = 'https://exploit-db.com/exploits/{}'.format(exploit_id) 
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'} 
    res = requests.get(url, headers=headers) 
    
    if res.status_code == 200: #request thành công
        exploit_content = res.text[res.text.find('<code') : res.text.find('</code>')] #lấy nội dung exploit trong thẻ <code> của html
        exploit_content = html.unescape(exploit_content[exploit_content.find('">') +2 :]) 
        
        if exploit_content: 
            filename = os.path.join(EXPLOIT_DIR, f'{exploit_id}.txt') #tạo file
            with open(filename, 'w') as file: 
                file.write(exploit_content) 
        else: 
            print(f"Can not get content from {url}") 
    else: 
        print(f"Error {url}")

def page_func(value):
    try:
        value = int(value)
        if value < 0:
            parser.print_help()
            sys.exit(1)

        exploit_files = sorted(os.listdir(EXPLOIT_DIR), key=lambda x: int(x.split('.')[0]))
        start_index = value * 5
        end_index = (value + 1) * 5

        for filename in exploit_files[start_index:end_index]:
            exploit_id = os.path.splitext(filename)[0]
            print(exploit_id)
    except ValueError as ve:
        print(f"Lỗi: {ve}")

def search_func(keyword):
    try:
        words = [word.strip() for word in keyword.split()] #tách từ + bỏ khoảng trắng
        pattern = re.compile(fr'\b({"|".join(words)})\b', re.IGNORECASE)
        for filename in os.listdir(EXPLOIT_DIR):
            exploit_id = filename[:-4]
            with open(os.path.join(EXPLOIT_DIR, filename), 'r') as file:
                content = file.read()
                if any(word.lower() in content.lower() for word in words): #check xem exploit có bất kỳ từ nào 
                    if pattern.sub("", content.lower()) != content.lower():#check xem nó ko nằm trong các từ khác
                        print(f'./exploit-db/{exploit_id}.txt')
    except Exception as e:
        print(f"Lỗi: {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Python Exam')
    parser.add_argument('--exploit', help='exploit ID')
    parser.add_argument('--page', help='get page')
    parser.add_argument('--search', help='search keyword')
    
    if len(sys.argv) == 2:
        parser.print_help()
        sys.exit(1)
        
    args = parser.parse_args()

    if args.exploit:
        exploit_func(args.exploit)
    elif args.page:
        page_func(args.page)
    elif args.search:
        search_func(args.search)


