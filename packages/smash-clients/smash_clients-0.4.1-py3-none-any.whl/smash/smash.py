# pylint:
#
"""
Smash client code.
"""
import requests
from smash.status import State, Tree, Node, Leaf


state_totals = {
    'okay': 0,
    'unknown': 0,
    'warning': 0,
    'error': 0,
    'unusable': 0,
    'stale': 0,
    'acknowledged': 0,
    'all': 0
}


def get_nodes_by_attribute(api_url, timeout, attribute, nogroupname='NA'):
    """
    Loads nodes from Smash server, grouped by given attribute, and their
    statuses.
    """
    # initialize API handler
    api = ApiHandler(api_url, timeout)

    # retrieve data
    data = api.get_nodes_by_attribute(attribute)

    # build status tree
    status_tree = Tree("smash")
    for groupname, nodedefs in data.items():
        groupname = groupname if groupname else nogroupname
        # create group node
        group = Node(groupname)
        status_tree[groupname] = group

        # create and populate nodes
        for nodedef in nodedefs:
            # create node
            nodename = nodedef['node']
            node = Node(nodename, registration=nodedef['registration'])
            group[nodename] = node

            # get node statuses
            statuses = api.get_node_status(nodename)
            for statusdef in statuses:
                # add status to node object
                status = Leaf(
                    statusdef['test'],
                    State[statusdef['state']],
                    message=statusdef.get('message'),
                    reported=statusdef.get('reported'),
                    acknowledged=statusdef.get('acknowledged'),
                    acknowledgement=statusdef.get('acknowledgement'),
                    stale=statusdef['stale']
                )
                node[statusdef['test']] = status

    return status_tree

def get_nodes(api_url, timeout):
    """
    Loads nodes and their statuses from the Smash server.
    """
    # initialize API handler
    api = ApiHandler(api_url, timeout)

    # retrieve data
    data = api.get_all_status()

    # build status tree
    status_tree = Tree("smash")
    for datum in data:
        nodename = datum['node']

        # retrieve or create node object
        try:
            node = status_tree[nodename]
        except KeyError:
            node = Node(nodename)
            status_tree[nodename] = node

        # add status to node object
        status = Leaf(
            datum['test'],
            State[datum['state']],
            message=datum.get('message'),
            reported=datum.get('reported'),
            acknowledged=datum.get('acknowledged'),
            acknowledgement=datum.get('acknowledgement'),
            stale=datum['stale']
        )
        node[datum['test']] = status

    return status_tree


# TODO: Make this unit-testable, so given the JSON, interpret the objects
#   With whatever mechanism uses `yield()`, create function that takes the
#   URL and creates the node objects
# TODO: simplify with new /status/ API call
def load_nodes(api_url, timeout):
    """ Loads nodes from Smash server and their statuses.
    """
    nodes = requests.get(api_url + '/nodes/', timeout=timeout).json()
    for node in nodes:

        node['totals'] = {
            'okay': 0,
            'unknown': 0,
            'warning': 0,
            'error': 0,
            'unusable': 0,
            'stale': 0,
            'acknowledged': 0,
            'all': 0
        }

        # request status
        node['statuses'] = requests.get(
            f"{api_url}/nodes/{node['node']}/status/", timeout=timeout
        ).json()
        for status in node['statuses']:
            if 'acknowledged' in status:
                state_totals['acknowledged'] += 1
                node['totals']['acknowledged'] += 1
            elif status['stale']:
                state_totals['stale'] += 1
                node['totals']['stale'] += 1
            else:
                state = status['state']
                state_totals[state] += 1
                node['totals'][state] += 1
            state_totals['all'] += 1
            node['totals']['all'] += 1
            status['message'] = status['message'].replace('\n','; ')

    return nodes


class ApiException(Exception):
    """ API exception class. """

    def __init__(self, response):
        self._response = response

    def __str__(self):
        string = f"{self._response.status_code}: {self._response.reason}"
        body = self._response.json()
        if message := body.get('message'):
            string += f" ({message})"
        return string

    @property
    def response(self):
        """ Return response """
        return self._response


def assert_ok(result):
    """ Assert result is okay. """
    if not result.ok:
        # TODO: if possible to set call stack one below
        raise ApiException(result)


class ApiHandler:
    """
    ApiHandler class something something
    """

    def __init__(self, api_url, timeout):
        self._api_url = api_url
        self._timeout = timeout

    def get_nodes_by_attribute(self, attribute):
        """ Retrieve nodes grouped by value of given attribute.
        """
        result = requests.get(
            f"{self._api_url}/attributes/{attribute}/nodes/",
            timeout=self._timeout
        )

        assert_ok(result)
        return result.json()

    def get_node(self, node):
        """
        Retrieve node information and status
        """
        # TODO: Not DRY along with load_nodes()

        obj = {
            'totals': {
                'okay': 0,
                'unknown': 0,
                'warning': 0,
                'error': 0,
                'unusable': 0,
                'stale': 0,
                'acknowledged': 0,
                'all': 0
            },
            'status': []
        }

        # request statuses
        result = requests.get(
            f"{self._api_url}/nodes/{node}/status/", timeout=self._timeout
        )
        assert_ok(result)
        statuses = result.json()

        for status in statuses:
            if 'acknowledged' in status:
                state_totals['acknowledged'] += 1
                obj['totals']['acknowledged'] += 1
            elif status['stale']:
                state_totals['stale'] += 1
                obj['totals']['stale'] += 1
            else:
                state = status['state']
                state_totals[state] += 1
                obj['totals'][state] += 1
            state_totals['all'] += 1
            obj['totals']['all'] += 1
            status['message'] = status['message'].replace('\n','; ')
            obj['status'].append(status)

        return obj

    def get_node_status(self, node, status=None):
        """
        Retrieve a particular status for a node.
        """
        if status:
            # retrieve specific status for node
            result = requests.get(
                f"{self._api_url}/nodes/{node}/status/{status}", timeout=self._timeout
            )
        else:
            # return all status for node
            result = requests.get(
                f"{self._api_url}/nodes/{node}/status/", timeout=self._timeout
            )
        assert_ok(result)
        return result.json()

    def get_all_status(self):
        """
        Retrieve all current status.
        """

        result = requests.get(
            f"{self._api_url}/", timeout=self._timeout
        )
        assert_ok(result)
        return result.json()

    def acknowledge(self, node, status, message=None, state=None, expiry=None):
        """
        Acknowledge a particular status on a node.
        """

        result = requests.put(
            f"{self._api_url}/nodes/{node}/status/{status}/acknowledgement",
            timeout=self._timeout,
            json={
                'message': message,
                'state': state,
                'expires-in': expiry
            }
        )
        assert_ok(result)
        return result.json()

    def set_attribute(self, node, markspec):
        """
        Set a tag or attribute on a node.
        """
        tokens = markspec.split('=', 2)
        attribute = tokens[0]
        if len(tokens) > 1:
            value = tokens[1]
        else:
            value = True
        result = requests.put(
            f"{self._api_url}/nodes/{node}/attributes/{attribute}",
            timeout=self._timeout,
            json={
                'value': value
            }
        )

        assert_ok(result)
        return result.json()

    def clear_attribute(self, node, mark):
        """
        Clear a tag or attribute on a node.
        """
        result = requests.delete(
            f"{self._api_url}/nodes/{node}/attributes/{mark}",
            timeout=self._timeout
        )

        assert_ok(result)
        return result.json()

    def delete_node(self, node):
        """
        Delete a node.
        """

        result = requests.delete(
            f"{self._api_url}/nodes/{node}",
            timeout=self._timeout
        )

        assert_ok(result)
        return result.json()

    def delete_node_status(self, node, status):
        """
        Delete the given status for the given node.
        """

        result = requests.delete(
            f"{self._api_url}/nodes/{node}/status/{status}",
            timeout=self._timeout
        )

        assert_ok(result)
        return result.json()
