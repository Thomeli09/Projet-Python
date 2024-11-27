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
    def getLTask(self, Title, StartDate, EndDate):
        """
        Add a task.

        - paramPLT: An instance of ParamPLT for plot styling.
        - start_date: Optional start date for the plot (YYYY-MM-DD format).
        - end_date: Optional end date for the plot (YYYY-MM-DD format).
        """
        self.LTask.append({
            "task": Title,
            "start": StartDate,
            "end": EndDate})

    def PLTTasks(self, paramPLT, start_date=None, end_date=None):
        """Plot the Gantt chart of tasks."""
        if not self.LTask:
            print("No tasks to plot.")
            return

        # Create DataFrame from the list of tasks
        df = pd.DataFrame(self.LTask)
        df["start"] = pd.to_datetime(df["start"])
        df["end"] = pd.to_datetime(df["end"])
        df["duration"] = (df["end"] - df["start"]).dt.days

        # Determine the plot start and end dates
        if start_date is None:
            start_date = df["start"].min()
        else:
            start_date = pd.to_datetime(start_date)

        if end_date is None:
            end_date = df["end"].max()
        else:
            end_date = pd.to_datetime(end_date)

        # Plotting the Gantt chart
        fig, ax = plt.subplots(figsize=(paramPLT.fig_width, paramPLT.fig_height))
        y_positions = range(len(df))

        for i, task in enumerate(df.itertuples()):
            ax.barh(i, task.duration, left=task.start, height=0.4, color=paramPLT.bar_color)
            ax.text(task.start + pd.Timedelta(days=task.duration / 2), i,
                    task.task, ha='center', va='center', color=paramPLT.text_color, fontsize=paramPLT.font_size)

        # Formatting the plot
        ax.set_yticks(y_positions)
        ax.set_yticklabels(df["task"])
        ax.set_xlabel("Date")
        ax.set_xlim(start_date, end_date)
        ax.grid(paramPLT.grid)
        plt.title(paramPLT.title)
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

