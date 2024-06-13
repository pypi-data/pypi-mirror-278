import os
import time
import functools
from coders_utils import open_file, verify_folder

class EnergyTracer:
    def __init__(self, intervalSecs = 0.5):
        self.vals = {} # first ones in lists are baseline
        self.intervalSecs = intervalSecs
        
        self.setup()

    def convertVal(self, val: str):
        return float(val) / 10 ** 6

    def setup(self):
        base_dir = "/sys/class/powercap/intel-rapl/"
        self.locations = {}

        for each in os.listdir(base_dir):
            if each.count(":") == 1:
                self.locations[each] = verify_folder(os.path.join(base_dir, each)) + "energy_uj"
                self.vals[each] = [self.convertVal(open_file(self.locations[each], split_lines = False))]
        
    def getStates(self):
        return {key: [vals[idx] - vals[0] for idx in range(1, len(vals))] for key, vals in self.vals.items()}

    def addState(self):
        for key, val in self.locations.items():
            self.vals[key].append(self.convertVal(open_file(val, split_lines = False)))

class EnergyDeco(EnergyTracer):
    def __init__(self, fxn):
        super().__init__()
        self.fxn = fxn

    def __call__(self, *args, **kwargs):
        result = self.fxn(*args, **kwargs)
        self.addState()
        
        return self.getStates()

def totalEnergy(energyConsumedJson):
    return f"{sum([sum(deviceVals) for deviceVals in energyConsumedJson.values()])} Joules used during this execution!"
    
if __name__ == "__main__":
    # Needs sudoers... bad form. Not willing to install across privileged sections
    @EnergyDeco
    def test():
        for i in range(100000):
            i *= i
            
    print(test())
