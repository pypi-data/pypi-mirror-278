from stat import S_IFREG, S_IFDIR
from dulwich.objects import Tree, Blob

class Container:
    def __init__(self, object_store, container, identifier, tree):
        self.object_store = object_store
        self.identifier = identifier
        
        if tree is None:
            tree = Tree()

        self.tree = tree
        self.container = container

        if not b'_' in self.tree:
            blob = Blob()
            
            if not blob.id in self.object_store:
                self.object_store.add_object(blob)
            
            self.tree[b'_'] = S_IFREG | 0o755, blob.id

        self._update()

    
    def _update(self):
        if not self.tree.id in self.object_store:
            self.object_store.add_object(self.tree)

        if self.container is None:
            return

        _, id_ = self.container.tree[self.identifier]
        
        if id_ != self.tree.id:
            self.container.tree[self.identifier] = S_IFDIR, self.tree.id
            
            self.container._update()
