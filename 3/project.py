import sys

class Project(object):
    def __init__(self, ):
        pass

    def run1(self, ):
        total = 0
        valid = 0

        for line in sys.stdin:
            triangle = self.get_triangle(line.split())
            total += 1

            if self.check(triangle):
                valid += 1
                print triangle, True
            else:
                print triangle, False

        print("Total: %s\nValid: %s" % (total, valid))

    def run2(self, ):
        total = 0
        valid = 0
        for triangle in self.triangles:
            total += 1
            if self.check(triangle):
                valid += 1
                print(triangle, True)
            else:
                print(triangle, False)

        print("Total: %s\nValid: %s" % (total, valid))


    def check(self, triangle):
        return triangle[0] + triangle[1] > triangle[2]

    def get_triangle(self, triangle):
        for i in range(len(triangle)):
            triangle[i] = int(triangle[i])
        return sorted(triangle)

    @property
    def triangles(self):
        while True:
            try:
                line1 = sys.stdin.next().split()
                line2 = sys.stdin.next().split()
                line3 = sys.stdin.next().split()

                for i in [0, 1, 2]:
                    yield self.get_triangle([line1[i], line2[i], line3[i]])
            except StopIteration:
                break




if __name__ == '__main__':
    Project().run2()
