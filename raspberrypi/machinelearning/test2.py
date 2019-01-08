import unittest
from test1 import no_name_new
import random

class TestNoName(unittest.TestCase):
    def test_init(self):
        pass

    def test_positive(self):
        for i in range(0,50):
            s1,s2 = self.generate_positive()
            self.assertEqual(self.no_name(s1,s2),no_name_new(s1,s2))

    def test_negtive(self):
        for i in range(0,50):
            s1,s2 = self.generate_negtive()
            self.assertEqual(self.no_name(s1,s2),no_name_new(s1,s2))

    def generate_positive(self):
        string_length = random.randint(1, 50)
        string1 = []
        for _ in range(string_length):
            string1.extend(random.sample(
            ['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g', 'f',
             'e', 'd', 'c', 'b', 'a'], 1))
        random_string1 = ''.join(string1)
        random_string2 = ''.join(random.sample(string1, string_length))
        return random_string1, random_string2

    def generate_negtive(self):
        string_length = random.randint(1, 50)
        string1 = []
        string2 = []
        for _ in range(string_length):
            string1.extend(random.sample(
            ['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g', 'f',
             'e', 'd', 'c', 'b', 'a'], 1))
        for _ in range(string_length):
            string2.extend(random.sample(
            ['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g', 'f',
             'e', 'd', 'c', 'b', 'a'], 1))
        random_string1 = ''.join(string1)
        random_string2 = ''.join(string2)
        return random_string1, random_string2

    def no_name(self,a,b):
        if len(a) != len(b):
            return False
        for x in range(0,len(b)):
            if a[0] == b[x]:
                return self.no_name(self.utilityFunction(a,0),self.utilityFunction(b,x))
        return len(b) == 0

    def utilityFunction(self,s,j):
        ret = ['' for i in range(0,len(s))]
        d = 0
        for k in range(0,len(s)):
            if k == j:
                d = 1
            else:
                ret[k - d ] = s[k]
        return ''.join(ret)

if __name__ == '__main__':
    unittest.main()