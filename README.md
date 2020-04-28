# Python Formal Languages Library (PyForm)

This repository contains implementations of various algorithms from formal language theory. It aims to provide a simple platform for expressing and manipulating finite automata, formal grammars and regular expressions.

## Examples

Find minimal partial automaton equivalent to given automaton, construct isomorphism between minimized automaton and expected result, and check the automata for language equivalence.

```
from pyform.automaton.dfa import DFA

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

minimized = dfa.minimize_valmari()
minimized.isomorphic(expected)
minimized.equivalent_hopcroft_karp(dfa)
```

## References

* Valmari, Antti. 2012. Fast brief practical DFA minimization. Information Processing Letters. 112(6): 213-217.

* Bonchi, Filippo & Pous, Damien. 2013. Checking NFA Equivalence with Bisimulations up to Congruence. Conference Record of the Annual ACM Symbposium on Principles of Programming Languages. 457-68.

* Hopcroft, John, Motwani, Rajeev & Ullman, Jeffrey. 2013. Introduction to Automata Theory, Languages and Computation (3rd ed.). Pearson.

## License

This project is licensed under the MIT license.




