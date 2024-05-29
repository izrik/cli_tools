#!/usr/bin/env python3

import argparse
import os
import subprocess
import sys

import yaml

HOME = os.getenv('HOME')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('identity')
    parser.add_argument('--config', '-c', default=f'{HOME}/.cswitch.yaml')
    args = parser.parse_args()
    identity = args.identity
    config_path = args.config
    with open(config_path) as f:
        config = yaml.safe_load(f)
    identities = config.get('identities') or {}
    ident = identities.get(identity)
    if not ident:
        print(f'Identity not found: \"{identity}\"', file=sys.stderr)
        if identities:
            print('  Available identities:', file=sys.stderr)
            for ident_name in identities.keys():
                print(f'    {ident_name}', file=sys.stderr)
        else:
            print('  No available identities found', file=sys.stderr)
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
