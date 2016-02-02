class SublistAlias(object):
    def __init__(self, l, start=0, length=None):
        '''
        >>> x = [1, 2, 3, 4]
        >>> s1 = SublistAlias(x, 2, 2)
        >>> s2 = SublistAlias(x, 2)
        >>> s3 = SublistAlias(x)
        '''
        assert length is None or length >= 0
        self.l = l
        self.start = start
        self.length = length

    def __repr__(self):
        '''
        >>> x = [1, 2, 3, 4]
        >>> s = SublistAlias(x, 2, 2)
        >>> s
        SublistAlias([1, 2, 3, 4], 2, 2)
        '''
        return '%s(%r, %r, %r)' % (
            self.__class__.__name__, self.l, self.start, self.length)

    def __len__(self):
        '''
        >>> x = [1, 2, 3, 4]
        >>> s = SublistAlias(x, 1)
        >>> len(s)
        3
        '''
        if self.length is None:
            return len(self.l) - self.start
        else:
            return self.length

    def get(self):
        '''
        >>> x = [1, 2, 3, 4]
        >>> s = SublistAlias(x, 2, 2)
        >>> s.get()
        [3, 4]
        '''
        return self.l[self.start:self.start+len(self)]

    def set(self, vals):
        '''
        >>> x = [1, 2, 3, 4]
        >>> s = SublistAlias(x, 2, 2)
        >>> s.set([6, 7])
        >>> x
        [1, 2, 6, 7]
        '''
        self.l[self.start:self.start+len(self)] = vals

    def __getitem__(self, offset):
        '''
        >>> x = [1, 2, 3, 4]
        >>> s = SublistAlias(x, 2, 2)
        >>> s[0]
        3
        '''
        return self.l[self.start+offset]

    def __setitem__(self, offset, val):
        '''
        >>> x = [1, 2, 3, 4]
        >>> s = SublistAlias(x, 2, 2)
        >>> s[0] = 9
        >>> s.get()
        [9, 4]
        '''
        self.l[self.start+offset] = val

    def mergeitem(self, offset, val, nulls=(None,)):
        '''
        >>> x = [1, 2, 3, None]
        >>> s = SublistAlias(x, 2, 2)
        >>> s.mergeitem(1, 5)
        >>> s.get()
        [3, 5]
        >>> x
        [1, 2, 3, 5]
        >>> s.mergeitem(1, 9)
        Traceback (most recent call last):
        ...
        ValueError: Merge conflict: 9 into 5
        '''
        if self[offset] in nulls:
            self[offset] = val
        elif val in nulls:
            pass
        else:
            raise ValueError(
                "Merge conflict: %r into %r" % (val, self[offset]))


    def merge(self, vals, *args, **kwargs):
        '''
        >>> x = [1, 2, 3, 4]
        >>> s = SublistAlias(x, 2, 2)
        >>> s.set([None, 7])
        >>> s.merge([5, None])
        >>> s.get()
        [5, 7]
        >>> x
        [1, 2, 5, 7]
        >>> s.merge([5, None])
        Traceback (most recent call last):
        ...
        ValueError: Merge conflict: 5 into 5
        '''
        for offset in xrange(len(self)):
            self.mergeitem(offset, vals[offset], *args, **kwargs)

    def __getslice__(self, start, end):
        '''
        >>> x = [1, 2, 3, 4]
        >>> s = SublistAlias(x)
        >>> s.get()
        [1, 2, 3, 4]
        >>> s[2:3].get()
        [3]
        >>> s[1:4].get()
        [2, 3, 4]
        >>> s[1:].get()
        [2, 3, 4]
        >>> s[:3].get()
        [1, 2, 3]
        '''
        import sys
        if end == sys.maxsize:
            if self.length is None:
                length = None
            else:
                length = self.length - start
        else:
            length = end - start

        return self.__class__(self.l, self.start+start, length)

    def __setslice__(self, start, end, vals):
        '''
        >>> x = [1, 2, 3, 4]
        >>> s = SublistAlias(x)[2:]
        >>> s.set([6, 7])
        >>> x
        [1, 2, 6, 7]
        '''
        self[start:end].set(vals)

    def __iter__(self):
        '''
        >>> x = [1, 2, 3, 4]
        >>> s = SublistAlias(x, 2, 2)
        >>> list(s)
        [3, 4]
        '''
        return self.get().__iter__()

