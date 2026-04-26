import numpy as np

# Patch for Python 3.12 removing imp module required by skfuzzy
import sys
import types
if not hasattr(sys.modules, 'imp'):
    sys.modules['imp'] = types.ModuleType('imp')
    sys.modules['imp'].reload = __import__('importlib').reload
    sys.modules['imp'].find_module = lambda *args, **kwargs: (None, None, None)

import skfuzzy as fuzz
from skfuzzy import control as ctrl

def evaluate_loyalty(lvr_val, cvr_val, arr_val, share_val):
    # Antecedents/Inputs
    lvr = ctrl.Antecedent(np.arange(0, 21, 0.1), 'lvr')
    cvr = ctrl.Antecedent(np.arange(0, 6, 0.1), 'cvr')
    arr = ctrl.Antecedent(np.arange(0, 101, 1), 'arr')
    sharing = ctrl.Antecedent(np.arange(0, 4, 0.1), 'sharing')
    
    # Consequent/Output
    loyalty = ctrl.Consequent(np.arange(0, 101, 1), 'loyalty')
    
    # Custom membership functions based on user limits
    lvr['rendah'] = fuzz.trapmf(lvr.universe, [0, 0, 2, 4])
    lvr['normal'] = fuzz.trapmf(lvr.universe, [3, 6, 6, 10])
    lvr['tinggi'] = fuzz.trapmf(lvr.universe, [8, 12, 20, 20])
    
    cvr['sepi'] = fuzz.trapmf(cvr.universe, [0, 0, 0.2, 0.5])
    cvr['aktif'] = fuzz.trapmf(cvr.universe, [0.4, 1, 1, 2])
    cvr['tinggi'] = fuzz.trapmf(cvr.universe, [1.8, 3, 5, 5])
    
    arr['drop'] = fuzz.trapmf(arr.universe, [0, 0, 15, 35])
    arr['stabil'] = fuzz.trapmf(arr.universe, [30, 45, 45, 65])
    arr['lama'] = fuzz.trapmf(arr.universe, [60, 80, 100, 100])
    
    sharing['rendah'] = fuzz.trapmf(sharing.universe, [0, 0, 0.1, 0.2])
    sharing['sedang'] = fuzz.trapmf(sharing.universe, [0.15, 0.4, 0.4, 0.8])
    sharing['tinggi'] = fuzz.trapmf(sharing.universe, [0.75, 1.5, 4, 4])
    
    loyalty['pasif'] = fuzz.trapmf(loyalty.universe, [0, 0, 20, 40])
    loyalty['aktif'] = fuzz.trapmf(loyalty.universe, [30, 50, 50, 75])
    loyalty['militan'] = fuzz.trapmf(loyalty.universe, [70, 85, 100, 100])
    
    # Rules
    rule1 = ctrl.Rule(arr['drop'] | lvr['rendah'] | cvr['sepi'] | sharing['rendah'], loyalty['pasif'])
    rule2 = ctrl.Rule(lvr['normal'] & cvr['aktif'] & arr['stabil'], loyalty['aktif'])
    rule3 = ctrl.Rule(lvr['tinggi'] & cvr['tinggi'], loyalty['militan'])
    rule4 = ctrl.Rule(arr['lama'] & sharing['tinggi'], loyalty['militan'])
    rule5 = ctrl.Rule(lvr['normal'] & arr['lama'], loyalty['aktif'])
    rule6 = ctrl.Rule(cvr['aktif'] & sharing['sedang'], loyalty['aktif'])
    rule7 = ctrl.Rule(lvr['tinggi'] & arr['stabil'], loyalty['aktif'])
    rule8 = ctrl.Rule(arr['stabil'] & cvr['tinggi'], loyalty['militan'])
    
    loyalty_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8])
    loyalty_sim = ctrl.ControlSystemSimulation(loyalty_ctrl)
    
    # Prevent values from going out of range
    loyalty_sim.input['lvr'] = max(0, min(20, lvr_val))
    loyalty_sim.input['cvr'] = max(0, min(5, cvr_val))
    loyalty_sim.input['arr'] = max(0, min(100, arr_val))
    loyalty_sim.input['sharing'] = max(0, min(3, share_val))
    
    try:
        loyalty_sim.compute()
        score = loyalty_sim.output['loyalty']
        
        # Determine Status
        status = 'Pasif'
        if score >= 70:
            status = 'Militan'
        elif score >= 40:
            status = 'Aktif'
            
        return round(score, 2), status
    except ValueError:
        # In case rules don't cover a very specific input combination perfectly
        return 0, 'Pasif'

# For testing
if __name__ == '__main__':
    print(evaluate_loyalty(10, 2.5, 70, 1))
