from bidict import bidict
from collections import deque
from pyform.automaton.fa import FA
from pyform.common.disjoint import DisjointSet
from pyform.common.partition import Partition
from pyform.automaton.valmari import ValmariState

class DFA(FA):

    """Deterministic finite automaton with partial transition function.

    Implementation of deterministic finite automata with partial transition
    functions. States are represented as integers. Symbols must be hashable
    objects. The alphabet may be empty but there must be at least one state
    (the start state). No method of this class modifies any data structure
    passed to init.

    The transition function may be partial and is represented using nested
    dictionaries. There is a transition from state q to state r on symbol a
    whenever delta[q][a] = r. If delta[q] is undefined then state q has no
    outgoing edges. If delta[q] is defined and delta[q][a] is undefined then
    state q has no outgoing edge with label a.
    
    Attributes:
        states : Set of integers.
        finals : Set of integers (subset of states).
        start  : Integer (member of states)
        sigma  : Set of hashable objects.
        delta  : Partial transition function represented as nested dictionary
            data structure (delta[q][a] == r iff there is a transition from
            state q to state r on symbol a and undefined otherwise).
    """
    
    def __init__(self, states, finals, sigma, start, delta):

        self.states = states
        self.finals = finals
        self.start  = start
        self.sigma  = sigma
        self.delta  = delta

    def validate(self):

        raise NotImplementedError

    def iterate(self):

        """Generator yielding transitions as triples (delta[q][a] == r iff
        (q, a, r) is yielded by the generator).

        Returns:
            Generator yielding transitions as triples.
        """

        return (
            (q, a, r)
            for q, m in self.delta.items()
            for a, r in m.items()
        )

    def transition(self, states, symbols):

        """The set of states obtained by transitioning from some state in
        states on symbols in symbols. This method does not assume the validity
        of statest and symbols passed as arguments.

        Args:
            states  : Iterable of states.
            symbols : Iterable of symbols.

        Returns:
            The set of states obtained by transitioning from some state in
            states on symbols in symbols.
        """

        return set(
            self.delta[q][a]
            for (q, a) in zip(states, symbols)
            if q in self.delta and a in self.deltq[a]
        )

    def reachable(self, states, symbols):

        """The set of states reachable from some state in states via repeated
        transitions on symbols in symbols. This method does not assume the
        validity of states and symbols passed as arguments.

        Args:
            states  : Iterable of states.
            symbols : Iterable of symbols.

        Returns:
            The set of states reachable from some state in states via repeated
            transitions on symbols in symbols. 
        """

        reached  = set()
        worklist = list(states)

        while worklist:
            state = worklist.pop()
            if state not in reached:
                targets = self.transition([state], symbols)
                reached.add(state)
                worklist.extend(targets - reached)

        return reached

    def productive(self, states, symbols):

        """The set of states that can reach some state in states via repeated
        transitions on symbols in symbols. This method does not assume the
        validity of states and symbols passed as arguments. This method uses
        additional space proportional to the number of transitions.

        Args:
            states  : Iterable of states.
            symbols : Iterable of symbols.

        Returns:
            The set of states that can reach some state in states via repeated
            transitions on symbols in symbols.
        """

        inverse  = {}
        reached  = set()
        worklist = list(states)

        for (q, a, r) in self.iterate():
            if r not in inverse:
                inverse[r] = {}
            inverse[r][a] = q

        while worklist:
            state = worklist.pop()
            if state not in reached:
                targets = set(
                    inverse[state][a]
                    for a in symbols
                    if state in inverse and a in inverse[state]
                )
                reached.add(state)
                worklist.extend(targets - reached)

        return reached

    def complete(self):

        return NotImplementedError

    def minimize_valmari(self):

        """Construct equivalent (up to isomorphism) minimal partial DFA using
        Valmari's algorithm [1]. This algorithm runs in O(N + M log M) time
        where N is the number of states and M the number of transitions and
        consumes O(N + M) additional space.

        In contrast with [1] this algorithm does not share memory for marked
        and touched states between the blocks and cords partitions. Because
        of the way transition functions are represented, the transition data
        structure used in the algorithm requires O(M) addtional space.

        [1] Valmari, Antti. 2012. Fast brief practical DFA minimization. Inf-
        ormation Processing Letters. 112(6): 213-217.
        """

        # initialize blocks partition and transition data structure

        vstate = ValmariState(self)
        blocks = Partition(vstate.num_states, key=None)

        # remove unreachable states from adjacent transitions

        vstate.reach(blocks, self.start)
        vstate.remove_unreachable(blocks, forwards=True)

        # remove unproductive states from adjacent transitions

        for state in self.finals:
            if blocks.location[state] < blocks.past[0]:
                vstate.reach(blocks, state)

        vstate.num_finals = vstate.num_reached
        vstate.remove_unreachable(blocks, forwards=False)

        # partition states into final and nonfinal states if the number of
        # useful final states is nonzero.
        
        blocks.marked[0] = vstate.num_finals
        if vstate.num_finals:
            blocks.touched[blocks.num_touched] = 0
            blocks.num_touched += 1
            blocks.split()

        # initialize cords partition and partition by transition labels

        cords = Partition(vstate.num_trans, key=vstate.labels.__getitem__)

        # refine blocks and cords until all blocks and cords are compatible

        block = 1
        cord  = 0

        vstate.make_adjacent(forwards=False)

        while cord < cords.size:
            for i in range(cords.first[cord], cords.past[cord]):
                blocks.mark(vstate.tails[cords.elements[i]])
            blocks.split()
            cord += 1
            while block < blocks.size:
                for i in range(blocks.first[block], blocks.past[block]):
                    for j in range(vstate.offset[blocks.elements[i]],
                                   vstate.offset[blocks.elements[i] + 1]):
                        cords.mark(vstate.adjacent[j])
                cords.split()
                block += 1

        # construct minimized partial dfa (note that the alphabet of the
        # minimized dfa may be a proper subset of the original alphabet)

        delta  = {}
        sigma  = set()

        for i in range(vstate.num_trans):
            source = blocks.setof[vstate.tails[i]]
            if blocks.location[vstate.tails[i]] == blocks.first[source]:
                label = vstate.labels[i]
                if source not in delta:
                    delta[source] = {}
                delta[source][label] = blocks.setof[vstate.heads[i]]
                sigma.add(label)

        return DFA(
            states = set(range(blocks.size)),
            finals = set(i for i in range(blocks.size)
                         if blocks.first[i] < vstate.num_finals),
            start  = blocks.setof[self.start],
            sigma  = sigma,
            delta  = delta
        )

    def equivalent_hopcroft_karp(self, dfa):

        """Determine whether the current and argument automata are equivalent
        using Hopcroft and Karp's algorithm [1]. Returns a shortest witness
        accepted by precisely one automaton if they are not equivalent. This
        implementation uses a disjoint set data structure to achieve almost
        linear time complexity.

        This method does not assume that the automata are complete or have
        disjoint state sets. Instead, it standardizes the state sets apart and
        employs virtual dummy states.

        [1] Bonchi, Filippo & Pous, Damien. 2013. Checking NFA Equivalence with
        Bisimulations up to Congruence. Conference Record of the Annual ACM
        Symbposium on Principles of Programming Languages. 457-68.
        
        Args:
            dfa : DFA instance.

        Returns:
            (b, w) where b is a boolean indicating whether the automata are
            equivalent and w is either None or a shortest witness if they are
            not equivalent.
        """
        
        dummy1  = 1 + max(self.states)
        dummy2  = 1 + max(dfa.states)
        offset  = 1 + dummy1

        equiv   = DisjointSet()
        queue   = deque([([], self.start, dfa.start)])

        while queue:
            witness, q1, r1 = queue.popleft()
            if equiv.find(q1) == equiv.find(r1 + offset):
                continue
            if (q1 in self.finals) ^ (r1 in dfa.finals):
                return (False, witness)
            for symbol in self.sigma:
                q2 = self.delta[q1].get(symbol, dummy1) \
                     if q1 in self.delta else dummy1
                r2 = dfa.delta[r1].get(symbol, dummy2) \
                     if r1 in dfa.delta else dummy2
                queue.append((witness + [symbol], q2, r2))
            equiv.union(q1, r1 + offset)

        return (True, None)

    def product(self, dfa, f):

        """Generalized product of current and argument automata with respect
        to boolean function f. The states of the resulting automata represent
        tuples (q1, r1) where q1 in self.states and r1 in dfa.states. State
        (q1, r1) is final if f(q1 in self.finals, r1 in dfa.finals) is true.

        If the current or argument automata are partial or have different
        alphabets, this method inserts a sink state (and derived products)
        into the resulting automaton.        

        Args:
            dfa : DFA instance.
            f   : Boolean function of two variables.

        Returns:
            Generalized product of current and argument automata with respect
            to boolean function f.
        """

        delta    = {}
        states   = {(self.start, dfa.start) : 0}
        sigma    = self.sigma.union(dfa.sigma)
        
        index    = 1
        worklist = [(self.start, dfa.start)]

        while worklist:
            q1, r1 = worklist.pop()
            for symbol in sigma:
                q2 = self.delta[q1].get(symbol) if q1 in self.delta else None
                r2 = dfa.delta[r1].get(symbol) if r1 in dfa.delta else None

                if (q2, r2) not in states:
                    states[(q2, r2)] = index
                    index += 1
                    worklist.add((q2, r2))

                source = states[(q1, r1)]
                target = states[(q2, r2)]
                if source not in delta:
                    delta[source] = {}
                delta[source][symbol] = target

        return DFA(
            states = set(states.values()),
            finals = set(
                states[(q1, r1)]
                for (q1, r1) in states
                if f(q1 in self.finals, r1 in dfa.finals)
            ),
            start  = 0,
            sigma  = sigma,
            delta  = delta
        )
    
    def isomorphic(self, dfa):

        """Let M and N be the subautomata induced by discarding any states
        unreachable from the start states of the current and argument DFAs,
        respectively. Determine whether M and N are isomorphic and construct
        the isomorphism if so.

        Args:
            dfa : DFA instance.

        Returns:
            bidict witnessing the isomorphism between M and N if M and N are
            isomorphic and None otherwise.
        """

        worklist    = [(self.start, dfa.start)]
        isomorphism = bidict(worklist)

        while worklist:
            q1, r1 = worklist.pop()

            if (q1 in self.finals) ^ (r1 in dfa.finals):
                return None
            
            if q1 not in self.delta and r1 not in dfa.delta:
                continue

            # q1 and r1 are not isomorphic if they are not jointly final or
            # nonfinal, have different numbers of outgoing transitions, or
            # those transitions have different labels.

            if (q1 in self.delta) ^ (r1 in dfa.delta) or \
               self.delta[q1].keys() ^ dfa.delta[r1].keys():
                return None

            for symbol, q2 in self.delta[q1].items():
                r2 = dfa.delta[r1][symbol]
                if q2 in isomorphism:
                    if r2 != isomorphism[q2]:
                        return None
                    continue
                if r2 in isomorphism.inverse:
                    if q2 != isomorphism.inverse[r2]:
                        return None
                    continue
                isomorphism[q2] = r2
                worklist.append((q2, r2))

        return isomorphism

    
