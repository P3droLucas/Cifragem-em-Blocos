import sys

def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def write_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)

def kamasutra_cipher(text, key):
    mapping = dict(zip(key[:len(key)//2], key[len(key)//2:]))
    mapping.update(dict(zip(key[len(key)//2:], key[:len(key)//2])))
    return ''.join(mapping.get(c, c) for c in text)

def alberti_cipher(text, key):
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    shifted_alphabet = key + ''.join(c for c in alphabet if c not in key)
    return ''.join(shifted_alphabet[alphabet.index(c)] if c in alphabet else c for c in text)

def adfgvx_cipher(text, key):
    adfgvx_square = {
        'A': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',
        'D': 'BCDEFGHIJKLMNOPQRSTUVWXYZ0123456789A',
        'F': 'CDEFGHIJKLMNOPQRSTUVWXYZ0123456789AB',
        'G': 'DEFGHIJKLMNOPQRSTUVWXYZ0123456789ABC',
        'V': 'EFGHIJKLMNOPQRSTUVWXYZ0123456789ABCD',
        'X': 'FGHIJKLMNOPQRSTUVWXYZ0123456789ABCDE'
    }
    return ''.join(adfgvx_square[c][key.index(c)] if c in adfgvx_square else c for c in text)

def feistel_network(text, key, rounds=2):
    def feistel_round(left, right, key):
        new_left = right
        new_right = ''.join(chr(ord(l) ^ ord(k)) for l, k in zip(left, key))
        return new_left, new_right
    
    left, right = text[:len(text)//2], text[len(text)//2:]
    for _ in range(rounds):
        left, right = feistel_round(left, right, key)
    return left + right

def encrypt(text, key):
    text = kamasutra_cipher(text, key)
    text = alberti_cipher(text, key)
    text = adfgvx_cipher(text, key)
    return feistel_network(text, key)

if __name__ == "__main__":
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    key = sys.argv[3] if len(sys.argv) > 3 else read_file('key.txt')
    
    plaintext = read_file(input_file)
    ciphertext = encrypt(plaintext, key)
    if ciphertext is None:
        print("Error: Ciphertext is None")
    else:
        write_file(output_file, ciphertext)
