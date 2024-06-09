from dulwich.objects import Tree, Blob
from stat import S_IFREG, S_IFDIR
from uuid import uuid4
from echovault._container import Container
from echovault.dict import Dict

class List(Container):
    Dict = Dict
    
    def __init__(self, object_store, container, identifier, values=(), *, tree=None):
        super().__init__(object_store, container, identifier, tree)
        self.extend(values)

    def __getitem__(self, key):
        _, id_ = self.tree[key]
        return self.Dict(self.object_store,
                         self,
                         key,
                         tree=self.object_store[id_])

        
    def __iter__(self):
        for key in self.tree:
            if key == b'_':
                continue
            
            yield self[key]

    def __repr__(self):
        return repr(list(iter(self)))
            
    def append(self, value):
        self.extend((value,))
            
    def extend(self, iterable):
        for item in iterable:
            identifier = str(uuid4()).encode('utf-8')
            self.tree[identifier] = S_IFDIR, None
            entry = self.Dict(self.object_store,
                              self,
                              identifier,
                              item)

        self._update()
            
    def remove(self, entry):
        del self.tree[entry.identifier]
        
        self._update()

    def diff(self, other):
        if self.tree.id == other.tree.id:
            return

        sks = set(self.tree) - {b'_'}
        oks = set(other.tree) - {b'_'}

        removed = oks - sks
        if removed:
            yield ('-', removed)

        added = sks - oks
        if added:
            yield ('+',
                   tuple(dict(self[key].items())
                         for key in added))
            
        for key in sks.intersection(oks):
            for difference in self[key].diff(other[key]):
                yield ('!=', key, *difference)

    def patch(self, differences):
        for difference in differences:
            match difference:
                case ('-', removed):
                    for key in removed:
                        self.remove(self[key])
                case ('+', added):
                    self.extend(added)
                case ('!=', key, *difference):
                    self[key].patch((difference,))
