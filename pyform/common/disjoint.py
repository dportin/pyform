class DisjointSet(object):

    """Disjoint-set data structure.

    Disjoint-set data structure supporting make_set, union and find. Uses path
    compression and union-by-rank algorithms to achieve optimal amortized time
    bounds. Elements are arbitrary hashable objects.

    Attributes:
        rank      : Dictionary mapping elements to ranks.
        parent    : Dictionary mapping elements to parents.
        num_elems : Number of elements in partition.
        num_equiv : Number of equivalence classes in partition.
    """
    
    def __init__(self, elements=None):

        self.rank      = {}
        self.parent    = {}

        self.num_elems = 0
        self.num_equiv = 0

        if elements is not None:
            for i in elements:
                self.make_set(i)

    def make_set(self, i):

        """Create singleton set containing i. If i belongs to some equivalence
        class, does not modify the partition.

        Args :
            i : Hashable object.
        """

        if i in self.parent:
            return

        self.rank[i]   = 0
        self.parent[i] = i

        self.num_elems += 1
        self.num_equiv += 1

    def find(self, i):

        """Return representative of equivalence class to which i belongs. If i
        does not belong to any equivalence class, calls make_set. Implemented
        using iterative path compression algorithm.

        Args:
            i : Hashable object.

        Returns:
            Representative of equivalence class to which i belongs.
        """

        if i not in self.parent:
            self.make_set(i)
            
        root = i
        while self.parent[root] != root:
            root = self.parent[root]

        while self.parent[i] != root:
            parent = self.parent[i]
            self.parent[i] = root
            i = parent

        return root

    def union(self, i, j):

        """Merge equivalence classes to which i and j belong. If either i or j
        are not members of any equivalence class, calls make_set. Implemented
        using the union-by-rank algorithm.

        Args:
            i : Hashable object.
            j : Hashable object.

        Returns:
            Representative of merged equivalence class (the representative of
            the equivalence class to which i belongs if rank[i] < rank[j] and
            the representative of the class to which j belongs otherwise).
        """

        iroot = self.find(i)
        jroot = self.find(j)

        if iroot == jroot:
            return iroot

        if self.rank[iroot] < self.rank[jroot]:
            iroot, jroot = jroot, iroot

        self.parent[jroot] = iroot
        self.num_equiv -= 1
        
        if self.rank[iroot] == self.rank[jroot]:
            self.rank[iroot] += 1

        return iroot

    def partition(self):

        """Return dictionary mapping representatives of equivalence classes to
        equivalence classes. This method calls find on each element of the
        partition and therefore compresses every path.

        Returns:
            Dictionary mapping representatives of equivalence classes to
            equivalence classes.
        """

        partition = {}
        for element in self.parent:
            equiv = self.find(element)
            if equiv not in partition:
                partition[equiv] = set()
            partition[equiv].add(element)

        return partition
