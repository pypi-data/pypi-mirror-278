# pylint:
#
"""
Status Tree definitions

This is a structure of one or more groups, systems and services, and then
tests for each of these along with the current status, organized in a tree.
Leaf nodes are always individual tests and status, children of nodes
representing systems and services.  These in turn are children either of the
root node, or an additional level or levels of groupings.

Two potential examples:

With groups:             Simple structure:

root                     root
- servers                - serverA
  - serverA                - DNS
    - DNS                  - web
    - web                  - disk usage
    - disk usage         - serverB
  - serverB                - web
    - web                  - mail
    - mail                 - disk usage
    - disk usage         - laptop
- workstations             - backups
  - laptop                 - disk usage
    - backups
    - disk usage

Groups:
    - name
    - overall state (derived)
    - add_node()

Nodes:
    - name
    - overall state (derived)
    - registered
    - add_status()

Status:
    - name
    - state
    - message
    - reported
    - stale
    - acknowledgement

"""
from enum import IntEnum

# For now, use lowercase as that's what the API uses
# pylint: disable=invalid-name
class State(IntEnum):
    """
    Test states.  Integer values are the corresponding exit status of check
    scripts.
    """
    okay = 0
    unknown = 1
    warning = 2
    error = 3
    unusable = 4

# pylint: disable=too-few-public-methods
class Base:
    """ Base class for status tree """
    def __init__(self, name):
        self._name = name

    def __str__(self):
        """ Return common string representation. """
        return self._name

    def iterate(self, depth=0, lineage=None):
        """
        Create generator for iterating children.

        Args:
            depth: tree depth of descent
            lineage: tuple or list of parent's name, grandparent's, ...

        Yields:
            path: node path (list of node name, parent, grandparent, ...)
            depth: node depth in tree
            state: node state
            self
        """
        yield((
            (lineage if lineage is not None else []) + [self._name],
            depth,
            self.state.name,
            self
        ))

    @property
    def state(self):
        """ Return node state (not applicable here). """
        return None

class Tree(Base):
    """
    A status tree represents a hierarchy of groups, optionally, and nodes and
    their statuses.  The root and optionally further levels represent groups
    of nodes, followed by a level of system/service nodes and finally a level
    of tests.
    """
    @staticmethod
    def worse(status1, status2):
        """ Returns worse (higher error level) status of the two given. """
        if status1 > status2:
            return status1
        return status2

    def __init__(self, name):
        super().__init__(name)
        self._children = {}
        self._state = None
        self._totals = None
        self._acknowledged = None

    def add(self, name, tree):
        """ Add subtree """
        self._children[name] = tree

    def __getitem__(self, key):
        return self._children[key]

    def __setitem__(self, key, value):
        self._children[key] = value

    def __delitem__(self, key):
        del self._children[key]

    def add_tree(self, name):
        """ Add and return subtree """
        tree = Tree(name)
        self._children[name] = tree
        return tree

    def add_node(self, name, registration):
        """ Add and return node """
        node = Node(name, registration)
        self._children[name] = node
        return node

    @property
    def state(self):
        """
        Get state of node or aggregate state of subtree (worst state of
        all children).
        """
        if self._state is None:
            self._state = State.okay
            # status is worst of children's statuses
            for child in self._children.values():
                self._state = Tree.worse(self._state, child.state)
        return self._state

    @property
    def acknowledged(self):
        """
        A node is considered acknowledged if it has any non-Okay status
        children, and each of those children with non-Okay status are
        acknowledged.
        """
        self._acknowledged = True
        for child in self._children.values():
            if child.state is not State.okay and not child.acknowledged:
                self._acknowledged = False
                break

        return self._acknowledged

    @property
    def totals(self):
        """ Tabulate totals for all states amongst children.  """
        if self._totals is None:
            self._totals = {
                State.okay: 0,
                State.unknown: 0,
                State.warning: 0,
                State.error: 0,
                State.unusable: 0
            }

            for child in self._children.values():
                self._totals = {
                    st: self._totals[st] + child.totals.get(st, 0)
                    for st in State
                }

        return self._totals

    def iterate(self, depth=0, lineage=None):
        """
        Create generator for iterating children.

        Args:
            depth: tree depth of descent
            lineage: tuple or list of parent's name, grandparent's, ...

        Yields:
            path: node path (list of node name, parent, grandparent, ...)
            depth: node depth in tree
            state: node state
            self
        """
        yield from super().iterate(depth, lineage)

        for child in self._children.values():
            yield from child.iterate(
                depth+1,
                (lineage if lineage is not None else []) + [self._name]
            )

    def __iter__(self):
        return self.iterate()

    def to_dict(self):
        """ Convert object to dict """
        d = {
            'name': self._name,
            'state': self.state.name
        }
        #d['nodes'] = {
        #    name: node.to_dict() for name, node in self._children.items()
        #}
        d['nodes'] = [
            node.to_dict() for node in self._children.values()
        ]

        return d

class Node(Tree):
    """
    A status tree node a hierarchy of groups, optionally, and nodes and
    their statuses.  Statuses are represented as leaf nodes and are further
    specialized.
    """

    def __init__(self, name, registration=None):
        super().__init__(name)
        self._registration = registration

    def add_status(self, test, state, acknowledgement=None, stale=False):
        """ Add status node as child """
        status = Leaf(test, state, acknowledgement, stale)
        self._children[test] = status
        return status

    def to_dict(self):
        d = {
            'node': self._name,
            'registered': self._registration,
            'state': self.state.name
        }
        if self.acknowledged:
            d['acknowledged'] = self.acknowledged
        #d['statuses'] = [
        #    child.to_dict() for child in self._children.values()
        #]
        d['statuses'] = self._children

        return d

class Leaf(Base):
    """
    A status leaf node representing a single task and its status.
    """

    def __init__(self, test, state, message=None, reported=None,
            acknowledged=None, acknowledgement=None, stale=False):
        super().__init__(test)
        self._state = state
        self._message = message
        self._reported = reported
        self._acknowledged = acknowledged
        self._acknowledgement = acknowledgement
        self._stale = stale

    @property
    def state(self):
        """ Get leaf's test state. """
        return self._state

    @state.setter
    def state(self, value):
        """ Set leaf's test state. """
        self._state = value

    @property
    def message(self):
        """ Get message. """
        return self._message

    @message.setter
    def message(self, value):
        """ Set message. """
        self._message = value

    @property
    def reported(self):
        """ Get reported. """
        return self._reported

    @reported.setter
    def reported(self, value):
        """ Set reported. """
        self._reported = value

    @property
    def acknowledged(self):
        """ Query when acknowledged--if none, hasn't been. """
        return self._acknowledged

    @acknowledged.setter
    def acknowledged(self, value):
        """ Set acknowledged timestamp. """
        self._acknowledged = value

    @property
    def acknowledgement(self):
        """ Get acknowledgement. """
        return self._acknowledgement

    @acknowledgement.setter
    def acknowledgement(self, value):
        """ Set acknowledgement. """
        self._acknowledgement = value

    @property
    def stale(self):
        """ Query whether status is stale. """
        return self._stale

    @stale.setter
    def stale(self, value):
        """ Set staleness of status. """
        self._stale = value

    @property
    def totals(self):
        """ Return dict of state counts (trivial for a leaf node). """
        return {
            self._state: 1
        }

    def to_dict(self):
        """ Return dict representation of object. """
        d = {
            'test': self._name,
            'state': self._state.name,
            'stale': self._stale
        }
        if self.acknowledgement:
            d['acknowledgement'] = self._acknowledgement
        return d
