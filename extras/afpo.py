from genome import GENOME
import constants
import copy
import random
import numpy as np
import copy
import sys
import time

class AFPO:

    def __init__(self,whatToMaximize, maxDepth):

        # random.seed(0)

        # np.random.seed(0)

        self.robotType = maxDepth

        self.timeSinceLastInjection = time.time()

        self.whatToMaximize = whatToMaximize

        self.genomes = {}

        self.nextAvailableID = 0

        for g in range(0,constants.popSize):

            self.genomes[g] = GENOME(self.nextAvailableID, self.robotType)

            self.nextAvailableID = self.nextAvailableID + 1

    def Advance_One_Generation(self,environment):

            self.Find_Pareto_Front()

            self.Sort_By_Dominated()

            self.Count_NonDominated_Solutions()

            self.Sort_NonDominated_By_Fitness()

            # if self.time_to_save:

            #     self.Save_Best()

            #     # self.Save_Random_Genome_From_Pareto_Front()

            self.Save_Best()

            # self.Display_Best()

            self.Delete_Dominated_Solutions()

            self.Print()

            self.Age_NonDominated_Solutions()

            self.Fill()

            self.Evaluate_All(environment)

    def Age_NonDominated_Solutions(self):

        for g in range(0,constants.popSize):

            if ( g in self.genomes ):

                self.genomes[g].Age()

        def Attempt_Injection_Of_New_Genome(self):

                self.secondsElapsedSinceLastInjection = time.time() - self.timeSinceLastInjection
                
                if ( self.secondsElapsedSinceLastInjection > 60.0 ):
                
                        self.Inject_New_Genome()
        
                        self.timeSinceLastInjection = time.time()

    def Count_NonDominated_Solutions(self):

        self.numNonDominated = 0

        for g in range(0,constants.popSize):

            if ( self.genomes[g].Get_Dominated() == False ):

                self.numNonDominated = self.numNonDominated + 1

    def Delete_Dominated_Solutions(self):

        for g in range(self.numNonDominated,constants.popSize):

            del self.genomes[g]

    def Display_Best(self):

        self.genomes[0].Display()

    def Evaluate_All(self,environment):

        for g in range(0,constants.popSize):

            if ( self.genomes[g].Get_Evaluated() == False ):

                                self.genomes[g].Send_To_Simulator(playBlind=True,playPaused=False,evaluationTime=constants.evaluationTime,environment=environment)

        for g in range(0,constants.popSize):

                        if ( self.genomes[g].Get_Evaluated() == False ):

                                self.genomes[g].Get_From_Simulator(self.whatToMaximize)

    def Evolve(self,environment):

        self.Evaluate_All(environment)

        for g in range(0,constants.numGenerations):

            print g,constants.numGenerations

            # if (g+1)%300 == 0: 

            #     self.time_to_save = True 
            # else: 
            #     self.time_to_save = False

            self.Advance_One_Generation(environment)

    def Fill(self):

        self.Spawn_Mutants_From_Pareto_Front()

        # self.Attempt_Injection_Of_New_Genome()

        self.Inject_New_Genome()

    def Find_Pareto_Front(self):

        self.Make_All_Genomes_NonDominated()

        for i in range(0,constants.popSize):

            for j in range(0,constants.popSize):

                if ( i != j ):

                    j_dominates_i = self.genomes[j].Dominates( self.genomes[i] )

                    if ( j_dominates_i ):

                        self.genomes[i].Set_Dominated( True )

    def Inject_New_Genome(self):

        self.genomes[constants.popSize-1] = GENOME(self.nextAvailableID, self.robotType)

        self.nextAvailableID = self.nextAvailableID + 1

    def Make_All_Genomes_NonDominated(self):

        for g in range(0,constants.popSize):

            self.genomes[g].Set_Dominated(False)

    def Print(self):

        for g in range(0,constants.popSize):

            if ( g in self.genomes ):

                self.genomes[g].Print()     

        print ''

    def Save_Best(self):

        # print self.genomes[0].ID
        
        self.genomes[0].Save(self.whatToMaximize)

    def Save_Random_Genome_From_Pareto_Front(self):

        selectedGenome = random.randint(0,self.numNonDominated-1)

        self.genomes[selectedGenome].Save(self.whatToMaximize)

    def Sort_By_Dominated(self):

        length = len(self.genomes) - 1

        sorted = False

        while not sorted:

            sorted = True

            for i in range(length):

                if ( (self.genomes[i].Get_Dominated()==True) and (self.genomes[i+1].Get_Dominated()==False) ):

                    sorted = False

                    self.genomes[i], self.genomes[i+1] = self.genomes[i+1], self.genomes[i]

    def Sort_NonDominated_By_Fitness(self):

                length = self.numNonDominated - 1

                sorted = False

                while not sorted:

                        sorted = True

                        for i in range(length):

                                if ( self.genomes[i].Get_Fitness() > self.genomes[i+1].Get_Fitness() ):

                                        sorted = False

                                        self.genomes[i], self.genomes[i+1] = self.genomes[i+1], self.genomes[i]


    def Spawn_Mutants_From_Pareto_Front(self):

            for g in range(self.numNonDominated,constants.popSize):

                genomeIndexToCopy = random.randint(0,self.numNonDominated-1)

                self.genomes[g] = copy.deepcopy( self.genomes[genomeIndexToCopy] )

                self.genomes[g].ID = self.nextAvailableID

                self.nextAvailableID = self.nextAvailableID + 1

                self.genomes[g].Mutate()

                self.genomes[g].Reset()
