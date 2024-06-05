#!/usr/bin/env python3

import argparse
import os
import subprocess
import sys

import yaml

HOME = os.getenv('HOME')


def get_available_identities(identities):
    if not identities:
        return []
    return list(identities.keys())


def print_available_identities(identities):
    identities = get_available_identities(identities)
    if identities:
        print(f'Available identities:', file=sys.stderr)
        for ident_name in identities:
            print(f'  {ident_name}', file=sys.stderr)
    else:
        print(f'No available identities found', file=sys.stderr)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('identity', nargs='?')
    parser.add_argument('--config', '-c', default=f'{HOME}/.cswitch.yaml')
    parser.add_argument('--list', '-l', action='store_true')
    args = parser.parse_args()
    config_path = args.config
    with open(config_path) as f:
        config = yaml.safe_load(f)
    identities = config.get('identities') or {}
    if args.list:
        print_available_identities(identities)
        return

    identity = args.identity
    if not identity:
        parser.print_usage()
        print("Error: the following arguments are required: identity")
        sys.exit(1)

    ident = identities.get(identity)
    if not ident:
        print(f'Identity not found: \"{identity}\"', file=sys.stderr)
        print_available_identities(identities)
        sys.exit(1)

    configuration = ident.get('configuration')
    if configuration:
        cmd = ['gcloud', 'config', 'configurations', 'activate', configuration]
        rv = subprocess.run(cmd)

    account = ident.get('account')
    if not account:
        print('No "account" configured for this identity', file=sys.stderr)
        sys.exit(1)
    project = ident.get('project')
    if not project:
        print('No "project" configured for this identity', file=sys.stderr)
        sys.exit(1)
    rv = subprocess.run(['gcloud', 'config', 'set', 'account', account])
    rv = subprocess.run(['gcloud', 'config', 'set', 'project', project])

    context = ident.get('context')
    if context:
        rv = subprocess.run(['kubectl', 'config', 'use-context', context])

    cluster = ident.get('cluster')
    zone = ident.get('zone')
    if cluster:
        cmd = ['gcloud', 'container', 'clusters', 'get-credentials', cluster]
        if zone:
            cmd.extend(['--zone', zone])
        rv = subprocess.run(cmd)

        namespace = ident.get('namespace')
        if namespace:
            cmd = ['kubectl', 'config', 'set-context', '--current',
                   f'--namespace={namespace}']
            re = subprocess.run(cmd)


if __name__ == '__main__':
    main()
