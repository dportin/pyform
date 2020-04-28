from pyform.automaton.dfa import DFA
from unittest import TestCase

class TestIsomorphic(TestCase):

    pass

class TestEquivalentHopcroftKarp(TestCase):

    pass

class TestProduct(TestCase):

    pass

class TestMinimizeValmari(TestCase):

    def test_minimize_valmari_1(self):
        
        dfa = DFA(
            states = set([0,1,2,3,4,5,6,7]),
            finals = set([1,2,3,4,5,6]),
            start  = 0,
            sigma  = set(['a','b']),
            delta  = {
                0 : {'a' : 1, 'b' : 4},
                1 : {'a' : 2, 'b' : 3},
                2 : {'a' : 7, 'b' : 7},
                3 : {'a' : 7, 'b' : 3},
                4 : {'a' : 5, 'b' : 6},
                5 : {'a' : 7, 'b' : 7},
                6 : {'a' : 7, 'b' : 6},
                7 : {'a' : 7, 'b' : 7}
            }
        )

        expected = DFA(
            states = set([0,1,2,3]),
            finals = set([1,2,3]),
            start  = 0,
            sigma  = set(['a','b']),
            delta = {
                0 : {'a' : 1, 'b' : 1},
                1 : {'a' : 2, 'b' : 3},
                3 : {'b' : 3},
            }
        )
        
        dfa_min = dfa.minimize_valmari()
        self.assertIsNotNone(dfa_min.isomorphic(expected))
        self.assertTrue(dfa_min.equivalent_hopcroft_karp(dfa)[0])

    def test_minimize_valmari_2(self):

        dfa = DFA(
            states = set([0,1,2,3,4,5,6]),
            finals = set([4,5,6]),
            start  = 0,
            sigma  = set(['a','b']),
            delta  = {
                0 : {'a' : 4, 'b' : 1},
                1 : {'a' : 5, 'b' : 2},
                2 : {'a' : 6, 'b' : 3},
                3 : {'a' : 3, 'b' : 3},
                4 : {'a' : 4, 'b' : 4},
                5 : {'a' : 5, 'b' : 5},
                6 : {'a' : 6, 'b' : 6}
            }
        )

        expected = DFA(
            states = set([0,1,2,3]),
            finals = set([3]),
            start  = 0,
            sigma  = set(['a','b']),
            delta  = {
                0 : {'a' : 3, 'b' : 1},
                1 : {'a' : 3, 'b' : 2},
                2 : {'a' : 3},
                3 : {'a' : 3, 'b' : 3}
            }
        )

        dfa_min = dfa.minimize_valmari()
        self.assertIsNotNone(dfa_min.isomorphic(expected))
        self.assertTrue(dfa_min.equivalent_hopcroft_karp(dfa)[0])

    def test_minimize_valmari_3(self):

        dfa = DFA(
            states = set([0,1,2,3,4,5]),
            finals = set([5]),
            start  = 0,
            sigma  = set(['a','b']),
            delta  = {
                0 : {'a' : 1, 'b' : 3},
                1 : {'a' : 1, 'b' : 2},
                2 : {'a' : 2, 'b' : 5},
                3 : {'a' : 3, 'b' : 4},
                4 : {'a' : 4, 'b' : 5},
                5 : {'a' : 5, 'b' : 5}
            }
        )

        expected = DFA(
            states = set([0,1,2,3]),
            finals = set([3]),
            start  = 0,
            sigma  = set(['a','b']),
            delta  = {
                0 : {'a' : 1, 'b' : 1},
                1 : {'a' : 1, 'b' : 2},
                2 : {'a' : 2, 'b' : 3},
                3 : {'a' : 3, 'b' : 3}
            }
        )

        dfa_min = dfa.minimize_valmari()
        self.assertIsNotNone(dfa_min.isomorphic(expected))
        self.assertTrue(dfa_min.equivalent_hopcroft_karp(dfa)[0])

    def test_minimize_valmari_4(self):

        dfa = DFA(
            states = set([0,1,2,3,4,5]),
            finals = set([0,2,4]),
            start  = 0,
            sigma  = set(['a','b']),
            delta  = {
                0 : {'a' : 1, 'b' : 3},
                1 : {'a' : 2, 'b' : 3},
                2 : {'a' : 5, 'b' : 2},
                3 : {'a' : 4, 'b' : 1},
                4 : {'a' : 5, 'b' : 4},
                5 : {'a' : 5, 'b' : 5}
            }
        )

        expected = DFA(
            states = set([0,1,2]),
            finals = set([0,2]),
            start  = 0,
            sigma  = set(['a','b']),
            delta  = {
                0 : {'a' : 1, 'b' : 1},
                1 : {'a' : 2, 'b' : 1},
                2 : {'b' : 2},
            }
        )

        dfa_min = dfa.minimize_valmari()
        self.assertIsNotNone(dfa_min.isomorphic(expected))
        self.assertTrue(dfa_min.equivalent_hopcroft_karp(dfa)[0])

    def test_minimize_valmari_5(self):

        dfa = DFA(
            states = set([0,1,2,3,4,5,6]),
            finals = set([1,3,5,6]),
            start  = 0,
            sigma  = set(['a','b']),
            delta  = {
                0 : {'a' : 1, 'b' : 3},
                1 : {'a' : 2, 'b' : 4},
                2 : {'a' : 5, 'b' : 5},
                3 : {'a' : 4, 'b' : 2},
                4 : {'a' : 5, 'b' : 5},
                5 : {'a' : 6, 'b' : 5},
                6 : {'a' : 6, 'b' : 6}
            }
        )

        expected = DFA(
            states = set([0,1,2,3]),
            finals = set([1,3]),
            start  = 0,
            sigma  = set(['a','b']),
            delta  = {
                0 : {'a' : 1, 'b' : 1},
                1 : {'a' : 2, 'b' : 2},
                2 : {'a' : 3, 'b' : 3},
                3 : {'a' : 3, 'b' : 3}
            }
        )

        dfa_min = dfa.minimize_valmari()
        self.assertIsNotNone(dfa_min.isomorphic(expected))
        self.assertTrue(dfa_min.equivalent_hopcroft_karp(dfa)[0])

if __name__ == '__main__':
    
    unittest.main()
