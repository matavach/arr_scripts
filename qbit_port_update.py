#!/usr/bin/python
from qbittorrent import Client
import sys
import argparse

parser = argparse.ArgumentParser(description="A script that processes named arguments.")

    # Add arguments
parser.add_argument('--url', type=str, required=True, help='URL of qBittorent instance')
parser.add_argument('--user', type=str, required=True, help='Admin username for qBittorent')
parser.add_argument('--password', type=str, required=False, help='Admin password for qBittorent')
parser.add_argument('--portfile', type=str, required=True, help='Location of gluetun port forward file')
    # Parse the arguments from the command line
args = parser.parse_args()

qb = Client(args.url)

try:
    with open(args.portfile) as file:
        port = file.read()
except FileNotFoundError:
    print(f"Error: The file '{args.portfile}' was not found.")
    sys.exit(1)

try:
    if args.password:
        qb.login(args.user)
    else:
        qb.login(args.user, args.password)
    qb.set_preferences(listen_port=port)
    print(f"Set port to {port}")
except Exception as e:
    print(e)
    sys.exit(1)







