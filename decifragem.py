import sys

def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def write_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)

def kamasutra_decipher(text, key):
    mapping = dict(zip(key[:len(key)//2], key[len(key)//2:]))
    mapping.update(dict(zip(key[len(key)//2:], key[:len(key)//2])))
    return ''.join(mapping.get(c, c) for c in text)

def alberti_decipher(text, key):
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    shifted_alphabet = key + ''.join(c for c in alphabet if c not in key)
    return ''.join(alphabet[shifted_alphabet.index(c)] if c in shifted_alphabet else c for c in text)

def adfgvx_decipher(text, key):
    adfgvx_square = {
        'A': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',
        'D': 'BCDEFGHIJKLMNOPQRSTUVWXYZ0123456789A',
        'F': 'CDEFGHIJKLMNOPQRSTUVWXYZ0123456789AB',
        'G': 'DEFGHIJKLMNOPQRSTUVWXYZ0123456789ABC',
        'V': 'EFGHIJKLMNOPQRSTUVWXYZ0123456789ABCD',
        'X': 'FGHIJKLMNOPQRSTUVWXYZ0123456789ABCDE'
    }
    return ''.join(adfgvx_square[c][key.index(c)] if c in adfgvx_square else c for c in text)

def feistel_network_decipher(text, key, rounds=2):
    def feistel_round(left, right, key):
        new_left = right
        new_right = ''.join(chr(ord(l) ^ ord(k)) for l, k in zip(left, key))
        return new_left, new_right
    
    left, right = text[:len(text)//2], text[len(text)//2:]
    for _ in range(rounds):
        left, right = feistel_round(left, right, key)
    return left + right

def decrypt(text, key):
    text = feistel_network_decipher(text, key)
    text = adfgvx_decipher(text, key)
    text = alberti_decipher(text, key)
    return kamasutra_decipher(text, key)

if __name__ == "__main__":
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    key = sys.argv[3] if len(sys.argv) > 3 else read_file('key.txt')
    
    ciphertext = read_file(input_file)
    plaintext = decrypt(ciphertext, key)
    if plaintext is None:
        print("Error: Plaintext is None")
    else:
        write_file(output_file, plaintext)
