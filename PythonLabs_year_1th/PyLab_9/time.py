import sys
import time

# sys.stdout.write() nhanh hơn một chút
start = time.time()
for i in range(1000):
    sys.stdout.write('test')
end = time.time()
print(f"sys.stdout.write: {end - start:.4f}s")

start = time.time()
for i in range(1000):
    print('test', end='')  # phải dùng end='' để không xuống dòng
end = time.time()
print(f"print with end='': {end - start:.4f}s")

error_message="error message"

with open("currency_file.txt", mode="a", encoding='utf-8') as file:
    file.write(error_message)
    # file.close() #auto close() if not use open(file_path, mode, encoding)