#! /usr/bin/python
import sys
import os.path
import re

path = os.path.abspath(sys.argv[1])
if not os.path.isfile(path): raise ValueError('Invalid File!')

regex_blank = re.compile(r'^$')
regex_model = re.compile(r'^class (?P<model_name>.*)\(.*\):$')
regex_field = re.compile(r'^(?P<field_name>.*) = (?P<field_type>.*)\((?P<options>.*)\)')

analysis = []
current_model = None

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
        analysis.append('Model => %s' % current_model)
    elif m3:
        print 'F-> ', l
        analysis.append('Field => %(model)s => %(field)s' % {
            'model': current_model,
            'field': m3.groupdict()['field_name']})
    else:
        print '?-> ', l
f.close()

print '=== Analysis ==='
for l in analysis: print l
