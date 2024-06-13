# pylint: disable=too-many-branches
#   This is fine.
#
"""
Smash command-line interface client.
"""
import json
from requests.exceptions import ReadTimeout
from smash import config
from smash import smash


def json_result(result):
    """ Print result as JSON. """
    print(json.dumps(result, indent=2))


def json_error(result):
    """ Print error as JSON. """
    print(json.dumps({
        'status_code': result.status_code,
        'reason': result.reason,
        'message': result.json()['message']
    }, indent=2))


def print_result(result):
    """ Print result as text. """
    if len(result['status']) > 1:
        # print totals summary
        print(f"Of {result['totals']}")
    # result might be a list
    for item in result:
        print(item)


def print_error(errmsg):
    """ Print error as text. """
    print(f"Error {errmsg}")


def success(result):
    """ Success callback
    """
    # pylint: disable=unused-argument
    # don't actually need to do anything
    pass

def main():
    """ Main client routine.

    I do not remember the scheme with the return code's values.
    """
    # pylint: disable=too-many-statements

    # load configuration
    # pylint: disable=invalid-name,broad-except
    try:
        conf = config.common(config.cli)

    except Exception as e:
        print(f"Could not load Smash configuration: {e}")
        return 131

    api = smash.ApiHandler(api_url=f"{conf['server']}/api",
        timeout=conf['request_timeout'])

    # for collecting output and result
    output = None

    # for handling result output (non-JSON)
    output_fn = print_result

    # DO put this next section in a try..except thingy (maybe)
    # the idea being to capture any exceptions and output them appropriately

    # handle command
    retcode = 0
    try:
        if conf.cmd == 'get':

            output = []
            if conf.nodestatus:
                for ns in conf.nodestatus:
                    if ns[1]:
                        output.append(api.get_node_status(ns[0], ns[1]))
                    else:
                        output.append(api.get_node(ns[0]))
            elif conf.group_by:
                #output.append(api.get_nodes_by_attribute(conf.group_by))
                output.append(
                    smash.get_nodes_by_attribute(
                        f"{conf['server']}/api", conf['request_timeout'], conf.group_by))
            else:
                output.append(smash.get_nodes(f"{conf['server']}/api", conf['request_timeout']))

        # Delete operation not yet supported--requires authentication
        #    elif args.cmd in ['del', 'delete']:
        #
        #        output = []
        #        for ns in args.nodestatus:
        #            if ns[1]:
        #                output.append(api.delete_node_status(ns[0], ns[1]))
        #            else:
        #                output.append(api.delete_node(ns[0]))

        elif conf.cmd in ['ack', 'acknowledge']:
            output = api.acknowledge(conf.nodestatus[0], conf.nodestatus[1],
                conf.message, conf.state, conf.expire_after)

            # output is not like everything else: or is it?
            # output will be: a response with error (handled by error
            # routines), or a collection of nodes and maybe statuses, or a
            # response like this from a "do something" request as opposed to a
            # "get something" request.  If we can't find a way to deal with
            # all three cases generically, we could set a fn in each command
            # clause for non-JSON output handling, so the "if JSON" stuff
            # below can still be simple.  Or we handle it here with repeated
            # "if conf.json: json_result" etc. which is repetitive
            # ex.
            # output_fn = handle_ack_response
            output_fn = success

        elif conf.cmd == 'tag':

            output = []
            node = conf.node
            if not conf.untag:
                for markspec in conf.mark:
                    output.append(api.set_attribute(node, markspec))
            else:
                for markspec in conf.markspec:
                    output.append(api.clear_attribute(node, markspec))

            output_fn = success

        else:
            print_error(f"Command not recognized: {conf.cmd}")

        # handle output
        if not output:
            if conf.json:
                json_error(f"{conf.cmd} unsuccessful")
            else:
                print_error(f"{conf.cmd} unsuccessful")
        else:
            if conf.json:
                json_result(output)
            else:
                output_fn(output)

    except smash.ApiException as e:
        if conf.json:
            json_error(e.response)
        else:
            print_error(e)
        retcode = 128
    except ReadTimeout as e:
        print_error("in request: Connection timed out")
        retcode = 129
    except ConnectionError as e:
        print_error("in request: Could not connect to server")
        retcode = 130

    return retcode

# if this module was called directly
if __name__ == '__main__':
    main()
