import subprocess
import argparse
import json

def get_subs(args):
    for network in args.networks:
        bashCommand = f"""curl --insecure --verbose --key {args.aopkey} --cert {args.aopcert}\
              'https://{args.domain}:9443/magma/v1/lte/{network}/subscribers?verbose={args.verbose}' -H 'accept: application/json'"""
        list_subs = subprocess.run(bashCommand, shell=True,capture_output=True)
        jsonstr = json.loads(list_subs.stdout.decode("utf-8").strip())
        subscribers = jsonstr["subscribers"]
        print(f"""Network Name: {network}\n{json.dumps(subscribers, indent = 3)}""")

parser = argparse.ArgumentParser(
                    description='List all the subscribers associated with a network')
parser.add_argument('verbose', metavar='Verbosity',
                    type=str,
                    help="enter 'true' or 'false' to toggle verbose output")
parser.add_argument('aopkey', metavar='Key',
                    type=str,
                    help ='path to admin_operator.key.pem')
parser.add_argument('aopcert', metavar='Cert',
                    type=str,
                    help ='path to admin_operator.pem')
parser.add_argument('domain', metavar='Domain',
                    type=str,
                    help ='orc8r domain name or IP address')
parser.add_argument('networks', metavar='NetworksList',
                    type=str, nargs='+',
                    help ='a list of networks separated by spaces')
args = parser.parse_args()
try:
    get_subs(args)
except:
    parser.print_help