
import argparse
import subprocess
from .parsers import lsmem_parser, free_parser, other_command_parser

def run_command(command):
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        raise RuntimeError(f"Command '{command}' failed with error: {result.stderr.decode()}")
    return result.stdout.decode()

def parse_command_output(command_output, parser_name):
    parsers = {
        'lsmem': lsmem_parser.parse,
        'free': free_parser.parse,
        # Add other parsers here
    }
    if parser_name in parsers:
        return parsers[parser_name](command_output)
    else:
        raise ValueError(f"No parser found for {parser_name}")

def main():
    parser = argparse.ArgumentParser(description='JP - JSON Parser for Linux commands')
    parser.add_argument('command', type=str, help='The Linux command to run')
    parser.add_argument('parser_name', type=str, nargs='?', default='', help='The name of the parser to use')

    args = parser.parse_args()
    result = jpcli(args.command, args.parser_name)
    print(result)

def jpcli(command, parser_name):
    output = run_command(command)
    return parse_command_output(output, parser_name)
