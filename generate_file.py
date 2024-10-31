import random
import string

letters = string.ascii_lowercase  # 'abcdefghijklmnopqrstuvwxyz'
total_size = 1 * 1024 * 1025

# with open('file1.txt', 'w') as f:
#     f.write(''.join(random.choice(string.ascii_letters) for _ in range(1 * 1024 * 512)))

with open('file1.txt', 'w') as f:
    for i in range(total_size):
        f.write(letters[i % len(letters)])