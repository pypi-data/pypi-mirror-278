import ase
import numpy as np
from ase.visualize import view
from surface_construct.systematic_opt import SystematicOpt

atoms = ase.Atoms('CO', positions=[[0, 0, 0], [0, 0, 1.4]])
coordinate = {
    'phi_x': {'indices': [0, 1], 'values': [0, 90]},
    'theta': {'indices': [0, 1], 'values': [0, 90]},
}

sysopt = SystematicOpt(atoms, coordinate)
A = sysopt.rotate_theta(0, 1, 0)
A1 = sysopt.rotate_phi_x(0, 1, 90)
atomslst = sysopt.get_initial_atomslst()
pass