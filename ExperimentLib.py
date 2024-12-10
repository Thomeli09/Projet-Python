# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 11:03:41 2024

@author: Thommes Eliott
"""

# Experiment library

# Other Lib

# Custom Lib

"""
Sauvegarde et lecture des données JSON ou YAML ou (Pickle, HDF5, mais pas lisible par un humain)
"""

"""
Base element
"""
from ast import List
from pickle import TRUE
import string


class DataBasis:
    def __init__(self, Name, UpperLevel):
        self.Name = Name

        self.UpperLevel = None
        self.LLowerLevel = []

        self.LTest = []

        self.LComment = []

    @property
    def getName(self):
        return self.Name

    @getName.setter
    def getName(self, Name):
        self.Name = Name

    @property
    def getUpperLevel(self):
        return self.UpperLevel

    @getUpperLevel.setter
    def getUpperLevel(self, UpperLevel):
        if self.UpperLevel:
            self.UpperLevel = UpperLevel
            UpperLevel.getLowerLevel = self
            # Retirer la précédente et remettre la nouvelle
        else:
            print("Info: Already highest level")

    @property
    def getLowerLevel(self):
        return self.LLowerLevel

    @getLowerLevel.setter
    def getLowerLevel(self, LowerLevel):
        if self.UpperLevel:
            self.LLowerLevel.append(LowerLevel)
        else:
            print("Info: Already lowest level")

    @property
    def getExperiments(self):
        return self.LTest

    @getExperiments.setter
    def getExperiments(self, Experiment):
        self.LTest.append(Experiment)

    @property
    def getComment(self):
        return self.LComment

    @getComment.setter
    def getComment(self, Comment):
        self.LComment.append(Comment)

"""
Experiments
"""
class Experiments(DataBasis):
    def __init__(self, Name, StartDate):
        super().__init__(Name=Name, UpperLevel=None)

        self.StartDate = StartDate
        self.EndDate = 0

    @property
    def getStartDate(self):
        return self.StartDate

    @getStartDate.setter
    def getStartDate(self, StartDate):
        self.StartDate = StartDate

    @property
    def getEndDate(self):
        return self.EndDate

    @getEndDate.setter
    def getEndDate(self, EndDate):
        self.EndDate = EndDate


"""
Composition
"""
class Composition(DataBasis):
    def __init__(self, Name, ProductionDate, Experiments):
        super().__init__(Name=Name, UpperLevel=Experiments)

        self.ProductionDate = ProductionDate
        self.Volume = None
        self.Compo = None

    @property
    def getProdDate(self):
        return self.ProductionDate

    @getProdDate.setter
    def getProdDate(self, ProductionDate):
        self.ProductionDate = ProductionDate

    @property
    def getVolume(self):
        return self.Volume

    @getVolume.setter
    def getVolume(self, Volume):
        self.Volume = Volume

    @property
    def getCompo(self):
        return self.Compo

    @getCompo.setter
    def getCompo(self, Compo):
        self.Compo = Compo

    @property
    def getMaterial(self):
        # Listing des ingrédients utilisés pour le volume X
        print('Listes des ingrédients de la composition {}, pour un volume de {} m3'.format(self.getName, self.getVolume))

        for key, value in self.getCompo:
            print(f"   -{key}: {value*self.getVolume} kg")
        return True

    def CmptCompo(self, Data):
        # Calcul 
        self.getCompo = Data
        return True

    def PLT2DCompo(self, Data):
        # Plot de la composition
        return True




"""
ParentSample
"""
class ParentSample(DataBasis):
    def __init__(self, Name, Type, ProductionDate, Composition):
        super().__init__(Name=Name, UpperLevel=Composition)

        self.Type = Type
        self.ProductionDate = ProductionDate
        self.Volume = None

    @property
    def getType(self):
        return self.Type

    @getType.setter
    def getType(self, Type):
        self.Type = Type

    @property
    def getProdDate(self):
        return self.ProductionDate

    @getProdDate.setter
    def getProdDate(self, ProductionDate):
        self.ProductionDate = ProductionDate

    @property
    def getVolume(self):
        return self.Volume

    @getVolume.setter
    def getVolume(self, Volume):
        self.Volume = Volume


"""
Sample
"""
class Sample(DataBasis):
    def __init__(self, Name, ExtractionDate, Type, ParentSample):
        super().__init__(Name=Name, UpperLevel=ParentSample)

        self.Type = Type
        self.LCaract = []
        self.ExtractionDate = ExtractionDate

    @property
    def getType(self):
        return self.Type

    @getType.setter
    def getType(self, Type):
        self.Type = Type

    @property
    def getLCaract(self):
        return self.LCaract

    @getLCaract.setter
    def getLCaract(self, Caract):
        self.LCaract.append(Caract)

    @property
    def getExtractDate(self):
        return self.ExtractionDate

    @getExtractDate.setter
    def getExtractDate(self, ExtractionDate):
        self.ExtractionDate = ExtractionDate


"""
Experiment base class
"""
class Experiment:
    def __init__(self, Name, StartDate):
        self.Name = Name
        self.StartDate = StartDate
        self.EndDate = 0
        self.LComment = []

    @property
    def getName(self):
        return self.Name

    @getName.setter
    def getName(self, Name):
        self.Name = Name

    @property
    def getStartDate(self):
        return self.StartDate

    @getStartDate.setter
    def getStartDate(self, StartDate):
        self.StartDate = StartDate

    @property
    def getEndDate(self):
        return self.EndDate

    @getEndDate.setter
    def getEndDate(self, EndDate):
        self.EndDate = EndDate

    @property
    def getComments(self):
        return self.Comment

    @getComments.setter
    def getComments(self, Comment):
        self.LComment.append(Comment)


"""
Sorption and Desorption
"""

class DeSorptionSorption(Experiment):
    def __init__(self, Name, StartDate, Other):
        super().__init__(Name, StartDate)
        self.Other = Other

    # Trace le type d'expérience et les valeurs à partir d'une liste

# Plot of results


"""
Granulometry
"""
class Granulometry(Experiment):
    def __init__(self, Name, StartDate, LSample):
        super().__init__(Name, StartDate)
        self.LSample = []
        self.LSizeResult = []
        self.LProportResult = []

    @property
    def getSamples(self):
        return self.LSample

    @property
    def getResults(self):
        return (self.LSizeResult, self.LProportResult)

    def getSampleResults(self, SampleID):
        if SampleID == str: 
            Index = self.getSampleName.index(SampleID) 
            return (self.LSizeResult[Index], self.LProportResult[Index])
        else:
            return (self.LSizeResult[SampleID], self.LProportResult[SampleID])

    def AddSample(self, Sample, LSize, LProportion):
        self.LSample.append(Sample)
        LSample.getExperiments = self

        self.LSizeResult.append(LSize)
        self.LProportResult.append(LProportion)

    # Plot of results
    def PLT2DGranulo(self, Select, paramPLT):
        """
        Select permet de définir comment afficher les résultats si c'est par échantillons, par type d'échantillon, échantillon parent, compo, Lcaract, Traitement
        """

        return False