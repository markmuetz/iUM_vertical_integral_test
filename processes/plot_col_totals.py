from collections import OrderedDict as odict
import importlib

import numpy as np

from omnium.processes import PylabProcess

OPTS = odict([(12, {182: {'l': 'Adv.', 'fmt': 'r-'}}),
             (9, {182: {'l': 'BL+cloud', 'fmt': 'r--'}}),
             (4, {182: {'l': 'LS rain', 'fmt': 'b--'}}),
             (30, {182: {'l': 'Total', 'fmt': 'k-'}})])


def find_cube(cubes, section_item):
    section, item = section_item
    for cube in cubes:
	cube_stash = cube.attributes['STASH']
	if cube_stash.section == section and cube_stash.item == item:
	    return cube


class PlotColTotals(PylabProcess):
    name = 'plot_col_totals'
    out_ext = 'png'

    def load_upstream(self):
        super(PlotColTotals, self).load_upstream()
        filenames = [n.filename(self.config) for n in self.node.from_nodes]

	qvars = self.iris.load(filenames[:-2])
	diag_data = self.iris.load(filenames[-2:])
        self.data = (qvars, diag_data)

    def run(self):
        super(PlotColTotals, self).run()
        qvars, diag_data = self.data
	Mwet_calc = qvars[0].data
	for qvar in qvars[1:]:
	    Mwet_calc += qvar.data

	Mtot_diag = find_cube(diag_data, (30, 404))
	Mdry_diag = find_cube(diag_data, (30, 403))
	Mwet_diag = Mtot_diag.data - Mdry_diag.data

        fig = self.plt.figure()

        fig.canvas.set_window_title('Mwet_diag - Mwet_calc')

        self.plt.title('Mwet_diag - Mwet_calc')

	diff = Mwet_diag[-1] - Mwet_calc[-1]
	max_min = max(np.abs(diff.min()), diff.max())
	self.plt.imshow(diff, interpolation='nearest', cmap=self.plt.cm.bwr, vmin=-max_min, vmax=max_min)
	cb = self.plt.colorbar()
	cb.set_label('(kg m$^{-2}$)')

        #self.plt.xlim((-10, 10))
        #self.plt.xlabel('(g kg$^{-1}$ day$^{-1}$)')
        #self.plt.ylabel('Height (km)')

        self.processed_data = fig
