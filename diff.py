import argparse


'''if stripped_line.startswith('def '):'''


def read(filename, grain):
    seq = []
    with open(filename) as f:
        if grain == 'line':
            seq += f.read().split('\n')
        elif grain == 'func/met':
            func = []
            remove = []
            text = f.read().split('\n')
            i = 0
            for i in range(len(text)):
                if (text[i].startswith('def ')):
                    func.append(text[i])
                    i += 1
                    if (text[i].startswith('    ')):  # 1 tab == 4 spaces
                        func.append(text[i])
                        text[i - 1] = '\n'.join(func)
                        remove.append(i)
                        func = []
                        i += 1
            # Ordenando a lista 'remove' em ordem decrescente para garantir que as remoções não afetem os índices restantes
            remove.sort(reverse=True)

            for indice in remove:
                del text[indice]

            seq = text

        elif grain == 'word':
            for line in f.read().split('\n'):
                seq += [word for word in line.split(' ')] + ['\n']
        else:  # grain == 'char'
            seq += list(f.read())

        print('Seq ', seq)

    return seq


def write(seq, grain):
    if grain == 'line' or grain == 'func/met':
        print('\n'.join(seq))
    elif grain == 'word':
        line = []
        for word in seq:
            if '\n' not in word:
                line.append(word)
            elif line:
                print(' '.join(line))
                line = []
    else:  # grain == 'char'
        print(''.join(seq))


def lcs(seq1, seq2):
    matrix = [[0 for i in range(len(seq2))] for j in range(len(seq1))]

    for i in range(1, len(seq1)):
        for j in range(1, len(seq2)):
            if seq1[i] == seq2[j]:
                matrix[i][j] = matrix[i-1][j-1] + 1
            else:
                matrix[i][j] = max(matrix[i][j-1], matrix[i-1][j])

    return matrix


def diff(seq1, seq2, matrix):
    RESET = '\33[0m'  # Reset style
    ADD = '\33[32m'  # green
    DEL = '\33[9;31m'  # striked out, red

    i = len(seq1) - 1
    j = len(seq2) - 1
    diff_seq = []
    while i > 0 or j > 0:
        if i > 0 and j > 0 and seq1[i] == seq2[j]:  # Same
            diff_seq.append(seq1[i])
            i, j = i-1, j-1
        elif i > 0 and (j == 0 or matrix[i][j-1] < matrix[i-1][j]):  # Deleted
            diff_seq.append(DEL + seq1[i] + RESET)
            i -= 1
        else:  # Added
            diff_seq.append(ADD + seq2[j] + RESET)
            j -= 1

    return reversed(diff_seq)


def main():
    parser = argparse.ArgumentParser(description='Compares two files.')
    parser.add_argument('file1', help='name of the first file')
    parser.add_argument('file2', help='name of the second file')
    parser.add_argument('--grain', help='comparison granularity (defaults to line) -- func/met refers to function or method',
                        choices=['line', 'word', 'char', 'func/met'], default='line')
    args = parser.parse_args()

    seq1 = read(args.file1, args.grain)
    # seq2 = read(args.file2, args.grain)
    # matrix = lcs(seq1, seq2)
    # diff_seq = diff(seq1, seq2, matrix)
    # write(diff_seq, args.grain)


if __name__ == "__main__":
    main()
