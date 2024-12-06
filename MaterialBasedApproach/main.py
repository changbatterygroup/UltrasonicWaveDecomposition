from MaterialBasedApproach.IndividualWave import *
from MaterialBasedApproach.Material import *

# TODO: Return a fitness score based on the above fitness tests

#def determine_fitness(CompWave: IndividualWave, Reference: IndividualWave):
#    score = 0
#    scoreFactor = 100 / (len(Reference.unit_cell) * 5)
#    for x in range(0, len(CompWave.unit_cell) - 1):
#        if len(Reference.unit_cell) <= x:
#            break
#        if CompWave.unit_cell[x].material_type == Reference.unit_cell[x].material_type:
#            score += 3
#        score += (1 / abs(CompWave.unit_cell[x].density))
#        score += (1 / abs(CompWave.unit_cell[x].thickness))
#    score *= scoreFactor
#    score -= abs(len(CompWave.unit_cell) - len(Reference.unit_cell))
#    score -= abs(CompWave.num_unit_cells - Reference.num_unit_cells)
#    return score
"""
Determine the fitness score of a wave relative to the reference wave
@param CompWave: Generated IndividualWave object to compare
@param Reference: Reference waveform
@param cellDivision: Number of times to divide a wave for correlation symmetry
@param weight: Fitness method to score above the others. Can be "correlation", "DTW", or "correlation_sym"
@param weightParam: Float, amount to weigh a particular method by
"""
def determine_fitness(CompWave: IndividualWave, Reference, cellDivision=2, weight="unweighted", weightParam=0):
    score = 0
    # Each fitness score is out of 100 for a maximum score of 300 without weights

    # Correlation score: determine how similar two signals are when laid over top of each other.
    # Score is the percentage of points in common over the entire wave
    corScore = CompWave.correlation(Reference)

    # Dynamic time warping score: Match out of phase signal features
    dtwScore = CompWave.dynamic_time_warping(Reference)

    # Correlation symmetry score: Divide the waves into cellDivision equal slices and measure their correlation scores
    # Final score is the average of correlation scores across the wave
    # cellDivision defaults to 2, so the wave is sliced in half and compared.
    corSymScore = CompWave.correlation_symmetry(Reference, cellDivision)

    if weight != "unweighted":
        match weight:
            case "correlation":
                corScore *= weightParam
            case "DTW":
                dtwScore *= weightParam
            case "correlation_sym":
                corSymScore *= weightParam
            case _:
                print("Unrecognized weight specification")
    CompWave.fitness_score = corScore + dtwScore + corSymScore
    return CompWave.fitness_score




def mate(IndividualA, IndividualB, Reference):
    scoreA = 0
    scoreB = 0
    child = IndividualWave()
    child.num_unit_cells = 0
    child.unit_cell = []
    runs = 0
    for x in range(0, len(Reference.unit_cell) - 1):
        runs += 1
        if len(IndividualA.unit_cell) <= x or len(IndividualB.unit_cell) <= x:
            break
        scoreA += 1 / (abs(IndividualA.unit_cell[x].density - Reference.unit_cell[x].density) + 1)
        scoreB += 1 / (abs(IndividualB.unit_cell[x].density - Reference.unit_cell[x].density) + 1)
        scoreA += 1 / (abs(IndividualA.unit_cell[x].thickness - Reference.unit_cell[x].thickness) + 1)
        scoreB += 1 / (abs(IndividualB.unit_cell[x].thickness - Reference.unit_cell[x].thickness) + 1)
        scoreA += 1 if IndividualA.unit_cell[x].material_type == Reference.unit_cell[x].material_type else -1
        scoreB += 1 if IndividualB.unit_cell[x].material_type == Reference.unit_cell[x].material_type else -1
        child.unit_cell.append(IndividualB.unit_cell[x]) if scoreB > scoreA else child.unit_cell.append(IndividualA.unit_cell[x])
    child.num_unit_cells = IndividualB.num_unit_cells if abs(IndividualA.num_unit_cells - Reference.num_unit_cells) > abs(IndividualB.num_unit_cells - Reference.num_unit_cells) else IndividualA.num_unit_cells
    return child

def main():
    ReferenceWaveMaterials = [Material("Aluminum", 1, 2),
                              Material("Copper", 5, 3),
                             Material("Copper", 1, 6),
                              Material("Copper", 3, 7)]
    ReferenceWave = IndividualWave(ReferenceWaveMaterials, 8)


    startingWaveMaterials = [Material("Aluminum", 1, 1),
                             Material("Copper", 1, 1)]
    startingWave = IndividualWave(startingWaveMaterials, 5)
    populationSize = 12
    survivingParents = 2
    generation = 1
    population = []
    found = False
    totalMaxFitness = 0
    maxFitness = 0
    for x in range(populationSize):
        population.append(startingWave.mutation())

    while not found:
        if len(population) == 0 or type(population) is None:
            print("ERROR: Population is empty")

        population.sort(key=(lambda wave: determine_fitness(wave, ReferenceWave)), reverse=True)  # Sort the waves based on their fitness scores
                                                                      # TODO: Make the fitness score a field instead of running the method everytime
        bestFit = determine_fitness(population[0], ReferenceWave)
        if 110 >= bestFit >= 90 or generation >= 80: # If the fitness score is 0 or it reaches the 80th generation, return the most fit wave
            found = True
            break

        print("Generation: {gen} Population Size: {pop} Minimum fitness: {minFit}".format( # General print for each generation
            gen=generation,
            pop=len(population),
            minFit=determine_fitness(population[0], ReferenceWave)))

        maxFitness = determine_fitness(population[0], ReferenceWave)
        totalMaxFitness = maxFitness if maxFitness > totalMaxFitness else totalMaxFitness

        matString = ""
        for n in range(len(population)):  # General print for each individual
            for m in range(len(population[n].unit_cell)):
                matString += population[n].unit_cell[m].material_type + ", "
            print("Child {num} - Parent: {par}, Fitness: {fit}, Unit cells: {numCells}, Materials: {mats}".format(
                num=n,
                par=population[n].parent,
                fit=determine_fitness(population[n], ReferenceWave),
                numCells=population[n].num_unit_cells,
                mats=matString
            ))
            matString = ""
        next_gen = []
        parents = []
        for j in range(survivingParents):
            parents.append(population[j])
        for n in range(int(populationSize / 3)): # / survivingParents  # Mutate current gen and add to next_gen list
            next_gen.append(mate(parents[0], parents[1], ReferenceWave).mutation("Mate"))
            next_gen.append(parents[0].mutation("0"))
            next_gen.append(parents[1].mutation("1"))
            #for i in range(len(parents)):  #int(populationSize/(populationSize / survivingParents))):

        if len(next_gen) != populationSize: # Stop running if it generates too many or too few children
            print("ERROR: New generation exceeds population size")
            break

        population.clear()
        population = next_gen # Replace current population with the next generation

        generation += 1

    if found: # When the loop breaks, check if the best fit was found. If it was, print it.
        matStringFinal = ""
        for m in range(len(population[0].unit_cell)):
            matStringFinal += population[0].unit_cell[m].material_type + ", "

        print("Best fit found! Generation: {gen} Materials: {wave}".format(
            gen=generation,
            wave=matStringFinal
        ))
        matStringFinal = ""
        print("Total max fitness :", totalMaxFitness)

if __name__ == '__main__':
    main()
