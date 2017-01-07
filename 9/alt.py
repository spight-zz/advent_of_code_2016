"""
Alternate solution the works left-to-right, as if from a character stream
with minimum memory usage.

To run: python test.py <compressed string>

Output: Numerical length of the uncompressed file

Example:
> python test.py "$(cat input.txt)"
11052855125
"""
import sys


def main():
    dat = []
    total = 0
    factor = 1
    data = sys.argv[1]
    idx = 0

    while idx < len(data):
        while dat and idx > dat[-1][0]:
            factor /= dat.pop()[1]

        if data[idx] != '(':
            total += factor
            idx += 1
            continue

        end_of_marker = data.index(')', idx)

        run_len, new_factor = map(int, data[idx + 1:end_of_marker].split('x'))
        dat.append((run_len + end_of_marker, new_factor))
        factor *= new_factor

        idx = end_of_marker + 1

    print total


if __name__ == '__main__':
    main()
