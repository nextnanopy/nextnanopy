import unittest
import nextnanopy.outputs as outputs
from nextnanopy.utils.datasets import default_unit
from os.path import join
import os

folder_nnp = os.path.join('tests', 'datafiles', 'nextnano++')
folder_nn3 = os.path.join('tests', 'datafiles', 'nextnano3')
folder_negf = os.path.join('tests', 'datafiles', 'nextnano.NEGF')
folder_msb = os.path.join('tests', 'datafiles', 'nextnano.MSB')


class TestOutputs_nnp(unittest.TestCase):

    def test_dat(self):
        df = outputs.DataFile(join(folder_nnp, 'bandedges_1d.dat'), product='nextnano++')
        self.assertEqual(len(df.coords.keys()), 1)
        self.assertEqual(df.coords['x'].name, 'x')
        self.assertEqual(df.coords['x'].unit, 'nm')
        self.assertEqual(df.coords['x'].value.size, 548)
        self.assertEqual(len(df.variables.keys()), 4)
        self.assertEqual(df.variables['Gamma'].name, 'Gamma')
        self.assertEqual(df.variables['Gamma'].unit, 'eV')
        self.assertEqual(df.variables['Gamma'].value.size, 548)
        self.assertEqual(df.metadata['ndim'], 1)
        self.assertEqual(df.metadata['dkeys'], [0])

        df = outputs.DataFile(join(folder_nnp, 'wf_occupation_1d.dat'), product='nextnano++')
        self.assertEqual(len(df.coords.keys()), 0)
        self.assertEqual(len(df.variables.keys()), 2)
        self.assertEqual(df.variables['no.'].name, 'no.')
        self.assertEqual(df.variables['no.'].unit, default_unit)
        self.assertEqual(df.variables['no.'].value.size, 10)
        self.assertEqual(df.variables['Occupation'].name, 'Occupation')
        self.assertEqual(df.variables['Occupation'].unit, 'electrons/cm^2')
        self.assertEqual(df.variables['Occupation'].value.size, 10)
        self.assertEqual(df.metadata['ndim'], 0)
        self.assertEqual(df.metadata['dkeys'], [])

    def test_avs(self):
        df = outputs.DataFile(join(folder_nnp, 'bandedges_2d.fld'), product='nextnano++')
        self.assertEqual(len(df.coords.keys()), 2)
        self.assertEqual(list(df.coords.keys()), ['x', 'y'])
        self.assertEqual(df.coords['x'].unit, 'nm')
        self.assertEqual(df.coords['x'].value.size, 164)
        self.assertEqual(df.coords['x'].dim, 0)
        self.assertEqual(df.coords['y'].unit, 'nm')
        self.assertEqual(df.coords['y'].value.size, 79)
        self.assertEqual(df.coords['y'].dim, 1)
        self.assertEqual(len(df.variables.keys()), 2)
        self.assertEqual(df.variables['Gamma'].name, 'Gamma')
        self.assertEqual(df.variables['Gamma'].unit, 'eV')
        self.assertEqual(df.variables['Gamma'].value.shape, (164, 79))
        self.assertEqual(df.metadata['ndim'], 2)
        self.assertEqual(df.metadata['dims'], [164, 79])
        self.assertEqual(df.metadata['field'], 'rectilinear')

    def test_avs3D(self):
        df = outputs.DataFile(join(folder_nnp, 'potential.fld'), product='nextnano++')
        self.assertEqual(len(df.coords.keys()), 3)
        self.assertEqual(list(df.coords.keys()), ['x', 'y', 'z'])
        self.assertEqual(df.coords['x'].unit, 'nm')
        self.assertEqual(df.coords['x'].value.size, 11)
        self.assertEqual(df.coords['x'].dim, 0)
        self.assertEqual(df.coords['y'].unit, 'nm')
        self.assertEqual(df.coords['y'].value.size, 11)
        self.assertEqual(df.coords['y'].dim, 1)
        self.assertEqual(df.coords['z'].unit, 'nm')
        self.assertEqual(df.coords['z'].value.size, 76)
        self.assertEqual(df.coords['z'].dim, 2)
        self.assertEqual(len(df.variables.keys()), 1)
        self.assertEqual(df.variables['potential'].name, 'potential')
        self.assertEqual(df.variables['potential'].unit, default_unit)
        self.assertEqual(df.variables['potential'].value.shape, (11, 11, 76))
        self.assertEqual(df.metadata['ndim'], 3)
        self.assertEqual(df.metadata['dims'], [11, 11, 76])
        self.assertEqual(df.metadata['field'], 'rectilinear')

    def test_vtr_potential(self):
        df = outputs.DataFile(join(folder_nnp, 'potential.vtr'), product='nextnano++')

        self.assertEqual(len(df.coords.keys()), 3)
        self.assertEqual(list(df.coords.keys()), ['x', 'y', 'z'])
        self.assertEqual(df.coords['x'].unit, default_unit)
        self.assertEqual(df.coords['x'].value.size, 11)
        self.assertEqual(df.coords['x'].dim, 0)
        self.assertEqual(df.coords['y'].unit, default_unit)
        self.assertEqual(df.coords['y'].value.size, 11)
        self.assertEqual(df.coords['y'].dim, 1)
        self.assertEqual(df.coords['z'].unit, default_unit)
        self.assertEqual(df.coords['z'].value.size, 76)
        self.assertEqual(df.coords['z'].dim, 2)
        self.assertEqual(len(df.variables.keys()), 1)
        self.assertEqual(df.variables['potential'].name, 'potential')
        self.assertEqual(df.variables['potential'].unit, default_unit)
        self.assertEqual(df.variables['potential'].value.shape, (11, 11, 76))
        self.assertEqual(df.metadata, {})

    def test_vtr_bandedges(self):
        df = outputs.DataFile(join(folder_nnp, 'bandedges.vtr'), product='nextnano++')

        self.assertEqual(len(df.coords.keys()), 3)
        self.assertEqual(list(df.coords.keys()), ['x', 'y', 'z'])
        self.assertEqual(df.coords['x'].unit, default_unit)
        self.assertEqual(df.coords['x'].value.size, 11)
        self.assertEqual(df.coords['x'].dim, 0)
        self.assertEqual(df.coords['y'].unit, default_unit)
        self.assertEqual(df.coords['y'].value.size, 11)
        self.assertEqual(df.coords['y'].dim, 1)
        self.assertEqual(df.coords['z'].unit, default_unit)
        self.assertEqual(df.coords['z'].value.size, 76)
        self.assertEqual(df.coords['z'].dim, 2)
        self.assertEqual(len(df.variables.keys()), 4)
        self.assertEqual(df.variables['Gamma'].name, 'Gamma')
        self.assertEqual(df.variables['Gamma'].unit, 'eV')
        self.assertEqual(df.variables['Gamma'].value.shape, (11, 11, 76))
        self.assertEqual(df.metadata, {})

    def test_txt(self):
        df = outputs.DataFile(join(folder_nnp, 'variables_input.txt'), product='nextnano++')
        self.assertEqual(len(df.coords.keys()), 0)
        self.assertEqual(len(df.variables.keys()), 3)
        self.assertEqual(df.variables['var_1'].name, 'var_1')
        self.assertEqual(df.variables['var_1'].unit, default_unit)
        self.assertEqual(df.variables['var_1'].value, -47.5)
        self.assertEqual(df.variables['var_2'].value, 75)
        self.assertEqual(df.variables['string'].value, '"hello"')

        df = outputs.DataFile(join(folder_nnp, 'variables_database.txt'), product='nextnano++')
        self.assertEqual(len(df.coords.keys()), 0)
        self.assertEqual(len(df.variables.keys()), 0)

        files = ['simulation_database.txt', 'simulation_info.txt', 'simulation_input.txt']
        for file in files:
            self.assertRaises(NotImplementedError, outputs.DataFile, join(folder_nnp, file), 'nextnano++')

    def test_rest(self):
        files = ['example.log', 'example.in']
        for file in files:
            self.assertRaises(NotImplementedError, outputs.DataFile, join(folder_nnp, file), 'nextnano++')


class TestOutputs_nn3(unittest.TestCase):

    def test_dat(self):
        df = outputs.DataFile(join(folder_nn3, 'bandedges_1d.dat'), product='nextnano3')
        self.assertEqual(len(df.coords.keys()), 1)
        self.assertEqual(df.coords['position'].name, 'position')
        self.assertEqual(df.coords['position'].unit, 'nm')
        self.assertEqual(df.coords['position'].value.size, 258)
        self.assertEqual(len(df.variables.keys()), 6)
        self.assertEqual(df.variables['Gamma_bandedge'].name, 'Gamma_bandedge')
        self.assertEqual(df.variables['Gamma_bandedge'].unit, 'eV')
        self.assertEqual(df.variables['Gamma_bandedge'].value.size, 258)
        self.assertEqual(df.metadata['ndim'], 1)
        self.assertEqual(df.metadata['dkeys'], [0])

        df = outputs.DataFile(join(folder_nn3, 'wf_shift_1d.dat'), product='nextnano3')
        self.assertEqual(len(df.coords.keys()), 1)
        self.assertEqual(len(df.variables.keys()), 10)
        self.assertEqual(df.coords['position'].name, 'position')
        self.assertEqual(df.coords['position'].unit, 'nm')
        self.assertEqual(df.coords['position'].value.size, 121)
        self.assertEqual(df.variables['psi^2_1'].name, 'psi^2_1')
        self.assertEqual(df.variables['psi^2_1'].unit, default_unit)
        self.assertEqual(df.variables['psi^2_1'].value.size, 121)
        self.assertEqual(df.metadata['ndim'], 1)
        self.assertEqual(df.metadata['dkeys'], [0])

        df = outputs.DataFile(join(folder_nn3, 'bandedges_2d_cut.dat'), product='nextnano3')
        self.assertEqual(len(df.coords.keys()), 1)
        self.assertEqual(df.coords['position'].name, 'position')
        self.assertEqual(df.coords['position'].unit, 'nm')
        self.assertEqual(df.coords['position'].value.size, 258)
        self.assertEqual(len(df.variables.keys()), 6)
        self.assertEqual(df.variables['Gamma_bandedge'].name, 'Gamma_bandedge')
        self.assertEqual(df.variables['Gamma_bandedge'].unit, 'eV')
        self.assertEqual(df.variables['Gamma_bandedge'].value.size, 258)
        self.assertEqual(df.metadata['ndim'], 1)
        self.assertEqual(df.metadata['dkeys'], [0])

    def test_avs1D(self):
        df = outputs.DataFile(join(folder_nn3, 'cb_Gamma_avs.fld'), product='nextnano3')
        self.assertEqual(len(df.coords.keys()), 1)
        self.assertEqual(list(df.coords.keys()), ['x'])
        self.assertEqual(df.coords['x'].unit, 'nm')
        self.assertEqual(df.coords['x'].value.size, 105)
        self.assertEqual(df.coords['x'].dim, 0)
        self.assertEqual(len(df.variables.keys()), 1)
        self.assertEqual(df.variables['cb_Gamma'].name, 'cb_Gamma')
        self.assertEqual(df.variables['cb_Gamma'].unit, 'eV')
        self.assertEqual(df.variables['cb_Gamma'].value.shape, (105,))
        self.assertEqual(df.metadata['ndim'], 1)
        self.assertEqual(df.metadata['dims'], [105])
        self.assertEqual(df.metadata['field'], 'rectilinear')

    def test_avs(self):
        df = outputs.DataFile(join(folder_nn3, 'bandedges_2d.fld'), product='nextnano3')
        self.assertEqual(len(df.coords.keys()), 2)
        self.assertEqual(list(df.coords.keys()), ['x', 'y'])
        self.assertEqual(df.coords['x'].unit, 'nm')
        self.assertEqual(df.coords['x'].value.size, 258)
        self.assertEqual(df.coords['x'].dim, 0)
        self.assertEqual(df.coords['y'].unit, 'nm')
        self.assertEqual(df.coords['y'].value.size, 11)
        self.assertEqual(df.coords['y'].dim, 1)
        self.assertEqual(len(df.variables.keys()), 6)
        self.assertEqual(df.variables['Gamma_bandedge'].name, 'Gamma_bandedge')
        self.assertEqual(df.variables['Gamma_bandedge'].unit, 'eV')
        self.assertEqual(df.variables['Gamma_bandedge'].value.shape, (258, 11))
        self.assertEqual(df.metadata['ndim'], 2)
        self.assertEqual(df.metadata['dims'], [258, 11])
        self.assertEqual(df.metadata['field'], 'rectilinear')

    def test_avs2D(self):
        df = outputs.DataFile(join(folder_nn3, '2Dcb1_sg1_deg1_psi_ev001.fld'), product='nextnano3')
        self.assertEqual(len(df.coords.keys()), 2)
        self.assertEqual(list(df.coords.keys()), ['x', 'y'])
        self.assertEqual(df.coords['x'].unit, 'nm')
        self.assertEqual(df.coords['x'].value.size, 61)
        self.assertEqual(df.coords['x'].dim, 0)
        self.assertEqual(df.coords['y'].unit, 'nm')
        self.assertEqual(df.coords['y'].value.size, 61)
        self.assertEqual(df.coords['y'].dim, 1)
        self.assertEqual(df.variables[0], df.variables['psi_real'])
        self.assertEqual(df.variables[0].name, 'psi_real')
        self.assertEqual(df.variables[0].unit, 'nm^-1')
        self.assertEqual(df.variables[0].value.shape, (61, 61))
        self.assertEqual(df.variables[1], df.variables['psi_imag'])
        self.assertEqual(df.variables[1].name, 'psi_imag')
        self.assertEqual(df.variables[1].unit, 'nm^-1')
        self.assertEqual(df.variables[1].value.shape, (61, 61))
        self.assertEqual(df.metadata['ndim'], 2)
        self.assertEqual(df.metadata['dims'], [61, 61])
        self.assertEqual(df.metadata['field'], 'rectilinear')

    def test_avs3D(self):
        df = outputs.DataFile(join(folder_nn3, '3Dcb1_sg1_deg1_psi_squared_ev001.fld'), product='nextnano3')
        self.assertEqual(len(df.coords.keys()), 3)
        self.assertEqual(list(df.coords.keys()), ['x', 'y', 'z'])
        self.assertEqual(df.coords['x'].unit, 'nm')
        self.assertEqual(df.coords['x'].value.size, 19)
        self.assertEqual(df.coords['x'].dim, 0)
        self.assertEqual(df.coords['y'].unit, 'nm')
        self.assertEqual(df.coords['y'].value.size, 19)
        self.assertEqual(df.coords['y'].dim, 1)
        self.assertEqual(df.coords['z'].unit, 'nm')
        self.assertEqual(df.coords['z'].value.size, 9)
        self.assertEqual(df.coords['z'].dim, 2)
        self.assertEqual(len(df.variables.keys()), 1)
        self.assertEqual(df.variables['psi_squared'].name, 'psi_squared')
        self.assertEqual(df.variables['psi_squared'].unit, 'nm^-3')
        self.assertEqual(df.variables[0].value.shape, (19, 19, 9))
        self.assertEqual(df.metadata['ndim'], 3)
        self.assertEqual(df.metadata['dims'], [19, 19, 9])
        self.assertEqual(df.metadata['field'], 'rectilinear')

    def test_vtr_LocalDOS(self):
        df = outputs.DataFile(join(folder_nn3, 'LocalDOS_sg1_deg1_Lead1.vtr'), product='nextnano3')

        self.assertEqual(len(df.coords.keys()), 2)
        self.assertEqual(list(df.coords.keys()), ['x', 'y'])
        self.assertEqual(df.coords['x'].unit, default_unit)
        self.assertEqual(df.coords['x'].value.size, 51)
        self.assertEqual(df.coords['x'].dim, 0)
        self.assertEqual(df.coords['y'].unit, default_unit)
        self.assertEqual(df.coords['y'].value.size, 101)
        self.assertEqual(df.coords['y'].dim, 1)
        self.assertEqual(len(df.variables.keys()), 1)
        self.assertEqual(df.variables['LocalDOS_sg1_deg1_Lead1'].name, 'LocalDOS_sg1_deg1_Lead1')
        self.assertEqual(df.variables['LocalDOS_sg1_deg1_Lead1'].unit, 'nm^-1eV^-1')
        self.assertEqual(df.variables['LocalDOS_sg1_deg1_Lead1'].value.shape, (51, 101))
        self.assertEqual(df.metadata, {})

    def test_vtr_2Dcb1(self):
        df = outputs.DataFile(join(folder_nn3, '2Dcb1_sg1_deg1_psi_ev001.vtr'), product='nextnano3')

        self.assertEqual(len(df.coords.keys()), 2)
        self.assertEqual(list(df.coords.keys()), ['x', 'y'])
        self.assertEqual(df.coords['x'].unit, default_unit)
        self.assertEqual(df.coords['x'].value.size, 61)
        self.assertEqual(df.coords['x'].dim, 0)
        self.assertEqual(df.coords['y'].unit, default_unit)
        self.assertEqual(df.coords['y'].value.size, 61)
        self.assertEqual(df.coords['y'].dim, 1)
        self.assertEqual(len(df.variables.keys()), 2)
        self.assertEqual(df.variables[0], df.variables['psi_real'])
        self.assertEqual(df.variables[0].name, 'psi_real')
        self.assertEqual(df.variables[0].unit, 'nm^-1')
        self.assertEqual(df.variables[0].value.shape, (61, 61))
        self.assertEqual(df.variables[1], df.variables['psi_imag'])
        self.assertEqual(df.variables[1].name, 'psi_imag')
        self.assertEqual(df.variables[1].unit, 'nm^-1')
        self.assertEqual(df.variables[1].value.shape, (61, 61))
        self.assertEqual(df.metadata, {})

    def test_vtr_3Dcb1(self):
        df = outputs.DataFile(join(folder_nn3, '3Dcb1_sg1_deg1_psi_squared_ev001.vtr'), product='nextnano3')

        self.assertEqual(len(df.coords.keys()), 3)
        self.assertEqual(list(df.coords.keys()), ['x', 'y', 'z'])
        self.assertEqual(df.coords['x'].unit, default_unit)
        self.assertEqual(df.coords['x'].value.size, 19)
        self.assertEqual(df.coords['x'].dim, 0)
        self.assertEqual(df.coords['y'].unit, default_unit)
        self.assertEqual(df.coords['y'].value.size, 19)
        self.assertEqual(df.coords['y'].dim, 1)
        self.assertEqual(df.coords['z'].unit, default_unit)
        self.assertEqual(df.coords['z'].value.size, 9)
        self.assertEqual(df.coords['z'].dim, 2)
        self.assertEqual(len(df.variables.keys()), 1)
        self.assertEqual(df.variables['psi_squared'].name, 'psi_squared')
        self.assertEqual(df.variables['psi_squared'].unit, 'nm^-3')
        self.assertEqual(df.variables['psi_squared'].value.shape, (19, 19, 9))
        self.assertEqual(df.metadata, {})

    def test_txt(self):
        df = outputs.DataFile(join(folder_nn3, 'variables_input.txt'), product='nextnano3')
        self.assertEqual(len(df.coords.keys()), 0)
        self.assertEqual(len(df.variables.keys()), 3)
        self.assertEqual(df.variables['var_1'].name, 'var_1')
        self.assertEqual(df.variables['var_1'].unit, default_unit)
        self.assertEqual(df.variables['var_1'].value, -47.5)
        self.assertEqual(df.variables['var_2'].value, 75)
        self.assertEqual(df.variables['string'].value, '"hello"')

        df = outputs.DataFile(join(folder_nn3, 'variables_database.txt'), product='nextnano3')
        self.assertEqual(len(df.coords.keys()), 0)
        self.assertEqual(len(df.variables.keys()), 0)

    def test_rest(self):
        files = ['example.log', 'example.in']
        for file in files:
            self.assertRaises(NotImplementedError, outputs.DataFile, join(folder_nnp, file), 'nextnano3')


class TestOutputs_negf(unittest.TestCase):

    def test_dat(self):
        df = outputs.DataFile(join(folder_negf, 'ReducedRealSpaceModes.dat'), product='nextnano.NEGF')
        self.assertEqual(len(df.coords.keys()), 1)
        self.assertEqual(df.coords['Position'], df.coords[0])
        self.assertEqual(df.coords['Position'].name, 'Position')
        self.assertEqual(df.coords['Position'].unit, 'nm')
        self.assertEqual(df.coords['Position'].value.size, 608)
        self.assertEqual(len(df.variables.keys()), 19)
        self.assertEqual(df.variables['Conduction_BandEdge'], df.variables[0])
        self.assertEqual(df.variables['Conduction_BandEdge'].name, 'Conduction_BandEdge')
        self.assertEqual(df.variables['Conduction_BandEdge'].unit, 'eV')
        self.assertEqual(df.variables['Conduction_BandEdge'].value.size, 608)
        self.assertEqual(df.variables['Psi_1 (lev.1 per.0)'], df.variables[1])
        self.assertEqual(df.variables['Psi_1 (lev.1 per.0)'].name, 'Psi_1 (lev.1 per.0)')
        self.assertEqual(df.variables['Psi_1 (lev.1 per.0)'].unit, 'a.u.')
        self.assertEqual(df.variables['Psi_1 (lev.1 per.0)'].value.size, 608)
        self.assertEqual(df.metadata['ndim'], 1)
        self.assertEqual(df.metadata['dkeys'], [0])

        df = outputs.DataFile(join(folder_negf, 'E_p (Kane energy).dat'), product='nextnano.NEGF')
        self.assertEqual(df.coords['Position'], df.coords[0])
        self.assertEqual(df.coords['Position'].name, 'Position')
        self.assertEqual(df.coords['Position'].unit, 'nm')
        self.assertEqual(df.coords['Position'].value.size, 203)
        self.assertEqual(len(df.variables.keys()), 1)
        self.assertEqual(df.variables['E_p'].name, 'E_p')
        self.assertEqual(df.variables['E_p'].unit, default_unit)
        self.assertEqual(df.variables['E_p'].value.size, 203)
        self.assertEqual(df.metadata['ndim'], 1)
        self.assertEqual(df.metadata['dkeys'], [0])

    def test_vtr(self):
        df = outputs.DataFile(join(folder_negf, 'CarrierDensity_energy_resolved.vtr'), product='nextnano.NEGF')
        self.assertEqual(len(df.coords.keys()), 2)
        self.assertEqual(list(df.coords.keys()), ['x', 'y'])
        self.assertEqual(df.coords['x'].unit, default_unit)
        self.assertEqual(df.coords['x'].value.size, 176)
        self.assertEqual(df.coords['x'].dim, 0)
        self.assertEqual(df.coords['y'].unit, default_unit)
        self.assertEqual(df.coords['y'].value.size, 82)
        self.assertEqual(df.coords['y'].dim, 1)
        self.assertEqual(len(df.variables.keys()), 1)
        self.assertEqual(df.variables['Carrier density'].name, 'Carrier density')
        self.assertEqual(df.variables['Carrier density'].unit, 'cm^-3 eV^-1')
        self.assertEqual(df.variables['Carrier density'].value.shape, (176, 82))
        self.assertEqual(df.metadata, {})

    def test_rest(self):
        files = ['example.log', 'example.in', 'Material_Database.xml', 'Convergence.txt']
        for file in files:
            self.assertRaises(NotImplementedError, outputs.DataFile, join(folder_negf, file), 'nextnano.NEGF')


class TestOutputs_msb(unittest.TestCase):

    def test_dat(self):
        df = outputs.DataFile(join(folder_msb, 'BandEdge_conduction.dat'), product='nextnano.MSB')
        self.assertEqual(len(df.coords.keys()), 1)
        self.assertEqual(df.coords['Position'].name, 'Position')
        self.assertEqual(df.coords['Position'].unit, 'nm')
        self.assertEqual(df.coords['Position'].value.size, 100)
        self.assertEqual(len(df.variables.keys()), 1)
        self.assertEqual(df.variables['Conduction Band Edge'].name, 'Conduction Band Edge')
        self.assertEqual(df.variables['Conduction Band Edge'].unit, 'eV')
        self.assertEqual(df.variables['Conduction Band Edge'].value.size, 100)
        self.assertEqual(df.metadata['ndim'], 1)
        self.assertEqual(df.metadata['dkeys'], [0])

    def test_vtr(self):
        df = outputs.DataFile(join(folder_msb, 'DOS_Lead_Source_position_resolved.vtr'), product='nextnano.MSB')
        self.assertEqual(len(df.coords.keys()), 2)
        self.assertEqual(list(df.coords.keys()), ['x', 'y'])
        self.assertEqual(df.coords['x'].unit, default_unit)
        self.assertEqual(df.coords['x'].value.size, 50)
        self.assertEqual(df.coords['x'].dim, 0)
        self.assertEqual(df.coords['y'].unit, default_unit)
        self.assertEqual(df.coords['y'].value.size, 401)
        self.assertEqual(df.coords['y'].dim, 1)
        self.assertEqual(len(df.variables.keys()), 1)
        self.assertEqual(df.variables[0], df.variables['Density of States (Source)'])
        self.assertEqual(df.variables[0].name, 'Density of States (Source)')
        self.assertEqual(df.variables[0].unit, '1/eV/nm')
        self.assertEqual(df.variables[0].value.shape, (50, 401))
        self.assertEqual(df.metadata, {})


class TestOutput(unittest.TestCase):

    def test_data(self):
        df = outputs.DataFile(join(folder_nnp, 'bandedges_2d.fld'), product='nextnano++')
        self.assertEqual(len(df.data), len(df.coords) + len(df.variables))
        for key, value in df.coords.items():
            self.assertEqual(df.data[key], value)
        for key, value in df.variables.items():
            self.assertEqual(df.data[key], value)

    def test_access_by_index(self):
        df = outputs.DataFile(join(folder_nnp, 'bandedges_2d.fld'), product='nextnano++')
        for key, value in df.coords.items():
            self.assertEqual(df[key], value)
        for key, value in df.variables.items():
            self.assertEqual(df[key], value)

    def test_for_loop(self):
        df = outputs.DataFile(join(folder_nnp, 'bandedges_2d.fld'), product='nextnano++')
        for i, dfi in enumerate(df):
            self.assertEqual(df.data[i], dfi)


if __name__ == '__main__':
    unittest.main()
