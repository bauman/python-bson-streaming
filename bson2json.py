#!/usr/bin/python

from bson.json_util import dumps  # pip install pymongo
from bsonstream import BSONInput
from sys import argv, stdout
import gzip
import six


if "gz" in argv[1] or "dz" in argv[1]:
    f = gzip.open(argv[1], 'rb')
else:
    f = open(argv[1], "rb")

stream = BSONInput(fh=f)
for doc in stream:
    json_str = dumps(doc)
    if six.PY3:
        stdout.write("{}\n".format(json_str))
    else:  # six.PY2
        stdout.write("%s\n" %json_str)

