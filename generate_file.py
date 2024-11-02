import string

normalLetters = string.ascii_lowercase  # 'abcdefghijklmnopqrstuvwxyz'
invertedLetters = string.ascii_lowercase[::-1]  # 'zyxwvutsrqponmlkjihgfedcba'
total_size = 1 * 1024 * 1025

# with open('file1.txt', 'w') as f:
#     f.write(''.join(random.choice(string.ascii_letters) for _ in range(1 * 1024 * 512)))

with open('file1.txt', 'w') as f:
    for i in range(total_size):
        f.write(normalLetters[i % len(normalLetters)])

with open('file2.txt', 'w') as f:
    for i in range(total_size):
        f.write(invertedLetters[i % len(invertedLetters)])