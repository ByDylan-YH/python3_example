from collections import ChainMap
import os, argparse

defaults = {
    'color': 'red',
    'user': 'guest'
}

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--user')
parser.add_argument('-c', '--color')
namespace = parser.parse_args()
print(namespace)
command_line_args = {k: v for k, v in vars(namespace).items() if v}
print(command_line_args)

combined = ChainMap(command_line_args, os.environ, defaults)
print('color=%s' % combined['color'])
print('user=%s' % combined['user'])
