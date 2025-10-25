# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 11:03:41 2024

@author: Thommes Eliott
"""

# Experiment library


# Other Lib
import pandas as pd
import numpy as np


# Custom Lib


"""
Sauvegarde et lecture des données JSON ou YAML ou (Pickle, HDF5, mais pas lisible par un humain)
"""

"""
Databasis : Default class for all the data
"""
class DataBasis:
    def __init__(self, Name, UpperLevel=False):
        self.Name = Name

        self.UpperLevel = UpperLevel
        if UpperLevel:
            UpperLevel.getLowerLevel = self
            print("Info: Upper level connected")
        else:
            print("Info: No upper level")

        self.LLowerLevel = []

        self.LExperiments = []

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
            print("Info: No upper level")

    @property
    def getLowerLevel(self):
        return self.LLowerLevel

    @getLowerLevel.setter
    def getLowerLevel(self, LowerLevel):
        self.LLowerLevel.append(LowerLevel)

    @property
    def getExperiments(self):
        return self.LExperiments

    @getExperiments.setter
    def getExperiments(self, Experiment):
        self.LExperiments.append(Experiment)
        Experiment.AddSample = self

    def AddExperiment(self, Experiment):
        self.LExperiments.append(Experiment)

    @property
    def getComment(self):
        return self.LComment

    @getComment.setter
    def getComment(self, Comment):
        self.LComment.append(Comment)


"""
1) Experiments
"""
class Experiments(DataBasis):
    def __init__(self, Name, StartDate):
        super().__init__(Name=Name, UpperLevel=None)
        self.StartDate = StartDate
        self.EndDate = None

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
2) Batch of samples
"""
class Batch(DataBasis):
    def __init__(self, Name, ProductionDate, Experiments):
        super().__init__(Name=Name, UpperLevel=Experiments)

        self.ProductionDate = ProductionDate
        self.Volume = None
        self.Material = None

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
    def getMaterial(self):
        return self.Material

    @getMaterial.setter
    def getMaterial(self, Material):
        self.Material = Material
        Material.AddBatch = self


"""
3) Sample
"""
class Sample(DataBasis):
    def __init__(self, Name, Type, ProductionDate, SampleOrComposition):
        super().__init__(Name=Name, UpperLevel=SampleOrComposition)

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
Experiment base class
"""
class Experiment:
    def __init__(self, Name, ID, Type, StartDate, EndDate):
        # Metadata
        self.Name = Name
        self.ID = ID
        self.Type = Type

        # Dates
        self.StartDate = StartDate
        self.EndDate = EndDate

        # Samples
        self.LSamples = []

        # Comments
        self.LComment = []

    # Metadata
    @property
    def getName(self):
        return self.Name

    @getName.setter
    def getName(self, Name):
        self.Name = Name

    @property
    def getID(self):
        return self.ID

    @getID.setter
    def getID(self, ID):
        self.ID = ID

    @property
    def getType(self):
        return self.Type

    @getType.setter
    def getType(self, Type):
        self.Type = Type

    # Dates
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

    # Samples
    @property
    def getSamples(self):
        return self.LSamples

    @getSamples.setter
    def getSamples(self, Sample):
        self.LSamples.append(Sample)
        Sample.AddExperiment = self

    def AddSample(self, Sample):
        self.LSamples.append(Sample)

    # Comments
    @property
    def getComments(self):
        return self.Comment

    @getComments.setter
    def getComments(self, Comment):
        self.LComment.append(Comment)



# A retirer et Définir un type de fichier pour chaque type d'expérience

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
        LSamples = self.getSamples
        LSamples.append(Sample)
        LSamples.getExperiments = self

        self.LSizeResult.append(LSize)
        self.LProportResult.append(LProportion)

    # Plot of results
    def PLT2DGranulo(self, Select, paramPLT):
        """
        Select permet de définir comment afficher les résultats si c'est par échantillons, par type d'échantillon, échantillon parent, compo, Lcaract, Traitement
        """

        return False
