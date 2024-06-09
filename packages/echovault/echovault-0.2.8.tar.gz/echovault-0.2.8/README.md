# echovault

`echovault` is data storage which store dictionary collection inexed by name.
The dictionary can be any pickleable key to any pickleable value.

Any operation done to the vault are translated to its git opertaion equivalent.

You can use all the git operation then to duplicate, branch, tag, prune, rollback ... be creative ...

```python
from echovault.vault import Vault
from dulwich.object_store import DiskObjectStore
from dulwich.refs import DiskRefsContainer
from sys import argv

object_store = DiskObjectStore(argv[-1] + '/objects/')
refs_containers = DiskRefsContainer(argv[-1] + '/')

vault = Vault(object_store, refs_containers)

vault.commit('main')

vault['test'] = ((('all', 'your'),
                  ('base', 4),
                  ('re', b'b'),
                  (3, 'longs')),
                 {'cui':1})

for entry in vault['test']:
    print(entry)
    if 3 in entry.keys():
        print(entry['all'])
        vault['test'].remove(entry)
vault['cuicui'] = ({'troll':None},)

vault.commit('main')

del vault['cuicui']

vault.commit('main')
```