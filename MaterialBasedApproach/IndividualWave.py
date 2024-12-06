import random
from MaterialBasedApproach.Material import *

class IndividualWave(object):
    def __init__(self, unit_cell=None, num_unit_cells=0, parent="N/A"):
        if unit_cell is None:
            unit_cell = []
        self.unit_cell = unit_cell # List of materials in a single unit cell (NOT the whole battery)
        self.num_unit_cells = num_unit_cells # Number of unit cells in the jellyroll
        self.parent = parent
        self.wave = self.generate_wave() # automatically generated wave based on the unit cell
        self.fitness_score = 0

    # TODO: Generate a wave based on the unit cell of the object
    def generate_wave(self):
        return "Sample_Wave"

    # Mutations
    # M1
    # TODO: insert a random layer in the unit cell
    def insert_layer(self):
        newCell = self.unit_cell
        newMaterial = random.choice(list(MaterialLibrary.keys()))
        newMaterialPos = random.randint(0, len(newCell) - 1) if len(newCell) > 1 else 0
        newCell.insert(newMaterialPos, Material(newMaterial, random.randint(1, 10), random.randint(1, 10), ))
        self.unit_cell = newCell

    # TODO: remove a random layer from the unit cell
    def remove_layer(self):
        newCell = self.unit_cell
        removeMaterialPos = random.randint(0, len(newCell) - 1)
        newCell.pop(removeMaterialPos)
        self.unit_cell = newCell

    # TODO: swap two layers in the unit cell
    def swap_layers(self):
        newCell = self.unit_cell
        swapLayerA = random.randint(0, len(newCell) - 1)
        swapLayerB = random.randint(0, len(newCell) - 1)
        while swapLayerA == swapLayerB:
            swapLayerB = random.randint(0, len(newCell) - 1)
        tempLayerA = newCell[swapLayerA]
        tempLayerB = newCell[swapLayerB]
        newCell.pop(swapLayerA)
        newCell.insert(swapLayerA, tempLayerA)
        newCell.pop(swapLayerB)
        newCell.insert(swapLayerB, tempLayerB)
        self.unit_cell = newCell

    # TODO: generate new layer parameters in the unit cell
    def gen_new_parameters(self):
        pass

    # M2
    # TODO: change a material thickness in the unit cell
    def change_thickness(self):
        newCell = self.unit_cell
        targetMaterial = random.randint(0, len(newCell) - 1)
        newThickness = random.randint(1, 25)
        newCell[targetMaterial].thickness = newThickness
        self.unit_cell = newCell

    # M3
    # TODO: change a material's wave speed in the unit cell
    def change_wave_speed(self):
        pass

    # M4
    # TODO: Swap parameters of two layers in the unit cell
    def swap_layer_params(self):
        pass

    # M5
    # TODO: Change the number of unit cells
    def change_num_unit_cells(self):
        newUnit = random.randint(0, 1)
        if newUnit == 0:
            self.num_unit_cells += 1
        elif newUnit == 1:
            self.num_unit_cells -= 1

    """ 
    Alter the parameters of a parent IndividualWave through mutation steps M1-M5
    @param parent: optional string to trace the lineage of the new object
    @param alterationDegree: int 1-4 to determine how many mutations should be performed on the object
    @returns: new IndividualWave object
    """
    def mutation(self, alterationDegree, parent="N/A"):
        childWave = IndividualWave(self.unit_cell, self.num_unit_cells, parent=parent)
        while alterationDegree != 0:
            genMutationSelect = random.randint(1, 4)
            match genMutationSelect:
                # M1: perform one of four possible individual layer mutations
                case 1:
                    m1MutationSelect = random.randint(1, 4)
                    while len(childWave.unit_cell) <= 1:
                        childWave.insert_layer()
                    match m1MutationSelect:
                        case 1:
                            childWave.insert_layer()
                        case 2:
                            childWave.remove_layer()
                        case 3:
                            if len(childWave.unit_cell) > 1:
                                childWave.swap_layers()
                        case 4:
                            childWave.gen_new_parameters()
                # M2: Change thickness of a layer
                case 2:
                    childWave.change_thickness()
                # M3: Swap parameters of two layers
                case 3:
                    childWave.swap_layer_params()
                # M4: Change the number of unit cells in the battery
                case 4:
                    childWave.change_num_unit_cells()
            return childWave

    # Fitness testing
    def correlation(self, reference):
        return 1

    def dynamic_time_warping(self, reference):
        return 1

    def correlation_symmetry(self, reference, division):
        return 1
