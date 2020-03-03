import numpy as np
import numpy.testing as npt
import unittest
import wisdem.towerse.tower as tow
import openmdao.api as om
from wisdem.commonse import gravity as g
import copy

class TestTowerSE(unittest.TestCase):
    def setUp(self):
        self.inputs = {}
        self.outputs = {}
        self.discrete_inputs = {}
        self.discrete_outputs = {}

        
    def testDiscYAML_Land_1Material(self):

        # Test land based, 1 material
        self.inputs['tower_s'] = np.linspace(0, 1, 5)
        self.inputs['tower_layer_thickness'] = 0.25*np.ones((1,4))
        self.inputs['tower_height'] = 1e2
        self.inputs['tower_outer_diameter_in'] = 8*np.ones(5)
        self.inputs['tower_outfitting_factor'] = 1.1
        self.discrete_inputs['tower_layer_materials'] = ['steel']
        self.inputs['monopile_s'] = np.empty(0)
        self.inputs['monopile_layer_thickness'] = np.empty((0,0))
        self.inputs['monopile_height'] = 0.
        self.inputs['monopile_outer_diameter_in'] = np.empty(0)
        self.inputs['monopile_outfitting_factor'] = 0.0
        self.discrete_inputs['monopile_layer_materials'] = ['']
        self.inputs['E_mat'] = 1e9*np.ones((1,3))
        self.inputs['G_mat'] = 1e8*np.ones((1,3))
        self.inputs['sigma_y_mat'] = np.array([1e7])
        self.inputs['rho_mat'] = np.array([1e4])
        self.inputs['unit_cost_mat'] = np.array([1e1])
        self.discrete_inputs['material_names'] = ['steel']
        myobj = tow.DiscretizationYAML(n_height_tower=5, n_height_monopile=0,
                                       n_layers_tower=1, n_layers_monopile=0, n_mat=1)
        myobj.compute(self.inputs, self.outputs, self.discrete_inputs, self.discrete_outputs)
        
        npt.assert_equal(self.outputs['tower_section_height'], 25.*np.ones(4))
        npt.assert_equal(self.outputs['tower_outer_diameter'], self.inputs['tower_outer_diameter_in'])
        npt.assert_equal(self.outputs['tower_wall_thickness'], 0.25*np.ones(4))
        npt.assert_equal(self.outputs['outfitting_factor'], 1.1*np.ones(4))
        npt.assert_equal(self.outputs['E'],             1e9*np.ones(4))
        npt.assert_equal(self.outputs['G'],             1e8*np.ones(4))
        npt.assert_equal(self.outputs['sigma_y'],       1e7*np.ones(4))
        npt.assert_equal(self.outputs['rho'],           1e4*np.ones(4))
        npt.assert_equal(self.outputs['unit_cost'],     1e1*np.ones(4))
        
    def testDiscYAML_Land_2Materials(self):
        # Test land based, 2 materials
        self.inputs['tower_s'] = np.linspace(0, 1, 5)
        self.inputs['tower_layer_thickness'] = np.array([[0.25, 0.25, 0.0, 0.0],[0.0, 0.0, 0.1, 0.1]])
        self.inputs['tower_height'] = 1e2
        self.inputs['tower_outer_diameter_in'] = 8*np.ones(5)
        self.inputs['tower_outfitting_factor'] = 1.1
        self.discrete_inputs['tower_layer_materials'] = ['steel','other']
        self.inputs['monopile_s'] = np.empty(0)
        self.inputs['monopile_layer_thickness'] = np.empty((0,0))
        self.inputs['monopile_height'] = 0.
        self.inputs['monopile_outer_diameter_in'] = np.empty(0)
        self.inputs['monopile_outfitting_factor'] = 0.0
        self.discrete_inputs['monopile_layer_materials'] = ['']
        self.inputs['E_mat'] = 1e9*np.vstack( (np.ones((1,3)), 2*np.ones((1,3)) ) )
        self.inputs['G_mat'] = 1e8*np.vstack( (np.ones((1,3)), 2*np.ones((1,3)) ) )
        self.inputs['sigma_y_mat'] = np.array([1e7, 2e7])
        self.inputs['rho_mat'] = np.array([1e4, 2e4])
        self.inputs['unit_cost_mat'] = np.array([1e1, 2e1])
        self.discrete_inputs['material_names'] = ['steel','other']
        myobj = tow.DiscretizationYAML(n_height_tower=5, n_height_monopile=0,
                                       n_layers_tower=1, n_layers_monopile=0, n_mat=2)
        myobj.compute(self.inputs, self.outputs, self.discrete_inputs, self.discrete_outputs)
        
        npt.assert_equal(self.outputs['tower_section_height'], 25.*np.ones(4))
        npt.assert_equal(self.outputs['tower_outer_diameter'], self.inputs['tower_outer_diameter_in'])
        npt.assert_equal(self.outputs['tower_wall_thickness'], np.array([0.25, 0.25, 0.1, 0.1]))
        npt.assert_equal(self.outputs['outfitting_factor'], 1.1*np.ones(4))
        npt.assert_equal(self.outputs['E'],             1e9*np.array([1,1,2,2]))
        npt.assert_equal(self.outputs['G'],             1e8*np.array([1,1,2,2]))
        npt.assert_equal(self.outputs['sigma_y'],       1e7*np.array([1,1,2,2]))
        npt.assert_equal(self.outputs['rho'],           1e4*np.array([1,1,2,2]))
        npt.assert_equal(self.outputs['unit_cost'],     1e1*np.array([1,1,2,2]))
        
    def testDiscYAML_Monopile_1Material(self):
        self.inputs['tower_s'] = np.linspace(0, 1, 5)
        self.inputs['tower_layer_thickness'] = 0.25*np.ones((1,4))
        self.inputs['tower_height'] = 1e2
        self.inputs['tower_outer_diameter_in'] = 8*np.ones(5)
        self.inputs['tower_outfitting_factor'] = 1.1
        self.discrete_inputs['tower_layer_materials'] = ['steel']
        self.inputs['monopile_s'] = np.linspace(0, 1, 5)
        self.inputs['monopile_layer_thickness'] = 0.5*np.ones((1,4))
        self.inputs['monopile_height'] = 50.
        self.inputs['monopile_outer_diameter_in'] = 10*np.ones(5)
        self.inputs['monopile_outer_diameter_in'][-1] = 8
        self.inputs['monopile_outfitting_factor'] = 1.2
        self.discrete_inputs['monopile_layer_materials'] = ['steel']
        self.inputs['E_mat'] = 1e9*np.ones((1,3))
        self.inputs['G_mat'] = 1e8*np.ones((1,3))
        self.inputs['sigma_y_mat'] = np.array([1e7])
        self.inputs['rho_mat'] = np.array([1e4])
        self.inputs['unit_cost_mat'] = np.array([1e1])
        self.discrete_inputs['material_names'] = ['steel']
        myobj = tow.DiscretizationYAML(n_height_tower=5, n_height_monopile=5,
                                       n_layers_tower=1, n_layers_monopile=1, n_mat=1)
        myobj.compute(self.inputs, self.outputs, self.discrete_inputs, self.discrete_outputs)
        
        npt.assert_equal(self.outputs['tower_section_height'], np.r_[12.5*np.ones(4), 25*np.ones(4)])
        npt.assert_equal(self.outputs['tower_outer_diameter'], np.r_[10*np.ones(4), 8*np.ones(5)])
        npt.assert_equal(self.outputs['tower_wall_thickness'], np.r_[0.5*np.ones(4), 0.25*np.ones(4)])
        npt.assert_equal(self.outputs['outfitting_factor'], np.r_[1.2*np.ones(4), 1.1*np.ones(4)])
        npt.assert_equal(self.outputs['E'],             1e9*np.ones(8))
        npt.assert_equal(self.outputs['G'],             1e8*np.ones(8))
        npt.assert_equal(self.outputs['sigma_y'],       1e7*np.ones(8))
        npt.assert_equal(self.outputs['rho'],           1e4*np.ones(8))
        npt.assert_equal(self.outputs['unit_cost'],     1e1*np.ones(8))
        
    def testDiscYAML_Monopile_DifferentMaterials(self):
        self.inputs['tower_s'] = np.linspace(0, 1, 5)
        self.inputs['tower_layer_thickness'] = 0.25*np.ones((1,4))
        self.inputs['tower_height'] = 1e2
        self.inputs['tower_outer_diameter_in'] = 8*np.ones(5)
        self.inputs['tower_outfitting_factor'] = 1.1
        self.discrete_inputs['tower_layer_materials'] = ['steel']
        self.inputs['monopile_s'] = np.linspace(0, 1, 5)
        self.inputs['monopile_layer_thickness'] = 0.5*np.ones((1,4))
        self.inputs['monopile_height'] = 50.
        self.inputs['monopile_outer_diameter_in'] = 10*np.ones(5)
        self.inputs['monopile_outer_diameter_in'][-1] = 8
        self.inputs['monopile_outfitting_factor'] = 1.2
        self.discrete_inputs['monopile_layer_materials'] = ['other']
        self.inputs['E_mat'] = 1e9*np.vstack( (np.ones((1,3)), 2*np.ones((1,3)) ) )
        self.inputs['G_mat'] = 1e8*np.vstack( (np.ones((1,3)), 2*np.ones((1,3)) ) )
        self.inputs['sigma_y_mat'] = np.array([1e7, 2e7])
        self.inputs['rho_mat'] = np.array([1e4, 2e4])
        self.inputs['unit_cost_mat'] = np.array([1e1, 2e1])
        self.discrete_inputs['material_names'] = ['steel','other']
        myobj = tow.DiscretizationYAML(n_height_tower=5, n_height_monopile=5,
                                       n_layers_tower=1, n_layers_monopile=1, n_mat=2)
        myobj.compute(self.inputs, self.outputs, self.discrete_inputs, self.discrete_outputs)
        
        npt.assert_equal(self.outputs['tower_section_height'], np.r_[12.5*np.ones(4), 25*np.ones(4)])
        npt.assert_equal(self.outputs['tower_outer_diameter'], np.r_[10*np.ones(4), 8*np.ones(5)])
        npt.assert_equal(self.outputs['tower_wall_thickness'], np.r_[0.5*np.ones(4), 0.25*np.ones(4)])
        npt.assert_equal(self.outputs['outfitting_factor'], np.r_[1.2*np.ones(4), 1.1*np.ones(4)])
        npt.assert_equal(self.outputs['E'],             1e9*np.r_[2*np.ones(4), np.ones(4)])
        npt.assert_equal(self.outputs['G'],             1e8*np.r_[2*np.ones(4), np.ones(4)])
        npt.assert_equal(self.outputs['sigma_y'],       1e7*np.r_[2*np.ones(4), np.ones(4)])
        npt.assert_equal(self.outputs['rho'],           1e4*np.r_[2*np.ones(4), np.ones(4)])
        npt.assert_equal(self.outputs['unit_cost'],     1e1*np.r_[2*np.ones(4), np.ones(4)])
        
    def testDiscYAML_Bad_Inputs(self):
        self.inputs['tower_s'] = np.linspace(0, 1, 5)
        self.inputs['tower_layer_thickness'] = 0.25*np.ones((1,4))
        self.inputs['tower_height'] = 1e2
        self.inputs['tower_outer_diameter_in'] = 8*np.ones(5)
        self.inputs['tower_outfitting_factor'] = 1.1
        self.discrete_inputs['tower_layer_materials'] = ['steel']
        self.inputs['monopile_s'] = np.empty(0)
        self.inputs['monopile_layer_thickness'] = np.empty((0,0))
        self.inputs['monopile_height'] = 0.
        self.inputs['monopile_outer_diameter_in'] = np.empty(0)
        self.inputs['monopile_outfitting_factor'] = 0.0
        self.discrete_inputs['monopile_layer_materials'] = ['']
        self.inputs['E_mat'] = 1e9*np.ones((1,3))
        self.inputs['G_mat'] = 1e8*np.ones((1,3))
        self.inputs['sigma_y_mat'] = np.array([1e7])
        self.inputs['rho_mat'] = np.array([1e4])
        self.inputs['unit_cost_mat'] = np.array([1e1])
        self.discrete_inputs['material_names'] = ['steel']
        myobj = tow.DiscretizationYAML(n_height_tower=5, n_height_monopile=0,
                                       n_layers_tower=1, n_layers_monopile=0, n_mat=1)

        try:
            self.inputs['tower_layer_thickness'][0,-1] = 0.0
            myobj.compute(self.inputs, self.outputs, self.discrete_inputs, self.discrete_outputs)
            self.assertTrue(False) # Shouldn't get here
        except ValueError:
            self.assertTrue(True)

        try:
            self.inputs['tower_layer_thickness'][0,-1] = 0.25
            self.inputs['tower_outer_diameter_in'][-1] = -1.0
            myobj.compute(self.inputs, self.outputs, self.discrete_inputs, self.discrete_outputs)
            self.assertTrue(False) # Shouldn't get here
        except ValueError:
            self.assertTrue(True)

        try:
            self.inputs['tower_layer_thickness'][0,-1] = 0.25
            self.inputs['tower_outer_diameter_in'][-1] = 8.0
            self.inputs['tower_s'][-1] = self.inputs['tower_s'][-2]
            myobj.compute(self.inputs, self.outputs, self.discrete_inputs, self.discrete_outputs)
            self.assertTrue(False) # Shouldn't get here
        except ValueError:
            self.assertTrue(True)
        
        
    def testMonopileFoundation(self):
        # Test Land
        self.inputs['suctionpile_depth'] = 0.0
        self.inputs['foundation_height'] = 0.0
        myobj = tow.MonopileFoundation(monopile=False)
        myobj.compute(self.inputs, self.outputs)
        npt.assert_equal(self.outputs['z_start'], self.inputs['foundation_height'])

        # Test Land with bad suctionpile input
        self.inputs['suctionpile_depth'] = 10.0
        myobj.compute(self.inputs, self.outputs)
        npt.assert_equal(self.outputs['z_start'], self.inputs['foundation_height'])
        
        # Test monopile with pile
        self.inputs['suctionpile_depth'] = 10.0
        self.inputs['foundation_height'] = -30.0
        myobj = tow.MonopileFoundation(monopile=True)
        myobj.compute(self.inputs, self.outputs)
        npt.assert_equal(self.outputs['z_start'], -40.0)

        self.inputs['suctionpile_depth'] = -10.0
        myobj.compute(self.inputs, self.outputs)
        npt.assert_equal(self.outputs['z_start'], -40.0)
        
        # Test monopile with gravity
        self.inputs['suctionpile_depth'] = 0.0
        myobj = tow.MonopileFoundation(monopile=True)
        myobj.compute(self.inputs, self.outputs)
        npt.assert_equal(self.outputs['z_start'], self.inputs['foundation_height'])

        
    def testTowerDisc(self):
        # Test Land
        self.inputs['hub_height'] = 100.0
        self.inputs['z_param'] = np.array([0., 40., 80.])
        self.inputs['z_full'] = np.linspace(0., 80., 7)
        self.inputs['rho'] = 1e3 * np.ones(2)
        self.inputs['outfitting_factor'] = 1.1 * np.ones(2)
        self.inputs['unit_cost'] = 5.0 * np.ones(2)
        myobj = tow.TowerDiscretization(n_height=3)
        myobj.compute(self.inputs, self.outputs)
        self.assertEqual(self.outputs['height_constraint'], 20.0)
        

        
    def testTowerMass(self):

        self.inputs['z_full'] = np.array([-50., -30, 0.0, 40., 80.])
        self.inputs['cylinder_mass'] = 1e3*np.ones(4)
        self.inputs['cylinder_cost'] = 1e5
        self.inputs['cylinder_center_of_mass'] = 10.0
        self.inputs['cylinder_section_center_of_mass'] = self.inputs['z_full'][:-1] + 0.5*np.diff(self.inputs['z_full'])
        self.inputs['cylinder_I_base'] = 1e4*np.r_[np.ones(3), np.zeros(3)]
        self.inputs['transition_piece_height'] = 20.0
        self.inputs['transition_piece_mass'] = 1e2
        self.inputs['gravity_foundation_mass'] = 1e2
        self.inputs['foundation_height'] = -30.
        
        myobj = tow.TowerMass(n_height=5)
        myobj.compute(self.inputs, self.outputs)
        
        self.assertEqual(self.outputs['tower_raw_cost'], self.inputs['cylinder_cost'])
        npt.assert_equal(self.outputs['tower_I_base'], self.inputs['cylinder_I_base'])
        self.assertEqual(self.outputs['tower_center_of_mass'], (4*1e3*10.0 + 1e2*20.0 + 1e2*-30.0)/(4*1e3+2e2) )
        npt.assert_equal(self.outputs['tower_section_center_of_mass'], self.inputs['cylinder_section_center_of_mass'])
        self.assertEqual(self.outputs['monopile_mass'], 1e3*2.5 + 2*1e2)
        self.assertEqual(self.outputs['monopile_cost'], self.inputs['cylinder_cost']*2.5/4.0)
        self.assertEqual(self.outputs['monopile_length'], 70.0)
        self.assertEqual(self.outputs['tower_mass'], 1e3*(4-2.5))


    def testPreFrame(self):
        
        # Test Land 
        self.inputs['z_param'] = 10. * np.array([0., 3., 6.])
        self.inputs['z_full'] = 10. * np.arange(0,7)
        self.inputs['d_full'] = 6. * np.ones(self.inputs['z_full'].shape)
        self.inputs['mass'] = 1e5
        self.inputs['mI']   = np.r_[1e5, 1e5, 2e5, np.zeros(3)]
        self.inputs['mrho'] = np.array([-3., 0.0, 1.0])
        self.inputs['transition_piece_mass'] = 0.0
        self.inputs['transition_piece_height'] = 0.0
        self.inputs['gravity_foundation_mass'] = 0.0
        self.inputs['foundation_height'] = 0.0
        self.inputs['rna_F'] = 1e5*np.array([2., 3., 4.,])
        self.inputs['rna_M'] = 1e6*np.array([2., 3., 4.,])
        self.inputs['k_monopile'] = np.zeros(6)
        self.inputs['E'] = 1e9 * np.ones(2)
        self.inputs['G'] = 1e8 * np.ones(2)
        self.inputs['sigma_y'] = 1e8 * np.ones(2)

        myobj = tow.TowerPreFrame(n_height=3, monopile=False)
        myobj.compute(self.inputs, self.outputs)

        npt.assert_equal(self.outputs['kidx'], np.array([0]))
        npt.assert_equal(self.outputs['kx'], np.array([1e16]))
        npt.assert_equal(self.outputs['ky'], np.array([1e16]))
        npt.assert_equal(self.outputs['kz'], np.array([1e16]))
        npt.assert_equal(self.outputs['ktx'], np.array([1e16]))
        npt.assert_equal(self.outputs['kty'], np.array([1e16]))
        npt.assert_equal(self.outputs['ktz'], np.array([1e16]))

        npt.assert_equal(self.outputs['midx'], np.array([6, 0, 0]))
        npt.assert_equal(self.outputs['m'], np.array([1e5, 0, 0]))
        npt.assert_equal(self.outputs['mrhox'], np.array([-3., 0., 0.]))
        npt.assert_equal(self.outputs['mrhoy'], np.array([0., 0., 0.]))
        npt.assert_equal(self.outputs['mrhoz'], np.array([1., 0., 0.]))
        npt.assert_equal(self.outputs['mIxx'], np.array([1e5, 0., 0.]))
        npt.assert_equal(self.outputs['mIyy'], np.array([1e5, 0., 0.]))
        npt.assert_equal(self.outputs['mIzz'], np.array([2e5, 0., 0.]))
        npt.assert_equal(self.outputs['mIxy'], np.zeros(3))
        npt.assert_equal(self.outputs['mIxz'], np.zeros(3))
        npt.assert_equal(self.outputs['mIyz'], np.zeros(3))

        npt.assert_equal(self.outputs['plidx'], np.array([6]))
        npt.assert_equal(self.outputs['Fx'], np.array([2e5]))
        npt.assert_equal(self.outputs['Fy'], np.array([3e5]))
        npt.assert_equal(self.outputs['Fz'], np.array([4e5]))
        npt.assert_equal(self.outputs['Mxx'], np.array([2e6]))
        npt.assert_equal(self.outputs['Myy'], np.array([3e6]))
        npt.assert_equal(self.outputs['Mzz'], np.array([4e6]))

        # Test Monopile 
        self.inputs['z_full'] = 10. * np.arange(-6,7)
        self.inputs['d_full'] = 6. * np.ones(self.inputs['z_full'].shape)
        self.inputs['transition_piece_mass'] = 1e3
        self.inputs['transition_piece_height'] = 10.0
        self.inputs['gravity_foundation_mass'] = 1e4
        self.inputs['foundation_height'] = -30.0
        self.inputs['rna_F'] = 1e5*np.array([2., 3., 4.,])
        self.inputs['rna_M'] = 1e6*np.array([2., 3., 4.,])
        self.inputs['k_monopile'] = 20. + np.arange(6)

        myobj = tow.TowerPreFrame(n_height=5, monopile=True)
        myobj.compute(self.inputs, self.outputs)

        npt.assert_equal(self.outputs['kidx'], np.array([0]))
        npt.assert_equal(self.outputs['kx'], 20.*np.ones(1))
        npt.assert_equal(self.outputs['ky'], 22.*np.ones(1))
        npt.assert_equal(self.outputs['kz'], 24.*np.ones(1))
        npt.assert_equal(self.outputs['ktx'], 21.*np.ones(1))
        npt.assert_equal(self.outputs['kty'], 23.*np.ones(1))
        npt.assert_equal(self.outputs['ktz'], 25.*np.ones(1))

        npt.assert_equal(self.outputs['midx'], np.array([12, 7, 0]))
        npt.assert_equal(self.outputs['m'], np.array([1e5, 1e3, 1e4]))
        npt.assert_equal(self.outputs['mrhox'], np.array([-3., 0., 0.]))
        npt.assert_equal(self.outputs['mrhoy'], np.array([0., 0., 0.]))
        npt.assert_equal(self.outputs['mrhoz'], np.array([1., 0., 0.]))
        npt.assert_equal(self.outputs['mIxx'], np.array([1e5, 1e3*9*0.5, 1e4*9*0.25]))
        npt.assert_equal(self.outputs['mIyy'], np.array([1e5, 1e3*9*0.5, 1e4*9*0.25]))
        npt.assert_equal(self.outputs['mIzz'], np.array([2e5, 1e3*9, 1e4*9*0.5]))
        npt.assert_equal(self.outputs['mIxy'], np.zeros(3))
        npt.assert_equal(self.outputs['mIxz'], np.zeros(3))
        npt.assert_equal(self.outputs['mIyz'], np.zeros(3))

        npt.assert_equal(self.outputs['plidx'], np.array([12]))
        npt.assert_equal(self.outputs['Fx'], np.array([2e5]))
        npt.assert_equal(self.outputs['Fy'], np.array([3e5]))
        npt.assert_equal(self.outputs['Fz'], np.array([4e5]))
        npt.assert_equal(self.outputs['Mxx'], np.array([2e6]))
        npt.assert_equal(self.outputs['Myy'], np.array([3e6]))
        npt.assert_equal(self.outputs['Mzz'], np.array([4e6]))


    def testProblemLand(self):

        # Store analysis options
        analysis_options = {}
        analysis_options['tower'] = {}
        analysis_options['tower']['buckling_length'] = 20.0
        analysis_options['tower']['monopile'] = False
        analysis_options['tower']['n_height'] = 3
        analysis_options['tower']['wind'] = 'PowerWind'
        analysis_options['tower']['nLC'] = 1

        analysis_options['tower']['gamma_f'] = 1.0
        analysis_options['tower']['gamma_m'] = 1.0
        analysis_options['tower']['gamma_n'] = 1.0
        analysis_options['tower']['gamma_b'] = 1.0
        analysis_options['tower']['gamma_fatigue'] = 1.0

        analysis_options['tower']['frame3dd']            = {}
        analysis_options['tower']['frame3dd']['DC']      = 80.0
        analysis_options['tower']['frame3dd']['shear']   = True
        analysis_options['tower']['frame3dd']['geom']    = True
        analysis_options['tower']['frame3dd']['dx']      = 5.0
        analysis_options['tower']['frame3dd']['nM']      = 2
        analysis_options['tower']['frame3dd']['Mmethod'] = 1
        analysis_options['tower']['frame3dd']['lump']    = 0
        analysis_options['tower']['frame3dd']['tol']     = 1e-9
        analysis_options['tower']['frame3dd']['shift']   = 0.0
        analysis_options['tower']['frame3dd']['add_gravity'] = True

        prob = om.Problem()
        prob.model = tow.TowerSE(analysis_options=analysis_options, topLevelFlag=True)
        prob.setup()

        prob['hub_height'] = 80.0
        prob['foundation_height'] = 0.0
        prob['transition_piece_height'] = 0.0
        prob['transition_piece_mass'] = 0.0
        prob['gravity_foundation_mass'] = 0.0
        prob['tower_section_height'] = 40.0*np.ones(2)
        prob['tower_outer_diameter'] = 10.0*np.ones(3)
        prob['tower_wall_thickness'] = 0.1*np.ones(2)
        prob['outfitting_factor'] = 1.0
        prob['yaw'] = 0.0
        prob['suctionpile_depth'] = 0.0
        prob['G_soil'] = 1e7
        prob['nu_soil'] = 0.5
        prob['E'] = 1e9
        prob['G'] = 1e8
        prob['rho'] = 1e4
        prob['sigma_y'] = 1e8
        prob['rna_mass'] = 2e5
        prob['rna_I'] = np.r_[1e5, 1e5, 2e5, np.zeros(3)]
        prob['rna_cg'] = np.array([-3., 0.0, 1.0])
        prob['wind_reference_height'] = 80.0
        prob['wind_z0'] = 0.0
        prob['cd_usr'] = -1.
        prob['rho_air'] = 1.225
        prob['mu_air'] = 1.7934e-5
        prob['shearExp'] = 0.2
        prob['rho_water'] = 1025.0
        prob['mu_water'] = 1.3351e-3
        prob['beta_wind'] = prob['beta_wave'] = 0.0
        prob['hsig_wave'] = 0.0
        prob['Tsig_wave'] = 1e3
        prob['min_d_to_t'] = 120.0
        prob['max_taper'] = 0.2
        prob['wind.Uref'] = 15.0
        prob['pre.rna_F'] = 1e3*np.array([2., 3., 4.,])
        prob['pre.rna_M'] = 1e4*np.array([2., 3., 4.,])
        prob.run_model()

        # All other tests from above
        mass_dens = 1e4*(5.**2-4.9**2)*np.pi
        npt.assert_equal(prob['z_start'], 0.0)
        npt.assert_equal(prob['z_param'], np.array([0., 40., 80.]))
        
        self.assertEqual(prob['height_constraint'], 0.0)
        self.assertEqual(prob['tower_raw_cost'], prob['cm.cost'])
        npt.assert_equal(prob['tower_I_base'], prob['cm.I_base'])
        npt.assert_almost_equal(prob['tower_center_of_mass'], 40.0)
        npt.assert_equal(prob['tower_section_center_of_mass'], prob['cm.section_center_of_mass'])
        self.assertEqual(prob['monopile_mass'], 0.0)
        self.assertEqual(prob['monopile_cost'], 0.0)
        self.assertEqual(prob['monopile_length'], 0.0)
        npt.assert_almost_equal(prob['tower_mass'], mass_dens*80.0)

        npt.assert_equal(prob['pre.kidx'], np.array([0], dtype=np.int_))
        npt.assert_equal(prob['pre.kx'], np.array([1e16]))
        npt.assert_equal(prob['pre.ky'], np.array([1e16]))
        npt.assert_equal(prob['pre.kz'], np.array([1e16]))
        npt.assert_equal(prob['pre.ktx'], np.array([1e16]))
        npt.assert_equal(prob['pre.kty'], np.array([1e16]))
        npt.assert_equal(prob['pre.ktz'], np.array([1e16]))

        npt.assert_equal(prob['pre.midx'], np.array([6, 0, 0]))
        npt.assert_equal(prob['pre.m'], np.array([2e5, 0, 0]))
        npt.assert_equal(prob['pre.mrhox'], np.array([-3., 0., 0.]))
        npt.assert_equal(prob['pre.mrhoy'], np.array([0., 0., 0.]))
        npt.assert_equal(prob['pre.mrhoz'], np.array([1., 0., 0.]))
        npt.assert_equal(prob['pre.mIxx'], np.array([1e5, 0., 0.]))
        npt.assert_equal(prob['pre.mIyy'], np.array([1e5, 0., 0.]))
        npt.assert_equal(prob['pre.mIzz'], np.array([2e5, 0., 0.]))
        npt.assert_equal(prob['pre.mIxy'], np.zeros(3))
        npt.assert_equal(prob['pre.mIxz'], np.zeros(3))
        npt.assert_equal(prob['pre.mIyz'], np.zeros(3))

        npt.assert_equal(prob['pre.plidx'], np.array([6]))
        npt.assert_equal(prob['pre.Fx'], np.array([2e3]))
        npt.assert_equal(prob['pre.Fy'], np.array([3e3]))
        npt.assert_equal(prob['pre.Fz'], np.array([4e3]))
        npt.assert_equal(prob['pre.Mxx'], np.array([2e4]))
        npt.assert_equal(prob['pre.Myy'], np.array([3e4]))
        npt.assert_equal(prob['pre.Mzz'], np.array([4e4]))



    def testProblemFixedPile(self):

        # Store analysis options
        analysis_options = {}
        analysis_options['tower'] = {}
        analysis_options['tower']['buckling_length'] = 20.0
        analysis_options['tower']['monopile'] = True
        analysis_options['tower']['n_height'] = 5
        analysis_options['tower']['wind'] = 'PowerWind'
        analysis_options['tower']['nLC'] = 1

        analysis_options['tower']['gamma_f'] = 1.0
        analysis_options['tower']['gamma_m'] = 1.0
        analysis_options['tower']['gamma_n'] = 1.0
        analysis_options['tower']['gamma_b'] = 1.0
        analysis_options['tower']['gamma_fatigue'] = 1.0

        analysis_options['tower']['frame3dd']            = {}
        analysis_options['tower']['frame3dd']['DC']      = 80.0
        analysis_options['tower']['frame3dd']['shear']   = True
        analysis_options['tower']['frame3dd']['geom']    = True
        analysis_options['tower']['frame3dd']['dx']      = 5.0
        analysis_options['tower']['frame3dd']['nM']      = 2
        analysis_options['tower']['frame3dd']['Mmethod'] = 1
        analysis_options['tower']['frame3dd']['lump']    = 0
        analysis_options['tower']['frame3dd']['tol']     = 1e-9
        analysis_options['tower']['frame3dd']['shift']   = 0.0
        analysis_options['tower']['frame3dd']['add_gravity'] = True

        prob = om.Problem()
        prob.model = tow.TowerSE(analysis_options=analysis_options, topLevelFlag=True)
        prob.setup()

        prob['hub_height'] = 80.0
        prob['foundation_height'] = -30.0
        prob['transition_piece_height'] = 15.0
        prob['transition_piece_mass'] = 1e2
        prob['gravity_foundation_mass'] = 1e4
        prob['tower_section_height'] = np.r_[15.0, 30.0*np.ones(3)]
        prob['tower_outer_diameter'] = 10.0*np.ones(5)
        prob['tower_wall_thickness'] = 0.1*np.ones(4)
        prob['suctionpile_depth'] = 15.0
        prob['outfitting_factor'] = 1.0
        prob['yaw'] = 0.0
        prob['G_soil'] = 1e7
        prob['nu_soil'] = 0.5
        prob['E'] = 1e9*np.ones(4)
        prob['G'] = 1e8*np.ones(4)
        prob['rho'] = 1e4*np.ones(4)
        prob['sigma_y'] = 1e8*np.ones(4)
        prob['rna_mass'] = 2e5
        prob['rna_I'] = np.r_[1e5, 1e5, 2e5, np.zeros(3)]
        prob['rna_cg'] = np.array([-3., 0.0, 1.0])
        prob['wind_reference_height'] = 80.0
        prob['wind_z0'] = 0.0
        prob['cd_usr'] = -1.
        prob['rho_air'] = 1.225
        prob['mu_air'] = 1.7934e-5
        prob['shearExp'] = 0.2
        prob['rho_water'] = 1025.0
        prob['mu_water'] = 1.3351e-3
        prob['beta_wind'] = prob['beta_wave'] = 0.0
        prob['hsig_wave'] = 0.0
        prob['Tsig_wave'] = 1e3
        prob['min_d_to_t'] = 120.0
        prob['max_taper'] = 0.2
        prob['wind.Uref'] = 15.0
        prob['pre.rna_F'] = 1e3*np.array([2., 3., 4.,])
        prob['pre.rna_M'] = 1e4*np.array([2., 3., 4.,])
        prob.run_model()


        # All other tests from above
        mass_dens = 1e4*(5.**2-4.9**2)*np.pi
        npt.assert_equal(prob['z_start'], -45.0)
        npt.assert_equal(prob['z_param'], np.array([-45., -30., 0., 30., 60.]))
        
        self.assertEqual(prob['height_constraint'], 20.0)
        self.assertEqual(prob['tower_raw_cost'], (40./105.)*prob['cm.cost'])
        npt.assert_equal(prob['tower_I_base'], prob['cm.I_base'])
        npt.assert_almost_equal(prob['tower_center_of_mass'], (7.5*mass_dens*105.+15.*1e2+1e4*-30.)/(mass_dens*105+1e2+1e4))
        npt.assert_equal(prob['tower_section_center_of_mass'], prob['cm.section_center_of_mass'])
        self.assertEqual(prob['monopile_cost'], (60./105.)*prob['cm.cost'])
        self.assertEqual(prob['monopile_length'], 60.0)
        npt.assert_almost_equal(prob['monopile_mass'], mass_dens*60.0 + 1e2+1e4)
        npt.assert_almost_equal(prob['tower_mass'], mass_dens*45.0)

        npt.assert_equal(prob['pre.kidx'], np.array([0], dtype=np.int_))
        npt.assert_array_less(prob['pre.kx'], 1e16)
        npt.assert_array_less(prob['pre.ky'], 1e16)
        npt.assert_array_less(prob['pre.kz'], 1e16)
        npt.assert_array_less(prob['pre.ktx'], 1e16)
        npt.assert_array_less(prob['pre.kty'], 1e16)
        npt.assert_array_less(prob['pre.ktz'], 1e16)
        npt.assert_array_less(0.0, prob['pre.kx'])
        npt.assert_array_less(0.0, prob['pre.ky'])
        npt.assert_array_less(0.0, prob['pre.kz'])
        npt.assert_array_less(0.0, prob['pre.ktx'])
        npt.assert_array_less(0.0, prob['pre.kty'])
        npt.assert_array_less(0.0, prob['pre.ktz'])

        npt.assert_equal(prob['pre.midx'], np.array([12, 7, 0]))
        npt.assert_equal(prob['pre.m'], np.array([2e5, 1e2, 1e4]))
        npt.assert_equal(prob['pre.mrhox'], np.array([-3., 0., 0.]))
        npt.assert_equal(prob['pre.mrhoy'], np.array([0., 0., 0.]))
        npt.assert_equal(prob['pre.mrhoz'], np.array([1., 0., 0.]))
        npt.assert_equal(prob['pre.mIxx'], np.array([1e5, 1e2*25*0.5, 1e4*25*0.25]))
        npt.assert_equal(prob['pre.mIyy'], np.array([1e5, 1e2*25*0.5, 1e4*25*0.25]))
        npt.assert_equal(prob['pre.mIzz'], np.array([2e5, 1e2*25, 1e4*25*0.5]))
        npt.assert_equal(prob['pre.mIxy'], np.zeros(3))
        npt.assert_equal(prob['pre.mIxz'], np.zeros(3))
        npt.assert_equal(prob['pre.mIyz'], np.zeros(3))

        npt.assert_equal(prob['pre.plidx'], np.array([12]))
        npt.assert_equal(prob['pre.Fx'], np.array([2e3]))
        npt.assert_equal(prob['pre.Fy'], np.array([3e3]))
        npt.assert_equal(prob['pre.Fz'], np.array([4e3]))
        npt.assert_equal(prob['pre.Mxx'], np.array([2e4]))
        npt.assert_equal(prob['pre.Myy'], np.array([3e4]))
        npt.assert_equal(prob['pre.Mzz'], np.array([4e4]))
        
        

    def testAddedMassForces(self):

        # Store analysis options
        analysis_options = {}
        analysis_options['tower'] = {}
        analysis_options['tower']['buckling_length'] = 20.0
        analysis_options['tower']['monopile'] = True
        analysis_options['tower']['n_height'] = 5
        analysis_options['tower']['wind'] = 'PowerWind'
        analysis_options['tower']['nLC'] = 1

        analysis_options['tower']['gamma_f'] = 1.0
        analysis_options['tower']['gamma_m'] = 1.0
        analysis_options['tower']['gamma_n'] = 1.0
        analysis_options['tower']['gamma_b'] = 1.0
        analysis_options['tower']['gamma_fatigue'] = 1.0

        analysis_options['tower']['frame3dd']            = {}
        analysis_options['tower']['frame3dd']['DC']      = 80.0
        analysis_options['tower']['frame3dd']['shear']   = True
        analysis_options['tower']['frame3dd']['geom']    = True
        analysis_options['tower']['frame3dd']['dx']      = 5.0
        analysis_options['tower']['frame3dd']['nM']      = 2
        analysis_options['tower']['frame3dd']['Mmethod'] = 1
        analysis_options['tower']['frame3dd']['lump']    = 0
        analysis_options['tower']['frame3dd']['tol']     = 1e-9
        analysis_options['tower']['frame3dd']['shift']   = 0.0
        analysis_options['tower']['frame3dd']['add_gravity'] = True

        prob = om.Problem()
        prob.model = tow.TowerSE(analysis_options=analysis_options, topLevelFlag=True)
        prob.setup()

        prob['hub_height'] = 80.0
        prob['foundation_height'] = -30.0
        prob['transition_piece_height'] = 15.0
        prob['transition_piece_mass'] = 0.0
        prob['gravity_foundation_mass'] = 0.0
        prob['tower_section_height'] = np.r_[15.0, 30.0*np.ones(3)]
        prob['tower_outer_diameter'] = 10.0*np.ones(5)
        prob['tower_wall_thickness'] = 0.1*np.ones(4)
        prob['suctionpile_depth'] = 15.0
        prob['outfitting_factor'] = 1.0
        prob['yaw'] = 0.0
        prob['G_soil'] = 1e7
        prob['nu_soil'] = 0.5
        prob['E'] = 1e9*np.ones(4)
        prob['G'] = 1e8*np.ones(4)
        prob['rho'] = 1e4*np.ones(4)
        prob['sigma_y'] = 1e8*np.ones(4)
        prob['rna_mass'] = 0.0
        prob['rna_I'] = np.r_[1e5, 1e5, 2e5, np.zeros(3)]
        prob['rna_cg'] = np.array([-3., 0.0, 1.0])
        prob['wind_reference_height'] = 80.0
        prob['wind_z0'] = 0.0
        prob['cd_usr'] = -1.
        prob['rho_air'] = 1.225
        prob['mu_air'] = 1.7934e-5
        prob['shearExp'] = 0.2
        prob['rho_water'] = 1025.0
        prob['mu_water'] = 1.3351e-3
        prob['beta_wind'] = prob['beta_wave'] = 0.0
        prob['hsig_wave'] = 0.0
        prob['Tsig_wave'] = 1e3
        prob['min_d_to_t'] = 120.0
        prob['max_taper'] = 0.2
        prob['wind.Uref'] = 15.0
        prob['pre.rna_F'] = 1e3*np.array([2., 3., 4.,])
        prob['pre.rna_M'] = 1e4*np.array([2., 3., 4.,])
        prob.run_model()

        myFz = copy.copy(prob['post.Fz'])

        prob['rna_mass'] = 1e4
        prob.run_model()
        myFz -= 1e4*g
        npt.assert_almost_equal(prob['post.Fz'], myFz)

        prob['transition_piece_mass'] = 1e2
        prob.run_model()
        myFz[:7] -= 1e2*g
        npt.assert_almost_equal(prob['post.Fz'], myFz)

        prob['gravity_foundation_mass'] = 1e3
        prob.run_model()
        #myFz[0] -= 1e3*g
        npt.assert_almost_equal(prob['post.Fz'], myFz)

        
    def testExampleRegression(self):
        # --- geometry ----
        h_param = np.diff(np.array([0.0, 43.8, 87.6]))
        d_param = np.array([6.0, 4.935, 3.87])
        t_param = 1.3*np.array([0.025, 0.021])
        z_foundation = 0.0
        theta_stress = 0.0
        yaw = 0.0
        Koutfitting = 1.07 * np.ones(2)

        # --- material props ---
        E = 210e9 * np.ones(2)
        G = 80.8e9 * np.ones(2)
        rho = 8500.0 * np.ones(2)
        sigma_y = 450.0e6 * np.ones(2)

        # --- extra mass ----
        m = np.array([285598.8])
        mIxx = 1.14930678e+08
        mIyy = 2.20354030e+07
        mIzz = 1.87597425e+07
        mIxy = 0.0
        mIxz = 5.03710467e+05
        mIyz = 0.0
        mI = np.array([mIxx, mIyy, mIzz, mIxy, mIxz, mIyz])
        mrho = np.array([-1.13197635, 0.0, 0.50875268])
        # -----------

        # --- wind ---
        wind_zref = 90.0
        wind_z0 = 0.0
        shearExp = 0.2
        cd_usr = -1.
        # ---------------

        # --- wave ---
        hmax = 0.0
        T = 1.0
        cm = 1.0
        suction_depth = 0.0
        soilG = 140e6
        soilnu = 0.4
        # ---------------

        # --- costs ---
        material_cost = 5.0
        labor_cost    = 100.0/60.0
        painting_cost = 30.0
        # ---------------

        # two load cases.  TODO: use a case iterator

        # # --- loading case 1: max Thrust ---
        wind_Uref1 = 11.73732
        Fx1 = 1284744.19620519
        Fy1 = 0.
        Fz1 = -2914124.84400512 + m*g
        Mxx1 = 3963732.76208099
        Myy1 = -2275104.79420872
        Mzz1 = -346781.68192839
        # # ---------------

        # # --- loading case 2: max wind speed ---
        wind_Uref2 = 70.0
        Fx2 = 930198.60063279
        Fy2 = 0.
        Fz2 = -2883106.12368949 + m*g
        Mxx2 = -1683669.22411597
        Myy2 = -2522475.34625363
        Mzz2 = 147301.97023764
        # # ---------------

        # Store analysis options
        analysis_options = {}
        analysis_options['tower'] = {}
        analysis_options['tower']['buckling_length'] = 30.0
        analysis_options['tower']['monopile'] = False

        # --- safety factors ---
        analysis_options['tower']['gamma_f'] = 1.35
        analysis_options['tower']['gamma_m'] = 1.3
        analysis_options['tower']['gamma_n'] = 1.0
        analysis_options['tower']['gamma_b'] = 1.1
        # ---------------

        # --- fatigue ---
        analysis_options['tower']['gamma_fatigue'] = 1.35*1.3*1.0
        life = 20.0
        # ---------------

        # -----Frame3DD------
        analysis_options['tower']['frame3dd']            = {}
        analysis_options['tower']['frame3dd']['DC']      = 80.0
        analysis_options['tower']['frame3dd']['shear']   = True
        analysis_options['tower']['frame3dd']['geom']    = True
        analysis_options['tower']['frame3dd']['dx']      = 5.0
        analysis_options['tower']['frame3dd']['nM']      = 2
        analysis_options['tower']['frame3dd']['Mmethod'] = 1
        analysis_options['tower']['frame3dd']['lump']    = 0
        analysis_options['tower']['frame3dd']['tol']     = 1e-9
        analysis_options['tower']['frame3dd']['shift']   = 0.0
        analysis_options['tower']['frame3dd']['add_gravity'] = True
        # ---------------

        # --- constraints ---
        min_d_to_t   = 120.0
        max_taper    = 0.2
        # ---------------

        analysis_options['tower']['n_height'] = len(d_param)
        analysis_options['tower']['wind'] = 'PowerWind'
        analysis_options['tower']['nLC'] = 2

        prob = om.Problem()
        prob.model = tow.TowerSE(analysis_options=analysis_options, topLevelFlag=True)
        prob.setup()

        if analysis_options['tower']['wind'] == 'PowerWind':
            prob['shearExp'] = shearExp

        # assign values to params

        # --- geometry ----
        prob['hub_height'] = h_param.sum()
        prob['foundation_height'] = 0.0
        prob['tower_section_height'] = h_param
        prob['tower_outer_diameter'] = d_param
        prob['tower_wall_thickness'] = t_param
        prob['outfitting_factor'] = Koutfitting
        prob['yaw'] = yaw
        prob['suctionpile_depth'] = suction_depth
        prob['G_soil'] = soilG
        prob['nu_soil'] = soilnu
        # --- material props ---
        prob['E'] = E
        prob['G'] = G
        prob['rho'] = rho
        prob['sigma_y'] = sigma_y

        # --- extra mass ----
        prob['rna_mass'] = m
        prob['rna_I'] = mI
        prob['rna_cg'] = mrho
        # -----------

        # --- costs ---
        prob['unit_cost'] = material_cost
        prob['labor_cost_rate']    = labor_cost
        prob['painting_cost_rate'] = painting_cost
        # -----------

        # --- wind & wave ---
        prob['wind_reference_height'] = wind_zref
        prob['wind_z0'] = wind_z0
        prob['cd_usr'] = cd_usr
        prob['rho_air'] = 1.225
        prob['mu_air'] = 1.7934e-5
        prob['rho_water'] = 1025.0
        prob['mu_water'] = 1.3351e-3
        prob['beta_wind'] = prob['beta_wave'] = 0.0
        prob['hsig_wave'] = hmax
        prob['Tsig_wave'] = T

        # --- fatigue ---
        prob['life'] = life
        # ---------------

        # --- constraints ---
        prob['min_d_to_t'] = min_d_to_t
        prob['max_taper'] = max_taper
        # ---------------

        # # --- loading case 1: max Thrust ---
        prob['wind1.Uref'] = wind_Uref1

        prob['pre1.rna_F'] = np.array([Fx1, Fy1, Fz1])
        prob['pre1.rna_M'] = np.array([Mxx1, Myy1, Mzz1])
        # # ---------------

        # # --- loading case 2: max Wind Speed ---
        prob['wind2.Uref'] = wind_Uref2

        prob['pre2.rna_F'] = np.array([Fx2, Fy2, Fz2])
        prob['pre2.rna_M' ] = np.array([Mxx2, Myy2, Mzz2])

        # # --- run ---
        prob.run_model()

        npt.assert_almost_equal(prob['z_full'], [ 0.,  14.6, 29.2, 43.8, 58.4, 73.,  87.6])
        npt.assert_almost_equal(prob['d_full'], [6.,    5.645, 5.29,  4.935, 4.58,  4.225, 3.87 ])
        npt.assert_almost_equal(prob['t_full'], [0.0325, 0.0325, 0.0325, 0.0273, 0.0273, 0.0273])
        
        npt.assert_almost_equal(prob['tower_mass'], [370541.14008246])
        npt.assert_almost_equal(prob['tower_center_of_mass'], [38.78441074])
        npt.assert_almost_equal(prob['weldability'], [-0.40192308, -0.34386447])
        npt.assert_almost_equal(prob['manufacturability'], [0.60521262, 0.60521262])
        npt.assert_almost_equal(prob['wind1.Uref'], [11.73732])
        npt.assert_almost_equal(prob['tower1.f1'], [0.33214436])
        npt.assert_almost_equal(prob['post1.top_deflection'], [0.69728181])
        npt.assert_almost_equal(prob['post1.stress'], [0.45829084, 0.41279851, 0.35017739, 0.31497515, 0.17978168, 0.12035124])
        npt.assert_almost_equal(prob['post1.global_buckling'], [0.50459926, 0.47009267, 0.42172339, 0.40495796, 0.29807777, 0.25473308])
        npt.assert_almost_equal(prob['post1.shell_buckling'], [0.32499642, 0.25914569, 0.18536257, 0.17036815, 0.06343523, 0.03259229])
        npt.assert_almost_equal(prob['wind2.Uref'], [70.])
        npt.assert_almost_equal(prob['tower2.f1'], [0.33218936])
        npt.assert_almost_equal(prob['post2.top_deflection'], [0.64374406])
        npt.assert_almost_equal(prob['post2.stress'], [0.44627896, 0.38220803, 0.30583361, 0.25654412, 0.13137214, 0.10615505])
        npt.assert_almost_equal(prob['post2.global_buckling'], [0.49412205, 0.4442257,  0.38450749, 0.35599809, 0.25784865, 0.24625576])
        npt.assert_almost_equal(prob['post2.shell_buckling'], [0.31189934, 0.22790801, 0.14712692, 0.12152703, 0.03909944, 0.02623264])
        npt.assert_almost_equal(prob['tower1.base_F'], [ 1.29980269e+06,  1.39698386e-09, -6.31005811e+06], 2)
        npt.assert_almost_equal(prob['tower1.base_M'], [ 4.14769959e+06,  1.10756769e+08, -3.46781682e+05], 0)
        npt.assert_almost_equal(prob['tower2.base_F'], [ 1.61668069e+06,  6.98491931e-10, -6.27903939e+06], 2)
        npt.assert_almost_equal(prob['tower2.base_M'], [-1.76118035e+06,  1.12568312e+08,  1.47301970e+05], 0)



    
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestTowerSE))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite())
