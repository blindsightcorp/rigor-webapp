#!/usr/bin/env python

from __future__ import division
import os
import random
import time
import json
import pprint

#--------------------------------------------------------------------------------

class ExtraKeyException(Exception): pass
class MissingKeyException(Exception): pass
class WrongTypeException(Exception): pass

# todo:
#   coerce types (unicode, str->int...)
#   remove extra keys
#   allow only some keys to be required and some to be optional
#   handle lists
#   write a ton of tests

def validate(schema, input, allowExtraKeys=False, allowMissingKeys=False, stack=[]):
    schemaKeys = set(schema.keys())
    inputKeys = set(input.keys())

    if not allowExtraKeys:
        if inputKeys - schemaKeys:
            raise ExtraKeyException('extra key(s): %s'%str(list(inputKeys-schemaKeys)))
    if not allowMissingKeys:
        if schemaKeys - inputKeys:
            raise MissingKeyException('missing key(s): %s'%str(list(schemaKeys-inputKeys)))


    for key, expectedVal in schema.items():
        if key not in input: continue

        if type(expectedVal) == type:
            expectedType = expectedVal
        else:
            expectedType = type(expectedVal)

        actualVal = input[key]
        actualType = type(actualVal)
        if not actualType == expectedType:
            raise WrongTypeException('in %s: key %s should be %s but is %s which is type %s'%('/'+'/'.join([str(s) for s in stack]),repr(key),expectedType,repr(actualVal),actualType))

        if actualType == expectedType == dict:
            result = validate(expectedVal,actualVal,stack=stack+[key])
            if not result: return result

    return True

if __name__ == '__main__':
    schema = {
        'id': int,
        'hash': str,
        'subdict': {
            'a': 1,
            'b': 2,
        },
    }

    input = {
        'id': 847,
        'hash': 'hello',
        'subdict': {
            'a': 1,
            'b': 'yo',
        },
    }
    print validate(schema,input)
