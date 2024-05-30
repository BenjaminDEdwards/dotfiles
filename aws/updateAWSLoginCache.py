#!/usr/bin/env python3

import boto3
from datetime import datetime
from dataclasses import dataclass, asdict
import json
import os
import sys

plaintext_file = "/tmp/aws_current_env"
cache_file = "/tmp/aws_env_cache"

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
  except Exception as e:
    return CachedValue(
      int(now.timestamp()) + 60,
      'unknown',
      now.strftime('%Y-%m-%d %H:%M:%S'),
      False
    )



# caller_identity = boto3.Session().client('sts').get_caller_identity()
# account = caller_identity["Account"]

# iam = boto3.Session().client('iam')


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

if ( now_ts > cached_value.expires or cached_value.success == False ):
  print("Cache is stale, regenerate")
  cached = fetchResponse()

  with open(plaintext_file, 'w') as file:
    file.write(cached.env)

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
