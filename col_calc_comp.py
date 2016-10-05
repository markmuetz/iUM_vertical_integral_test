# coding: utf-8
from collections import OrderedDict as odict

import pylab as plt
import numpy as np

import omnium as om


def find_cube(cubes, section_item):
    section, item = section_item
    for cube in cubes:
	cube_stash = cube.attributes['STASH']
	if cube_stash.section == section and cube_stash.item == item:
	    return cube


if __name__ == '__main__':
    config = om.ConfigChecker.load_config()
    process_classes = om.get_process_classes()
    dag = om.NodeDAG(config, process_classes)
    proc_eng = om.ProcessEngine(False, config, process_classes, dag)
    stash = om.Stash()

    atmos5nodes = dag.get_nodes('atmos.000.5.nc')
    atmos5s = [proc_eng.load(n) for n in atmos5nodes]
    [stash.rename_unknown_cubes(cbs, True) for cbs in atmos5s]
    mwvi = process_classes['mass_weighted_vertical_integral'](config, None)
    mwvi.load_modules()

    for atmos5 in atmos5s:
	rhoR2 = find_cube(atmos5, (0, 253))

	qvars = odict()
	qvars['q'] = find_cube(atmos5, (0, 10))
	qvars['qcl'] = find_cube(atmos5, (0, 254))
	qvars['qcf'] = find_cube(atmos5, (0, 12))
	#qvars['qcf2'] = find_cube(atmos5, (0, 12))
	#qvars['qrain'] = find_cube(atmos5, (0, 272))
	#qvars['qgraup'] = find_cube(atmos5, (0, 273))

	q_col_vars = odict()
	for name, qvar in qvars.items():
	    print('MWVI: ' + name)
	    mwvi.data = [(rhoR2, qvar)]
	    q_col_vars[name + '_col_calc'] = mwvi.run()

	qcl_col_diag = find_cube(atmos5, (30, 405))
	qcf_col_diag = find_cube(atmos5, (30, 406))

	print(np.allclose(q_col_vars['qcl_col_calc'].data, qcl_col_diag.data))
	print(np.allclose(q_col_vars['qcf_col_calc'].data, qcf_col_diag.data))
