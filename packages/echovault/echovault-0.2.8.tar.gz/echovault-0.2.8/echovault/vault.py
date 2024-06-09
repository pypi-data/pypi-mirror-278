from dulwich.objects import Tree, Commit
from dulwich.object_store import  PackBasedObjectStore
from dulwich.repo import BaseRepo
from dulwich.client import get_transport_and_path
from dulwich.protocol import ZERO_SHA
from echovault.list import List
from base64 import b64decode, b64encode
from socket import getfqdn, gethostname
from datetime import datetime
from os import getpid, getlogin, name as operating_system_name
from sys import argv
from typing import Optional
from time import time
from stat import S_IFDIR
from echovault._container import Container

try:
    from os import getuid, getgid
except:
    def getuid():
        return None

    def getgid():
        return None

ref_head = b'refs/heads/'

def walk_ancestor(object_store, commit):
    for identifier in commit.parents:
        yield identifier

    for identifier in commit.parents:
        yield from walk(object_store, object_store[identifier])
    
def last_common_ancestor(object_store,
                         refs,
                         branches):
    logs = {walk_ancestor(object_store, commit): {commit.id}
            for commit in (object_store[refs[branch]]
                           for branch in branches)}

    stopped = set()
    while (stopped != set(logs.keys())
           and not (common_ancestors := set.intersection(*(set(commits)
                                                           for commits
                                                           in logs.values())))):
        for walker, commits in logs.items():
            try:
                logs[walker] = commits | {next(walker)}
            except StopIteration:
                stopped |= {walker}

    common_ancestor, *_ = common_ancestors
    
    return common_ancestor

class Conflict(Exception):
    pass

class _Repo(BaseRepo):
    def get_named_file(self, path: str):
        return None

    def _del_named_file(self, path: str):
        ...
        
class Vault(Container):
    List = List
    
    @staticmethod
    def encode(string):
        return string.encode('utf-8')

    @staticmethod
    def decode(value):
        return value.decode('utf-8')
    
    def __init__(self, object_store, refs, *, tree:Tree=None, ref=None):
        super().__init__(object_store, None, None, tree)
        self.refs = refs
        if ref is not None:
            self.checkout(ref)
        else:
            self._ref = None

    @property
    def ref(self):
        return self._ref[len(ref_head):].decode('utf-8')
            
    def __getitem__(self, name:str):
        identifier = self.encode(name)
        _, oid = self.tree[identifier]
        tree = self.object_store[oid]
        return self.List(self.object_store,
                         self,
                         identifier,
                         tree=tree)

    def __setitem__(self, name:str, iterable):
        identifier = self.encode(name)
        self.tree[identifier] = S_IFDIR, None
        table = self.List(self.object_store, self, identifier, iterable)
        self._update()

    def __delitem__(self, name:str):
        del self.tree[self.encode(name)]
        self._update()

    def __iter__(self):
        return (self.decode(raw_key)
                for raw_key
                in iter(self.tree)
                if raw_key != b'_')

    def keys(self):
        yield from self.__iter__()

    def items(self):
        for name in iter(self):
            yield name, self[name]

    def values(self):
        for _, value in self.items():
            yield value

    def __repr__(self):
        return repr({key: value
                     for key, value
                     in self.items()})
            
    def rollback(self):
        if self._ref is None:
            self.tree = Tree()
        else:
            self.tree = self.object_store[self.object_store[self.refs[ref]].tree]

    def checkout(self, ref, branch=False):
        tree = self.tree
        
        ref = ref_head + ref.encode('utf-8')
        
        if ref in self.refs:
            tree = self.object_store[self.object_store[self.refs[ref]].tree]
        elif branch:
            self.refs[ref] = self.refs[self._ref]
        else:
            raise ValueError(f"No {ref} branch is existing !")
            
        self._ref = ref
        self.tree = tree

    def fetch(self, remote_uri, ref:Optional[str]=None):
        destination = _Repo(self.object_store, self.refs)
        # TODO: implement determine_wants function based on ref (or self._ref ?)
        client, source = get_transport_and_path(remote_uri)
        print('fetch:', client, source)
        def determine_wants(refs, depth=None):
            print('determine_wants:', refs)
            wanted_tips = list(refs.values())
            return wanted_tips

        # instead of changing local head branch,
        # we shall have update "remotes/{branch_name}"
        client.fetch(source, destination, determine_wants)

    def pull(self, remote_uri, ref:Optional[str]=None):
        self.fetch(remote_uri, ref)
        self.patch(self.diff(Vault(self.object_store, self.refs,
                                   ref=(ref.encode('utf-8')
                                        if ref is not None
                                        else self.ref))))
        
    def push(self, remote_uri, ref:Optional[str]=None):
        source = _Repo(self.object_store, self.refs)
        client, destination = get_transport_and_path(remote_uri)

        def update_refs(refs):
            # TODO: reduce dictionaire to ref (or self._ref ?)
            return {ref: (self.refs[ref]
                          if ref in self.refs
                          else ZERO_SHA)
                    for ref
                    in set(refs).union(set(self.refs.keys()))
                    if ref.startswith(b'refs/heads/')}

        client.send_pack(destination,
                         update_refs,
                         source.generate_pack_data)

    def commit(self,
               ref:Optional[str]=None,
               message:Optional[str]='',
               author:Optional[str]=None,
               committer:Optional[str]=None,
               time_:Optional[int]=None,
               timezone:Optional[int]=None,
               ):
        if ref is None:
            ref = self._ref
        else:
            ref = ref_head + ref.encode('utf-8')
            
        commit = Commit()
        
        commit.tree = self.tree

        if committer is None:
            committer = ('_'.join((getfqdn(), gethostname(),
                                   operating_system_name,
                                   repr(getgid()),
                                   repr(getuid()), repr(getpid())))
                         + f' <{getlogin()}@{getfqdn()}>')
            
        if author is None:
            author = f'{getlogin()} <{getlogin()}@{getfqdn()}>'

            
        commit.committer = committer.encode('utf-8')
        commit.author = author.encode('utf-8')

        if time_ is None:
            time_ = int(time())

        if timezone is None:
            timezone = 0

        commit.commit_time = time_
        commit.commit_timezone = timezone
        commit.author_time = time_
        commit.author_timezone = timezone

        if ref in self.refs:
            parents = (self.refs[ref],)
        elif self._ref is not None and self._ref in self.refs:
            parents = (self.refs[self._ref],)
        else:
            parents = ()
            
        commit.parents = parents
        
        commit.message = message.encode('utf-8')

        if not commit.id in self.object_store:
            self.object_store.add_object(commit)

        self.refs[ref] = commit.id

    def diff(self, other):
        if self.tree.id == other.tree.id:
            return

        sks = set(self.keys())
        oks = set(other.keys())

        removed = oks - sks
        if removed:
            yield ('-', removed)
        
        added = sks - oks
        if added:
            yield ('+',
                   dict((key,
                        tuple(dict(element.items())
                              for element in self[key]))
                        for key in added))

        for name in sks.intersection(oks):
            for difference in self[name].diff(other[name]):
                yield ('!=', name, *difference)

    def patch(self, differences):
        for difference in differences:
            match difference:
                case ('-', removed):
                    for key in removed:
                        del self[key]
                case ('+', added):
                    for key, entries in added.items():
                        self[key] = entries
                case ('!=', name, *difference):
                    self[name].patch((difference,))

    def merge(self, others, *, without_conflict=True):
        ancestor = last_common_ancestor(self.object_store,
                                        self.refs,
                                        (vault._ref for vault in (self, *others)))

        base_vault = Vault(self.object_store, self.refs,
                           tree=self.object_store[self.object_store[ancestor].tree])

        for child in others:
            self.patch(child.diff(base_vault))
