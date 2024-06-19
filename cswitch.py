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

    steps = identities.get(identity)
    if not steps:
        print(f'Identity not found: \"{identity}\"', file=sys.stderr)
        print_available_identities(identities)
        sys.exit(1)
    if isinstance(steps, dict):
        steps = [steps]
    if not steps:
        print(f'Identity not found: \"{identity}\"', file=sys.stderr)
        print_available_identities(identities)
        sys.exit(1)

    for step in steps:
        env = {**os.environ}
        __env__ = step.get('__env__')
        if __env__:
            env.update(__env__)

        configuration = step.get('gcloud:configuration')
        if configuration:
            cmd = ['gcloud', 'config', 'configurations', 'activate',
                   configuration]
            rv = subprocess.run(cmd, env=env)

        account = step.get('gcloud:account')
        if account:
            rv = subprocess.run(
                ['gcloud', 'config', 'set', 'account', account], env=env)
        project = step.get('gcloud:project')
        if project:
            rv = subprocess.run(
                ['gcloud', 'config', 'set', 'project', project], env=env)

        context = step.get('kubectl:context')
        if context:
            rv = subprocess.run(
                ['kubectl', 'config', 'use-context', context], env=env)

        cluster = step.get('gcloud:cluster')
        zone = step.get('gcloud:zone')
        if cluster:
            cmd = ['gcloud', 'container', 'clusters', 'get-credentials',
                   cluster]
            if zone:
                cmd.extend(['--zone', zone])
            rv = subprocess.run(cmd, env=env)

        namespace = step.get('kubectl:namespace')
        if namespace:
            cmd = ['kubectl', 'config', 'set-context', '--current',
                   f'--namespace={namespace}']
            rv = subprocess.run(cmd, env=env)

        aws_sso_login = step.get('aws:aws_sso_login')
        if aws_sso_login:
            cmd = ['aws', 'sso', 'login']
            rv = subprocess.run(cmd, env=env, stdout=sys.stdout,
                                stderr=sys.stderr)


if __name__ == '__main__':
    main()
