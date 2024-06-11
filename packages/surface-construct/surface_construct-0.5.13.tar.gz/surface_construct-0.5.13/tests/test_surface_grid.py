import ase.io
import matplotlib.pyplot as plt
import numpy as np
from ase.visualize import view
from sklearn.decomposition import PCA

from surface_construct.surface_grid import SurfaceGrid

atoms = ase.io.read('ru_0001_POSCAR')
# atoms = ase.io.read('In2O3_011.cif')
sg = SurfaceGrid(atoms, interval=0.2)
sg.gridize()
sg.vectorize()

energy_file = 'energy.dat'
with open(energy_file, 'r+') as f:
    content = f.readlines()

points = []
values = []
for l in content[1:]:
    x1, y1, z1, x2, y2, z2, e = list(map(float, l.split()[1:]))
    values.append(e)
    points.append([(x1 + x2) / 2.0, (y1 + y2) / 2.0, (z1 + z2) / 2.0])
points = np.asarray(points)
values = np.asarray(values)

sg.set_energy(points, values, ignore_z=True)

sg.plot_energy()
sg.plot_sigma()

points_sample = sg.grid_sample()

view(sg.atoms + ase.Atoms(symbols=['X'] * len(points_sample), positions=points_sample))
