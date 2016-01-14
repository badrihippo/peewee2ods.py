#! /usr/bin/python
import sys
import os.path
import re
import odswriter as ods

regex_blank = re.compile(r'^$')
regex_model = re.compile(r'^class (?P<model_name>.*)\(.*\):$')
regex_field = re.compile(r'^(?P<field_name>.*) = (?P<field_type>.*)\((?P<options>.*)\)')

def process_file(filepath):
    current_model = None
    models = {}
    if not os.path.isfile(filepath): raise ValueError('Invalid File!')
    f = open(filepath, 'r')
    for line in f.readlines():
        l = line.strip()
        m1 = regex_blank.match(l)
        m2 = regex_model.match(l)
        m3 = regex_field.match(l)
        if m1:
            pass # print '--> ', l
        elif m2:
            # print 'M-> ', l
            d = m2.groupdict()
            current_model = d['model_name']
            models[current_model] = [] # List of fields
        elif m3:
            # print 'F-> ', l
            d = m3.groupdict()
            models[current_model].append({
                'name': d['field_name'],
                'type': d['field_type'],
                'options_string': d['options']})
        else:
            print '?-> ', l
    f.close()
    return models

def print_data(models):
    '''Print model data from formatted dictionary'''
    
    print '=== Dict dump ==='
    for model, fieldlist in models.items():
        print 'Model: %s' % model
        for f in fieldlist:
            print '  * %s (%s)' % (f['name'], f['type']),
            if f.has_key('options_string'):
                print options_to_dict(f['options_string'])

def options_to_dict(options_string):
    '''Parse a string of options and output a formatted dictionary'''
    optlist = options_string.split(',')
    optdict = {}
    for o in optlist:
        o = o.strip().split('=')
        if len(o) == 2: optdict[o[0]] = o[1]
    return optdict

def get_option_table_index(models):
    '''
    Creates a unique list of options from all the models, so that they
    can be used to position options in the spreadsheet.
    '''
    all_option_names = []
    for model, fieldlist in models.items():
        for field in fieldlist:
            if not field.has_key('options_dict'):
                field['options_dict'] = options_to_dict(field['options_string'])
            for option, value in field['options_dict'].items():
                if all_option_names.count(option) == 0:
                    all_option_names.append(option)
    return all_option_names

def write_data(models, outfile='peewee_models.ods', overwrite=False):
    '''Write model data from process_file() to ODS output'''
    outfile=os.path.abspath(outfile)
    if (not overwrite) and os.path.exists(outfile):
        raise ValueError, 'File already exists!'
    optindex = get_option_table_index(models)
    with ods.writer(open(outfile, 'wb')) as odsfile:
        for model, fieldlist in models.items():
            modelsheet = odsfile.new_sheet(model)
            line = ['name', 'type'] + [o for o in optindex]
            modelsheet.writerow(line)
            for field in fieldlist:
                line = [field['name'], field['type']] + ['' for i in range(len(optindex))]
                if field.has_key('options_string'):
                    if not field.has_key('options_dict'):
                        field['options_dict'] = options_to_dict(field['options_string'])
                    for option, value in field['options_dict'].items():
                        line[optindex.index(option)+2] = value
                modelsheet.writerow(line)

if __name__ == '__main__':
    path = os.path.abspath(sys.argv[1])
    models = process_file(path)
    print_data(models)
    write_data(models)
