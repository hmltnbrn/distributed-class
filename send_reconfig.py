#!/usr/bin/python
"""
Broadcast initial reconfig message
"""

import sys

import tree_algo


def main():
    if len(sys.argv) == 2:
        # Get node_id from command line argument
        node_id = sys.argv[1]
        # Create node
        node = tree_algo.Node(int(node_id))
        # Send reconfig message
        node.send_reconfig_message()
    else:
        print("usage: %s node_id" % sys.argv[0])


if __name__ == "__main__":
    main()
