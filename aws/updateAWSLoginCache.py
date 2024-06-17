#!/usr/bin/env python3

import boto3
from botocore.exceptions import TokenRetrievalError
from datetime import datetime
from dataclasses import dataclass, asdict
import json
import os
import sys
import argparse
import yaml


parser = argparse.ArgumentParser(description="Fetch the aws environment")
parser.add_argument('pid', type=str, help="current pid")
parser.add_argument('--config', type=str, help="config file", default="")
parser.add_argument('--force', action='store_true', help='force cache refresh')

args = parser.parse_args()

plaintext_file = f'/tmp/aws_current_env_{args.pid}'
cache_file = f'/tmp/aws_env_cache_{args.pid}'


@dataclass(frozen=True)
class CachedValue:
  expires: int
  env: str
  generated: str
  success: bool

def fetchResponse():
  try:
    iam = boto3.client('iam')
    paginator = iam.get_paginator('list_account_aliases')
    now = datetime.now()
    for response in paginator.paginate():
      return CachedValue(
        int(now.timestamp()) + 60,
        response['AccountAliases'][0],
        now.strftime('%Y-%m-%d %H:%M:%S'),
        True
      )
  except TokenRetrievalError as e:
    return CachedValue(
      int(now.timestamp()) + 60,
      'not-signed-in',
      now.strftime('%Y-%m-%d %H:%M:%S'),
      False
    )
  except Exception as e:
    return CachedValue(
      int(now.timestamp()) + 60,
      'unknown',
      now.strftime('%Y-%m-%d %H:%M:%S'),
      False
    )


@dataclass(frozen=True)
class StringReplace:
  match: str
  replace_with: str

def load_string_replace_from_yaml(file_path: str) -> list[StringReplace]:
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
            return [StringReplace(**data)]
    else:
        return []

def apply_replacements(replacements: list[StringReplace], input_string: str) -> str:
    for replacement in replacements:
        input_string = input_string.replace(replacement.match, replacement.replace_with)
    return input_string

# caller_identity = boto3.Session().client('sts').get_caller_identity()
# account = caller_identity["Account"]

# iam = boto3.Session().client('iam')

replacements = load_string_replace_from_yaml(args.config)

if not os.path.isfile(cache_file):
    cached = fetchResponse()

    with open(plaintext_file, 'w') as file:
      file.write(cached.env)

    cached_value_dict = asdict(cached)
    cached_value_json = json.dumps(cached_value_dict, indent=2)
    with open(cache_file, 'w') as file:
      file.write(cached_value_json)
    sys.exit(1)

with open(cache_file, 'r') as file:
  data = json.load(file)  # Load the contents into a dictionary

data['expires'] = int(data['expires'])
cached_value = CachedValue(**data)

now = datetime.now()
now_ts = int(now.timestamp())

if ( now_ts > cached_value.expires or cached_value.success == False or args.force == True ):
  print("Cache is stale, regenerate")
  cached = fetchResponse()

  with open(plaintext_file, 'w') as file:
    replaced = apply_replacements(replacements,cached.env)
    file.write(replaced)

  cached_value_dict = asdict(cached)
  cached_value_json = json.dumps(cached_value_dict, indent=2)
  with open(cache_file, 'w') as file:
    file.write(cached_value_json)
else:
  print("Were good")

# print("Cached")
# print(cached_value)

# expires = int(now.timestamp()) + 60

# print(now_ts)
# print(expires)


# print(cached)
# print("Hello world")
