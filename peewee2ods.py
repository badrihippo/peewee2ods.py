#! /usr/bin/python
import sys
import os.path
import re

path = os.path.abspath(sys.argv[1])
if not os.path.isfile(path): raise ValueError('Invalid File!')

regex_blank = re.compile(r'^$')
regex_model = re.compile(r'^class (?P<model_name>.*)\(.*\):$')
regex_field = re.compile(r'^(?P<field_name>.*) = (?P<field_type>.*)\((?P<options>.*)\)')

current_model = None

models = {}

f = open(path, 'r')
for line in f.readlines():
    l = line.strip()
    m1 = regex_blank.match(l)
    m2 = regex_model.match(l)
    m3 = regex_field.match(l)
    if m1:
        print '--> ', l
    elif m2:
        print 'M-> ', l
        d = m2.groupdict()
        current_model = d['model_name']
        models[current_model] = [] # List of fields
    elif m3:
        print 'F-> ', l
        d = m3.groupdict()
        models[current_model].append({
            'name': d['field_name'],
            'type': d['field_type'],
            'options_string': d['options']})
    else:
        print '?-> ', l
f.close()

print '=== Dict dump ==='
for model, fieldlist in models.items():
    print 'Model: %s' % model
    for f in fieldlist:
        print '  * %s (%s)' % (f['name'], f['type'])
