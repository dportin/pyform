class ValmariState(object):

    """Stores adjacent transitions and miscellaneous data for implementation
    of Valmari's algorithm (DFA.minimizme_valmari). This class is tightly
    coupled with the DFA and Partition classes; each depends on specific
    implementation details of the other.

    Let M be a DFA. There is a transition from state q to state r on symbol a
    in M iff there is an index i such that heads[i] = q, tails [i] = r and
    labels[i] = a. The indices of the transitions adjacent to state i are
    stored in adjacent[offset[i]:offset[i + 1]] for some ordering of states in
    M. This data structure can be sorted by tail or head states, permitting
    efficient access to incoming and outgoing transitions (make_adjacent).

    The remaining attributes and methods are stored here because they require
    access to the adjacent transitions data structure. The state, transition,
    final state and reached counts are updated from DFA.minimize_valmari.

    Attributes:
        adjacent    : Array of adjacent transitions.
        offset      : Array of offsets into transitions.
        tails       : Array of transition tails.
        heads       : Array of transition heads.
        labels      : Array of transition labels.
        num_states  : Number of states in the DFA.
        num_trans   : Number of transitions in the DFA.
        num_finals  : Number of final states in the DFA.
        num_reached : Number of reached states.
    """

    def __init__(self, dfa):

        self.num_states  = len(dfa.states)
        self.num_trans   = len(list(dfa.iterate()))
        self.num_finals  = len(dfa.finals)
        self.num_reached = 0

        # adjacent transitions data structure

        self.adjacent = [0] * self.num_trans
        self.offset   = [0] * self.num_states + [0]

        # transition function data structure

        self.tails, self.labels, self.heads = (
            map(list, zip(*dfa.iterate()))
            if dfa.delta
            else ([], [], [])
        )

    def make_adjacent(self, forwards=True):

        """Initialize adjacent transitions and sort with respect to their
        tails or heads. This method employs counting sort to achieve linear
        time complexity.

        Args:
            forwards : Boolean indicating whether transitions are sorted
                according to their tails (True) or heads (False).
        """
        
        trans = self.tails if forwards else self.heads
        
        for i in range(self.num_states + 1):
            self.offset[i] = 0

        for i in range(self.num_trans):
            self.offset[trans[i]] += 1

        for i in range(self.num_states):
            self.offset[i + 1] += self.offset[i]

        for i in range(self.num_trans - 1, -1, -1):
            self.offset[trans[i]] -= 1
            self.adjacent[self.offset[trans[i]]] = i

    def reach(self, blocks, state):

        """Mark state as reachable in blocks partition. The behavior of blocks
        and this method is considered undefined if blocks contains more than
        one partition or any marked states.

        Args:
            blocks : Partition instance.
            state  : Integer in blocks.
        """

        index = blocks.location[state]

        # assumes reached states have indices lower than num_reached
        
        if index < self.num_reached:
            return

        # swap location of state and element at num_reached in blocks
        
        unreached                         = blocks.elements[self.num_reached]
        blocks.elements[index]            = unreached
        blocks.location[unreached]        = index
        blocks.elements[self.num_reached] = state
        blocks.location[state]            = self.num_reached

        self.num_reached += 1
        
    def remove_unreachable(self, blocks, forwards=True):

        """Remove transitions unreachable from previously reached states in
        blocks partition. The behavior of blocks and this method is considered
        undefined if blocks contains more than one partition or any marked
        states. The forwards argument determines whether the transition graph
        is traversed forwards or backwards. 

        This method updates num_trans but does not change num_states, because
        blocks is initialized with the original state numbers but the cords
        partition has not been initialized when remove_unreachable is called.

        Args:
            blocks   : Partition instance.
            forwards : Boolean indicating whether the transition graph is
                traversed forwards (True) or backwards (False).
        """

        tails, heads = (self.tails, self.heads) if forwards else \
                       (self.heads, self.tails)
        
        self.make_adjacent(forwards)

        # traverse transition graph using breadth-first search
        
        tail = 0
        while tail < self.num_reached:
            for head in range(self.offset[blocks.elements[tail]],
                              self.offset[blocks.elements[tail] + 1]):
                self.reach(blocks, heads[self.adjacent[head]])
            tail += 1

        # remove unreached states from adjacent transitions

        num_trans = 0
        for i in range(self.num_trans):
            if blocks.location[tails[i]] < self.num_reached:
                heads[num_trans]       = heads[i]
                tails[num_trans]       = tails[i]
                self.labels[num_trans] = self.labels[i]
                num_trans += 1

        self.num_trans   = num_trans
        blocks.past[0]   = self.num_reached
        self.num_reached = 0

    def iterate_offset(self, state):

        return range(self.offset[state], self.offset[state + 1])

    def iterate_adjacent(self, state):

        return map(self.adjacent.__getitem__, self.iterate_offset(state))


        
