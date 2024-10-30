import random
import string

with open('file1.txt', 'w') as f:
    f.write(''.join(random.choice(string.ascii_letters) for _ in range(1 * 1024 * 1025)))
with open('file2.txt', 'w') as f:
    f.write(''.join(random.choice(string.ascii_letters) for _ in range(1 * 1024 * 1025)))