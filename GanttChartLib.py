# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 10:16:55 2024

@author: Thommes Eliott
"""

# GanttChart library

import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
from PlotLib import ParamPLT

# Custom Lib


"""
Tasks class
"""


class Tasks:
    def __init__(self):
        self.LTask = []

    @property
    def getLTask(self):
        """Getter for the list of tasks."""
        return self.LTask

    @getLTask.setter
    def getLTask(self, Title, StartDate, EndDate, CompletionRatio=0, Color=None):
        """
        Add a task.

        - paramPLT: An instance of ParamPLT for plot styling.
        - start_date: Optional start date for the plot (YYYY-MM-DD format).
        - end_date: Optional end date for the plot (YYYY-MM-DD format).
        """
        self.LTask.append({
            "task": Title,
            "start": StartDate,
            "end": EndDate,
            "completion_ratio": CompletionRatio,
            "color": Color})

    def PLTTasks(self, paramPLT, StartDate=None, EndDate=None, BCurrentDate=False):
        """Plot the Gantt chart of tasks."""
        if not self.getLTask:
            print("No tasks to plot.")
            return

        # Create DataFrame from the list of tasks
        df = pd.DataFrame(self.getLTask)
        df["start"] = pd.to_datetime(df["start"])
        df["end"] = pd.to_datetime(df["end"])
        df["duration"] = (df["end"] - df["start"]).dt.days
        df["completion_days"] = df["completion_ratio"]*df["duration"]

        # Determine the plot start and end dates
        if StartDate is None:
            StartDate = df["start"].min()
        else:
            StartDate = pd.to_datetime(StartDate)

        if EndDate is None:
            EndDate = df["end"].max()
        else:
            EndDate = pd.to_datetime(EndDate)

        if BCurrentDate:
            CurrentDate = datetime.now()
            StartDate = min(StartDate, CurrentDate)
            EndDate = max(EndDate, CurrentDate)

        # Plotting the Gantt chart
        fig, ax = plt.subplots()
        # fig, ax = plt.subplots(figsize=(paramPLT.fig_width, paramPLT.fig_height))

        YPositions = range(len(df))

        for i, task in enumerate(df.itertuples()):
            # Adding a lower bar - for the overall task duration
            plt.barh(i, width=task.duration, left=task.start, height=0.4, color=task.color, alpha=0.4)

            # Adding an upper bar - for the status of completion
            plt.barh(i, width=task.completion_days, left=task.start, height=0.4, color=task.color)

            ax.text(task.start + pd.Timedelta(days=task.duration/2), i,
                    task.task, ha='center', va='center', color='k', fontsize=paramPLT.getTicksSize)

        if BCurrentDate:
            CurrentDate = pd.to_datetime(datetime.now().strftime('%Y-%m-%d'))
            ax.axvline(x=CurrentDate, color='r', linestyle='dashed')
            ax.text(x=CurrentDate + pd.Timedelta(days=1), y=len(df) - 1, 
                    s=CurrentDate.strftime('%d/%m/%Y'), color='r', fontsize=paramPLT.getTicksSize)

        # Formatting the plot
        ax.set_yticks(YPositions)
        ax.set_yticklabels(df["task"])
        ax.set_xlabel("Date")
        ax.set_xlim(StartDate, EndDate)
        plt.gca().invert_yaxis()
        if paramPLT.getGridAxis:
            plt.grid(axis=paramPLT.getGridAxis,
                    color=paramPLT.getColour,
                    linestyle=paramPLT.getGridLineType,
                    linewidth=paramPLT.getGridLineSize,
                    alpha=0.5)
        plt.title(paramPLT.getTitle, fontsize=paramPLT.getTitleSize)
        plt.show()


"""
-------
Example
-------

# Define the Tasks instance
my_tasks = Tasks()

# Add tasks to the agenda
my_tasks.add_task("Project Planning", "2024-01-01", "2024-06-30")
my_tasks.add_task("Development Phase 1", "2024-07-01", "2025-06-30")
my_tasks.add_task("Testing Phase", "2025-07-01", "2026-03-31")
my_tasks.add_task("Development Phase 2", "2026-04-01", "2027-06-30")
my_tasks.add_task("Final Review", "2027-07-01", "2027-12-31")

# Plot the tasks with default date range
my_tasks.PLTTasks(paramPLT)

# Plot the tasks with a user-defined date range
my_tasks.PLTTasks(paramPLT, start_date="2024-01-01", end_date="2028-01-01")
"""

