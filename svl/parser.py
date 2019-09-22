# Copyright (C) 2019 Korey Hinton
# This file is part of the svl project which is licensed under LGPL version 3
# See LICENSE file for full license details
class El:
    def __init__(self, name, kv={}):
        self.name = name
        self.kv = kv
    def get(self, key):
        return self.kv[key]
    def set(self, kv):
        self.kv = kv

def _parse_var(s, i, l, els):
    # assume s starts with '#'
    # print(s[i]=='#')
    i += 1
    key = ''
    while i<l and s[i] != '.':
        key += s[i]
        i += 1
    if i>= l or (i<l and s[i] != '.'):
        return (i, '')
    i += 1
    attrkey = ''
    while i<l and s[i] != '#':
        attrkey += s[i]
        i += 1
    if i>=l or (i<l and s[i] != '#'):
        return (i, '')
    attrval = ''
    for el in els:
        if el.name == key:
            attrval = el.get(attrkey)
            break
#    print(attrval)
    return (i, attrval)

def _parse_el_attr_val(s, i, l, els):
#    print('    start:' + s[i])
    val = ''
    # assume it starts with '='
    # print(s[i]=='=')
    #while i<l and (s[i]==' ' or s[i]=='\t'):
    #    i += 1
    #if i<l or (i<l and not s[i] == '='):
    #    print('    end:' + s[i])
    #    return (i, val)
    i += 1
    while i<l and (s[i]==' ' or s[i]=='\t'):
        i += 1
    if i>=l or (i<l and s[i] != '"'):
#        print(' [b]end:' + s[i])
        return (i, val)
    if s[i] != '"':
        return (i, val)
    i += 1
    while i<l and s[i] != '"':
        if i+1<l and s[i]=='\\' and s[i+1]=='#':
            i += 1
        elif i+1<l and s[i]=='\\' and s[i+1]=='"':
            i += 1
        elif s[i] == '#':
            i, v = _parse_var(s, i, l, els)
            val += v
        else:
            val += s[i]
        i += 1
    if i<l and s[i] != '"':
#        print('    end:' + s[i])
        return (i, val)
    i += 1
    while i<l and s[i] != '\n':
        i += 1
    if i<l and s[i]=='\n':
        i += 1
#    print('    end:' + s[i])
    return (i, val)

def _parse_el_attr_key(s, i, l):
#    print('start: '+s[i])
#    print('       si=' + str(i))
    key = ''
    while i<l and not (s[i].isspace() or s[i]=='='):
        key += s[i]
        i += 1
    if i<l and (s[i]==' ' or s[i] == '\t') and s[i] != '=':
        i += 1
#    print('end: '+s[i])
#    print('       ei=' + str(i))
    return (i, key)

def _parse_el_nm(s, i, l):
    nm = ''
    while i<l and not s[i].isspace():
        nm += s[i]
        i += 1
    while i<l and s[i] != '\n':
        i += 1
    if i<l and s[i]=='\n':
        i += 1
    return (i, nm)

def _skip_ws(s, i, l):
    while i<l and s[i].isspace():
        i += 1
    return i

def _skip_ind(s, i, l):
    while i<l and not (s[i]==' ' or s[i]=='\t') and s[i].isspace():
        i += 1
    skipped = False
    while i<l and (s[i]==' ' or s[i]=='\t'):
        skipped = True
        i += 1
    return (i, skipped)

def parse(svl):
    arr = []
    i = 0
    l = len(svl)
    while i < l:
        j = i
        if svl[i].isspace():
            i = _skip_ws(svl, i, l)
        i, nm = _parse_el_nm(svl, i, l)
        if nm == '':
            break
        el = El(nm)
        indented = True
        d = {}
        while indented:
            i, indented = _skip_ind(svl, i, l)
            i, key = _parse_el_attr_key(svl, i, l)
#            print('        i=' + str(i))
            if key=='':
                break
            if svl[i] != '=':
                continue
#            print(key)
#            print(svl[i])
            i, val = _parse_el_attr_val(svl, i, l, arr)
#            print('    '+val)
            d[key] = val
            if i>=l or (i+1<l and not svl[i+1].isspace()):
                break
#        print(el.name)
        el.set(d)
        arr.append(el)
        if i<l and svl[i].isspace():
            i = _skip_ws(svl, i, l)
#        print(svl[i])
        if i <= j:
            i = j + 1
    return arr
