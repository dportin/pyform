class Partition(object):

    """Partition refinement data structure.

    Partition refinement data structure for implementation of Valmari's
    algorithm (DFA.minimizme_valmari). This class is tightly coupled with the
    DFA and ValmariState classes; each depends on specific implementation
    details of the other.

    Elements of the partition are stored in the array elements. Elements that
    belong to the same equivalence class are contiguous. The location array
    stores the location of element e in elements. The equivalence class that
    element e belongs to is stored in the array setof. If setof[e] == i then
    the elements of equivalence class i are elements[first[i]:past[i]]. The
    attribute size records the number of equivalence classes.

    This class is initialized with a count and partition function f. Elements
    of the partition are integers in range(count). If f == None the partition
    is initialized with a single equivalence class. Otherwise, f is a function
    of elements and the initial partitions are determined by f. For example,
    the function lambda e: e % 2 == 0 partitions the elements by their parity.

    Attributes:
        size        : Number of equivalence classes in partition.
        elements    : Array of elements in partition.
        location    : Location of element e in elements.
        setof       : Equivalence class that element i belongs to.
        first       : Start index of equivalence class i in elements.
        past        : Start index of next equivalence class i in elements.
        marked      : Number of marked elements in equivalence class i.
        touched     : Equivalence classese with marked elements.
        num_touched : Number of equivalence classes with marked elements.
    """
    
    def __init__(self, count, key=None):

        self.elements    = list(range(count))
        self.location    = list(range(count))
        self.first       = [0] * count
        self.past        = [0] * count
        self.setof       = [0] * count        
        self.marked      = [0] * count + [0]
        self.touched     = [0] * count + [0]
        self.num_touched = 0

        # return singleton partition if count == 0 or key == None

        if not (count and key):
            self.size  = int(bool(count))
            if self.size:
                self.past[0] = count
            return

        # otherwise partition elements by key
        
        self.size = 0
        self.elements.sort(key=key)

        partition = key(self.elements[0])
        for i in range(count):
            element = self.elements[i]
            current = key(element)
            if partition != current:
                partition = current
                self.past[self.size]  = i
                self.size += 1
                self.first[self.size] = i
            self.setof[element]    = self.size
            self.location[element] = i

        self.past[self.size] = count
        self.size += 1

    def mark(self, element):

        """Mark element for splitting in partition.

        Args:
            element : Integer representing element in partition.
        """

        equiv    = self.setof[element]
        index    = self.location[element]
        unmarked = self.first[equiv] + self.marked[equiv]

        # return if element already marked

        if index < unmarked:
            return

        # swap location of element and first unmarked element
        
        self.elements[index]                = self.elements[unmarked]
        self.location[self.elements[index]] = index
        self.elements[unmarked]             = element
        self.location[element]              = unmarked

        # update marked count and touched states
        
        if not self.marked[equiv]:
            self.touched[self.num_touched] = equiv
            self.num_touched += 1
        self.marked[equiv] += 1

    def split(self):

        """Split equivalence classes containing marked elements. The unmarked
        elements are assigned the new class if the number of unmarked elements
        is smaller than the number of marked elements, and the marked elements
        otherwise. This ensure that split only iterates over the smaller half
        of each touched class.

        Returns:
            The number of new equivalence classes.
        """

        while self.num_touched:

            self.num_touched -= 1

            equiv    = self.touched[self.num_touched]
            unmarked = self.first[equiv] + self.marked[equiv]

            # continue if every element is marked
            
            if unmarked == self.past[equiv]:
                self.marked[equiv] = 0
                continue

            # otherwise assign smaller half new class
            
            if self.marked[equiv] <= self.past[equiv] - unmarked:
                self.first[self.size] = self.first[equiv]
                self.past[self.size]  = unmarked
                self.first[equiv]     = unmarked
            else:
                self.past[self.size]  = self.past[equiv]
                self.first[self.size] = unmarked
                self.past[equiv]      = unmarked

            for i in range(self.first[self.size], self.past[self.size]):
                self.setof[self.elements[i]] = self.size

            self.marked[equiv] = 0
            self.marked[self.size] = 0
            self.size += 1

    def partition(self, equiv):

        return self.elements[self.first[equiv]:self.past[equiv]]

    def partitions(self):

        return (self.partition(i) for i in range(self.size))


