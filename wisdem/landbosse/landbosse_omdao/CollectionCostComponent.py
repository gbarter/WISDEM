import numpy as np

from .LandBOSSEBaseComponent import LandBOSSEBaseComponent
from wisdem.landbosse.model import ArraySystem

class CollectionCostComponent(LandBOSSEBaseComponent):
    """
    This class is an OpenMDAO component that wraps the LandBOSSE CollectionCost
    module.
    """

    def setup(self):
        # Inputs
        self.add_input('line_frequency_hz', val=60, units='Hz')
        self.add_input('turbine_rating_MW', val=2.5, units='MW')
        self.add_input('turbine_spacing_rotor_diameters', val=10)
        self.add_input('rotor_diameter_m', val=177, units='m')
        self.add_input('plant_capacity_MW', val=100, units='m')
        self.add_input('construct_duration', val=9, desc='Total project construction time (months)')

        # Discrete inputs, dataframes
        self.add_discrete_input('cable_specs', val=None)
        self.add_discrete_input('rsmeans', val=None)

        # Outputs, discrete, dataframes
        self.add_discrete_output('collection_cost_details', val=None)
        self.add_discrete_output('collection_cost_module_type_operation', val=None)

    def compute(self, inputs, outputs, discrete_inputs=None, discrete_outputs=None):
        """
        This runs the ErectionCost module using the inputs and outputs into and
        out of this module.

        Note: inputs, discrete_inputs are not dictionaries. They do support
        [] notation. inputs is of class 'openmdao.vectors.default_vector.DefaultVector'
        discrete_inputs is of class openmdao.core.component._DictValues. Other than
        [] brackets, they do not behave like dictionaries. See the following
        documentation for details.

        http://openmdao.org/twodocs/versions/latest/_srcdocs/packages/vectors/default_vector.html
        https://mdolab.github.io/OpenAeroStruct/_modules/openmdao/core/component.html

        Parameters
        ----------
        inputs : openmdao.vectors.default_vector.DefaultVector
            A dictionary-like object with NumPy arrays that hold float
            inputs. Note that since these are NumPy arrays, they
            need indexing to pull out simple float64 values.

        outputs : openmdao.vectors.default_vector.DefaultVector
            A dictionary-like object to store outputs.

        discrete_inputs : openmdao.core.component._DictValues
            A dictionary-like with the non-numeric inputs (like
            pandas.DataFrame)

        discrete_outputs : openmdao.core.component._DictValues
            A dictionary-like for non-numeric outputs (like
            pandas.DataFrame)
        """
        # Create real dictionaries to pass to the module
        input_dict = {key: inputs[key][0] for key in inputs.keys()}
        discrete_input_dict = {key: value for key, value in discrete_inputs.items()}
        master_inputs_dict = {**input_dict, **discrete_input_dict}
        master_output_dict = dict()

        # Make sure cable specs are accessible
        master_inputs_dict['cable_specs_pd'] = master_inputs_dict['cable_specs']

        # execute the module
        collection_cost = ArraySystem(input_dict=master_inputs_dict, output_dict=master_output_dict,
                                      project_name='WISDEM')
        collection_cost.run_module()

        # Print verbose outputs if needed
        if self.options['verbosity']:
            self.print_verbose_module_type_operation(type(self).__name__,
                                                     master_output_dict['collection_cost_module_type_operation'])
            self.print_verbose_details(type(self).__name__, master_output_dict['collection_cost_csv'])