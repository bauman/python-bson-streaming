# python-bson-streaming
A small python library with tools to work with raw bson data exported from mongodb

## Source
This code is derived from the mongo-hadoop connector
https://github.com/mongodb/mongo-hadoop/blob/master/streaming/language_support/python/pymongo_hadoop/input.py


## Background
I needed a way to read BSON dumped from mongodb into python for customized map reduce scripts.

I did not want the overhead of hadoop and wanted to add a fast string prematcher to expedite map reduce

Because the source is a NoSQL database, not all documents contain the same types of data.  
As bson stores raw text, a fast string matcher quickly bypasses unwanted documents. 

I understand this has extremely limited usage, but it worked well for my needs.

## Installation

The python-bson-streaming library can be installed via the distutils setup.py script
included at the root directory:

<code>
python setup.py install
</code>

## Usage

this example shows an example start to a map/reduce style script.  

The fast_string_prematch would not bother converting records that do not have "github" 
somewhere in the document as plaintext.

<code>
from bsonstream import KeyValueBSONInput
from sys import argv
import gzip

for file in argv[1:]:
    f=None
    if "gz" not in file:
        f = open(file, 'rb')
    else:
        f=gzip.open(file,'rb')

    stream = KeyValueBSONInput(fh=f,  fast_string_prematch="github")
    for id, dict_data in stream:
        if id:
            ...process dict_data...

</code>


## Benchmark
Unfortunately, I cannot make available the test bson file.

used an 8GB bson file with ~2,500,000 documents of verying sizes
gzipped bson file compressed to 2.1GB


Without fast string matcher
<code>
[bauman@localhost ~]$ time ./example_map_reduce.py bson/example.bson.1.gz
 
real    6m55.758s
user    6m53.541s
sys     0m1.952s
</code>

With fast string matcher.  In this case, documents matching the fast string patern were present in 10% of documents, resuling in time savings not deserializing 90% of documents.  
<code>
[bauman@localhost ~]$ time ./example_fast_match_map_reduce.py bson/example.bson.1.gz  

real    1m16.387s
user    1m37.455s
sys     0m17.427s
</code>



## Dependencies

Required libraries
* [python-bson] 


## Versioning


