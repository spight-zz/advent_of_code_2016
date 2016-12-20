import hashlib

class Project(object):
    def __init__(self, unique_id):
        self.id = unique_id

    def run1(self, ):
        i = 0
        for found, _ in self.next:
            i += 1
            print(found)
            if i == 8:
                break

    def run2(self, ):
        output = [None] * 8
        i = 0
        for pos, found in self.next:
            print pos, found
            try:
                pos = int(pos)
            except ValueError:
                continue
            if pos < 8 and output[pos] is None:
                print("Adding to password")
                output[pos] = found
                i += 1
                if i == 8:
                    break

        print(''.join(output))

    @property
    def next(self):
        i = 0
        while True:
            key = self.id + str(i)
            hashed = hashlib.md5(key).hexdigest()
            if hashed.startswith('00000'):
                yield hashed[5], hashed[6]
            i += 1





if __name__ == '__main__':
    # Project('abc').run()
    Project('abbhdwsy').run2()
