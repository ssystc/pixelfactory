# coding: utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import json
import copy
from collections import defaultdict

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(-1)

    filename = sys.argv[1]
    with open(filename) as f:
        md = json.load(f)
    
    inputs = md['Userproperty']['InputParameter']['InputFilePath']
    outputs = md['Userproperty']['OutputParameter']['OutPutFilePath']

    print inputs

    multis = defaultdict(list)
    for inp in inputs:
        if inp.get('multi') or 'index' in inp:
            multis[inp['name']].append(inp)
    print multis
    multiCount = max([len(inps) for inps in multis.itervalues()])

    basename = 'test'

    multioutputs = []

    for upt in outputs:
        if upt.get('multi'):
            multioutputs.append(upt)
        else:
            upt['value'] = basename + upt['suffix']

    for mout in multioutputs:
        outputs.remove(mout)
        for i in range(multiCount):
            mo = copy.deepcopy(mout)
            mo['value'] = '%s%d%s' % (basename, i, mo['suffix'])
            mo['index'] = i
            outputs.append(mo)

    with open(filename, 'w') as f:
        json.dump(md, f, ensure_ascii=False)