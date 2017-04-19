"""
@name   control.py
@desc   


@author Joshua Paul A. Chan (@joshpaulchan)
"""

from embed.config import SystemConfig

class System(object):
    """
    Generic system controller class
    """
    
    INSTRUMENTS = {
        'FAN'   : [],
        'MOIST' : [],
        'LIGHT' : []
    }

    # maps sensor input values to an output controller
    # i.e. temp -> fan + heating element 
    S_I_MAP = {
        'MOIST-M'   : 'MOIST',
        'MOIST-F'   : 'MOIST',
        'MOIST-L'   : 'MOIST',
        'TEMP-M'    : 'FAN',
    }

    
    def __init__(self, config=None):
        pass
        
    def prepare(self, key, val):
        """
        """
        # avg
        
        # 
        
        raise NotImplementedError
    
    def predict(self, inputs):
        """
        Predicts the instrument outputs given sensor inputs
        
        @param      dict        inputs      dictionary of inputs
        @return     dict        dict of instrument -> param matching
        """
        raise NotImplementedError
    
class NaiveSystem(System):
    """
    
    """
    
    def __init__(self, config=None, io_map=None):
        super().__init__(config=config)
        
        self.io_map = io_map
    
    def resolve(self, input_name, val):
        """
        Predict whether
        """
        
        return 1
    
    def predict(self, inputs):
        """
        
        Given sensor readings as input dict, will use the the configured rules
        and the io_map to produce an output dictionary of
        
        """
        outputs = {}
        
        # irrigation - handled by scheduling
        # outputs['pump/enable'] = 1
        
        # climate control
        avg_temp = 0
        if avg_temp < 60:
            # too cold
            print("System is running too cold.")
            outputs['fan/enable'] = 1
            outputs['heat/enable'] = 1
        elif avg_temp > 80:
            # too hot
            print("System is running too hot.")
            outputs['fan/enable'] = 1
        else:
            # just right
            pass
        
        # lighting - handled by scheduling
        # outputs['lights/enable'] = 1
        # outputs['lights/red/enable'] = 1
        # outputs['lights/green/enable'] = 1
        # outputs['lights/blue/enable'] = 1
        
        return outputs

class HerbertSystem(System):
    """
    """
    pass
