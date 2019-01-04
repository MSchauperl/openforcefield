# =============================================================================================
# MODULE DOCSTRING
# =============================================================================================

"""
Direct simulation layer.

Authors
-------
* Simon Boothroyd <simon.boothroyd@choderalab.org>
"""


# =============================================================================================
# GLOBAL IMPORTS
# =============================================================================================

import pickle

from openforcefield.typing.engines.smirnoff import ForceField
from openforcefield.properties.estimator.layers.base import register_calculation_layer, PropertyCalculationLayer


# =============================================================================================
# Reweighting Layer
# =============================================================================================

@register_calculation_layer()
class ReweightingLayer(PropertyCalculationLayer):
    """Attempts to calculate properties by reweighting existing
    simulation data.
    """

    @staticmethod
    def perform_calculation(backend, data_model, existing_data, callback, synchronous=False):

        parameter_set = ForceField([])

        with open(data_model.parameter_set_path, 'rb') as file:
            parameter_set.__setstate__(pickle.load(file))

        reweighting_futures = []

        for physical_property in data_model.queued_properties:

            reweighting_future = backend.submit_task(ReweightingLayer.perform_reweighting,
                                                     physical_property,
                                                     parameter_set)

            reweighting_futures.append(reweighting_future)

        PropertyCalculationLayer._await_results(backend, data_model, callback, reweighting_futures, synchronous)

    @staticmethod
    def perform_reweighting(physical_property, parameter_set):
        """A placeholder method that would be used to attempt
        to reweight previous calculations to yield the desired
        property.
        """

        # For now the return tuple indicates that the reweighting
        # was not sufficiently accurate to estimate the property (False)
        # and simply returns the property back to be passed to the next layer.
        return False, physical_property