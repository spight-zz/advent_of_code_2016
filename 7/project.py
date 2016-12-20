import sys
import re

class Project(object):
    def __init__(self, ):
        pass

    def run1(self, ):
        total = 0
        valid = 0
        for line in sys.stdin:
            total += 1
            line = line.strip()
            if self.check_line1(line):
                valid += 1
                print("Works: %s" % line)
            else:
                print("Fuck: %s" % line)

        print total, valid


    def check_line1(self, line):
        nets, hypernets = self.extract(line)
        for hypernet in hypernets:
            if self.is_abba(hypernet):
                return False
        for net in nets:
            if self.is_abba(net):
                return True

    def run2(self):
        total = 0
        valid = 0
        for line in sys.stdin:
            total += 1
            line = line.strip()
            if self.check_line2(line):
                valid += 1
        print total, valid


    def check_line2(self, line):
        nets, hypernets = self.extract(line)
        nabas = []
        habas = []
        for net in nets:
            nabas += self.find_abas(net)

        for hypernet in hypernets:
            habas += self.find_abas(hypernet)

        for i, haba in enumerate(habas):
            habas[i] = haba[1] + haba[0] + haba[1]

        for naba in nabas:
            if naba in habas:
                return True

        return False

    def extract(self, line):
        """Extract 'hypernets' from IPv7 address"""
        ip_sections = []
        hypernets = []

        line = str(line)  # Copy line for manipulation
        while True:
            section, _, hypernet, line = re.match(r'([a-z]+)(\[([a-z]+)\])?(.*)$', line).groups()
            ip_sections.append(section)
            if hypernet is None:
                break
            else:
                hypernets.append(hypernet)

        return ip_sections, hypernets

    def find_abas(self, net, aba=None):
        matches = []

        for match in re.finditer('(?=((\w)(\w)\\2))', net):
            if match.group(2) != match.group(3):
                matches.append(match.group(1))

        return matches


    def is_abba(self, net):
        """Check whether a net is ABBA or not"""
        for match in re.finditer('(?=((\w)(\w)\\3\\2))', net):
            if match.group(2) != match.group(3):
                return True
        return False




if __name__ == '__main__':
    Project().run2()
