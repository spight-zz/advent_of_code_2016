import hashlib
import re


class Project(object):
    def __init__(self, salt, retention=1000):
        self.salt = salt
        self.potential = []
        self.current_hash_idx = 0
        self.retention = retention
        self.purge_rate = 1000
        self.trip = re.compile('(.)\\1\\1')
        self.quint = re.compile('(.)\\1\\1\\1\\1')

    def add_potential(self, trip_chr, hash_, key):
        self.potential.append((trip_chr, hash_, self.current_hash_idx, key))

    def purge(self):
        cutoff = self.current_hash_idx - self.retention
        for hash_ in self.potential:
            if hash_[2] < cutoff:
                self.potential.remove(hash_)

    def get_trip(self, hash_):
        match = self.trip.search(hash_)
        if match:
            return match.group(1)

    def get_quints(self, hash_):
        quints = []
        matches = self.quint.findall(hash_)
        if matches:
            for match in matches:
                quints.append(match)
        return quints

    def stretch_good(self, key):
        hash_ = hashlib.md5(key).hexdigest()
        for i in range(2016):
            hash_ = hashlib.md5(hash_).hexdigest()
        return hash_

    def run1(self, stretch=False):
        self.current_hash_idx = 0
        self.potential = []
        pad_keys = []
        end_times = None

        while end_times is None or end_times > self.current_hash_idx:
            key = self.salt + str(self.current_hash_idx)

            if stretch:
                hash_ = self.stretch_good(key)
            else:
                hash_ = hashlib.md5(key).hexdigest()

            quints = self.get_quints(hash_)
            if quints:
                cutoff = self.current_hash_idx - self.retention
                newly_added = []

                for pot in self.potential:
                    if pot[0] in quints and pot[2] >= cutoff:
                        pad_keys.append((pot, (hash_, self.current_hash_idx)))
                        newly_added.append(pot)

                for pot in newly_added:
                    self.potential.remove(pot)

            trip = self.get_trip(hash_)

            if trip:
                self.add_potential(trip, hash_, key)

            if self.current_hash_idx % self.purge_rate == 0:
                self.purge()

            self.current_hash_idx += 1

            if end_times is None and len(pad_keys) >= 64:
                end_times = self.current_hash_idx + 1001

        return sorted(pad_keys, key=lambda x: x[0][2])[63][0][2]

    def run2(self,):
        return self.run1(stretch=True)


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        p = Project(f.read().strip())

        print "Part 1:", p.run1()
        print "Part 2:", p.run2()
