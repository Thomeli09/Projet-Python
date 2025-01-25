# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 13:13:23 2025

@author: Thommes Eliott
"""

# Time management library


# Other Lib
import time
import matplotlib.pyplot as plt

# Custom Lib
from PlotLib import ParamPLT, StartPlots, PLTShow, PLTBar

"""
Chronometer structure
"""


class Chrono:
    def __init__(self, Name):
        """
        Initializes the stopwatch with a name.
        """
        self.Name = Name
        self.StartTime = None
        self.ElapsedTime = 0
        self.Running = False
        self.Records = []

    @property
    def getName(self):
        return self.Name

    @getName.setter
    def getName(self, Name):
        self.Name = Name

    @property
    def getStartTime(self):
        return self.StartTime

    @getStartTime.setter
    def getStartTime(self, Time):
        self.StartTime = Time

    @property
    def getElapsedTime(self):
        return self.ElapsedTime

    @getElapsedTime.setter
    def getElapsedTime(self, ElapsedTime):
        self.ElapsedTime = ElapsedTime

    @property
    def getRunning(self):
        return self.Running

    @getRunning.setter
    def getRunning(self, Running):
        self.Running = Running

    @property
    def getRecords(self):
        return self.Records

    @getRecords.setter
    def getRecords(self, Record):
        self.Records.append(Record)

    @property
    def Start(self):
        """
        Starts or resumes the stopwatch.
        """
        if (not self.getRunning):
            self.getStartTime = time.time()
            self.getRunning = True
            print("Info: Stopwatch started.")
        else:
            print("Info: Stopwatch already running.")

    @property
    def Stop(self):
        """
        Stops the stopwatch and records the elapsed time.
        """
        if self.getRunning:
            self.getElapsedTime += time.time() - self.getStartTime
            self.getRunning = False
            print("Info: Stopwatch stopped.")
        else:
            print("Info: Stopwatch already stopped.")

    @property
    def Reset(self):
        """
        Resets the stopwatch.
        """
        self.getStartTime = None
        self.getElapsedTime = 0
        self.getRunning = False
        print("Info: Stopwatch reset.")

    def Record(self, label=None):
        """
        Records the current elapsed time with an optional label.
        """
        if self.getRunning:
            self.Stop
        self.getRecords = (self.ElapsedTime, label)
        self.getElapsedTime = 0  # Resets elapsed time after recording
        print("Info: Stopwatch time recorded.")

    def PLTRecords(self, paramPLT=None):
        """
        Displays the records as a graph.
        """
        if not self.getRecords:
            print("Info: No records to display.")
            return

        if paramPLT is None:
            paramPLT = ParamPLT(colour='b', linetype=1, marker=0, linesize=0.8, fontsize=14)
            paramPLT.getTitle = f"Stopwatch: {self.getName}"
            paramPLT.getXLabel = "Records"
            paramPLT.getYLabel = "Elapsed time (s)"
            paramPLT.getGrid(Axis=-5)

        Times = [rec[0] for rec in self.getRecords]
        Labels = [rec[1] if rec[1] else f"Record {i+1}" for i, rec in enumerate(self.getRecords)]

        StartPlots()
        PLTBar(Labels, Times, paramPLT)
        PLTShow(paramPLT)


"""
Usage example
"""
if __name__ == "__main__":
    DeltaTime = Chrono("My Stopwatch")
    DeltaTime.Start
    time.sleep(2)  # Simulates a computation
    DeltaTime.Record("Task 1")
    DeltaTime.Reset

    DeltaTime.Start
    time.sleep(1)  # Simulates another computation
    DeltaTime.Record("Task 2")

    DeltaTime.PLTRecords()
