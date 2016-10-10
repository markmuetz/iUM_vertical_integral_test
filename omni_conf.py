# Demonstration omni_conf.py file.
# Please replace all values.
from collections import OrderedDict as odict

settings = {
    'ignore_warnings': True,
}

computer_name = open('computer.txt').read().strip()
computers = {
    'breakeven': {
        'remote': 'rdf-comp',
        'remote_address': 'mmuetz@login.rdf.ac.uk',
        'remote_path': '/nerc/n02/n02/mmuetz/omnis/iUM_vertical_integral_test',
        'dirs': {
            'output': '/home/markmuetz/Dropbox/omni_output/iUM_vertical_integral_test/output'
        }
    },
    'nxnode': {
        'remote': 'rdf-comp',
        'remote_address': 'mmuetz@login.rdf.ac.uk',
        'remote_path': '/nerc/n02/n02/mmuetz/omnis/iUM_vertical_integral_test',
        'dirs': {
            'output': '/home/hb865130/omni_output/iUM_vertical_integral_test/output'
        }
    },
    'rdf-comp': {
        'dirs': {
            'output': '/nerc/n02/n02/mmuetz/omni_output/iUM_vertical_integral_test/output',
        }
    }
}

#expts = ['MC_on', 'MC_off']
expts = ['MC_on', 'MC_on_WET2DRY_MOD']
comp = computers['rdf-comp']
for expt in expts:
    comp['dirs']['work_' + expt] = '/nerc/n02/n02/mmuetz/um10.5_runs/4day/iUM_vertical_integral_test_{}/work'.format(expt)
    comp['dirs']['results_' + expt] = '/nerc/n02/n02/mmuetz/omni_output/iUM_vertical_integral_test/results_{}'.format(expt)

comp = computers['breakeven']
for expt in expts:
    comp['dirs']['work_' + expt] = '/home/markmuetz/omni_output/iUM_vertical_integral_test/work_{}'.format(expt)
    comp['dirs']['results_' + expt] = '/home/markmuetz/omni_output/iUM_vertical_integral_test/results_{}'.format(expt)

comp = computers['nxnode']
for expt in expts:
    comp['dirs']['work_' + expt] = '/home/hb865130/omni_output/iUM_vertical_integral_test/work_{}'.format(expt)
    comp['dirs']['results_' + expt] = '/home/hb865130/omni_output/iUM_vertical_integral_test/results_{}'.format(expt)


batches = odict(('batch{}'.format(i), {'index': i}) for i in range(4))
groups = odict()
ngroups = odict()
nodes = odict()
nnodes = odict()

for expt in expts:
    groups['pp5_' + expt] = {
	    'type': 'init',
	    'base_dir': 'work_' + expt,
	    'batch': 'batch0',
	    'filename_glob': '2000??????????/atmos/atmos.090.pp5',
	    }

    groups['nc5_' + expt] = {
        'type': 'group_process',
        'from_group': 'pp5_' + expt,
        'base_dir': 'results_' + expt,
        'batch': 'batch1',
        'process': 'convert_pp_to_nc',
    }

    base_vars = ['q', 'qcl', 'qcf', 'qrain', 'qgraup']
    base_nodes = [bv + '_mwvi' for bv in base_vars]

    groups['mwvi_' + expt] = {
        'type': 'nodes_process',
        'base_dir': 'results_' + expt,
        'batch': 'batch2',
        'nodes': [bn + '_' + expt for bn in base_nodes],
    }

    for bn, bv in zip(base_nodes, base_vars):
	nodes[bn + '_' + expt] = {
	    'type': 'from_group',
	    'from_group': 'nc5_' + expt,
	    'variable': bv,
	    'process': 'mass_weighted_vertical_integral',
	}

    groups['diag_' + expt] = {
        'type': 'nodes_process',
        'base_dir': 'results_' + expt,
        'batch': 'batch2',
        'nodes': ['Mtot_diag_' + expt, 'Mdry_diag_' + expt],
    }

    nodes['Mtot_diag_' + expt] = {
        'type': 'from_group',
        'from_group': 'nc5_' + expt,
	'variable': 'Mtot_diag',
        'process': 'get_variable',
    }

    nodes['Mdry_diag_' + expt] = {
        'type': 'from_group',
        'from_group': 'nc5_' + expt,
	'variable': 'Mdry_diag',
        'process': 'get_variable',
    }

    groups['col_totals_plot_' + expt] = {
        'type': 'nodes_process',
        'base_dir': 'output',
        'batch': 'batch3',
        'nodes': ['col_totals_plot_' + expt],
    }

    groups['col_q_plot_' + expt] = {
        'type': 'nodes_process',
        'base_dir': 'output',
        'batch': 'batch3',
        'nodes': ['col_q_plot_' + expt],
    }

    nodes['col_totals_plot_' + expt] = {
        'type': 'from_nodes',
        'from_nodes': [bn + '_' + expt for bn in base_nodes] + ['Mtot_diag_' + expt, 'Mdry_diag_' + expt],
        'process': 'plot_col_totals',
    }

    nodes['col_q_plot_' + expt] = {
        'type': 'from_nodes',
        'from_nodes': [bn + '_' + expt for bn in base_nodes],
        'process': 'plot_q_totals',
    }

variables = {
    'q': {
	'section': 0,
	'item': 10,
    },
    'qcl': {
	'section': 0,
	'item': 254,
    },
    'qcf': {
	'section': 0,
	'item': 12,
    },
    'qrain': {
	'section': 0,
	'item': 272,
    },
    'qgraup': {
	'section': 0,
	'item': 273,
    },
    'Mtot_diag': {
	'section': 30,
	'item': 404,
    },
    'Mdry_diag': {
	'section': 30,
	'item': 403,
    },
}
    
process_options = {
}
