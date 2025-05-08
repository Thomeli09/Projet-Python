# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 11:21:29 2024

@author: Thommes Eliott
"""

# Library of graphics and translation to TikZ and PGF


# Other Lib


# Custom Lib

import matplotlib.pyplot as plt

class TikzPicture:
    def __init__(self):
        self.commands = []

    def add_line(self, x1, y1, x2, y2, options="thick"):
        cmd = f"\\draw[{options}] ({x1},{y1}) -- ({x2},{y2});"
        self.commands.append(cmd)
        
    def add_circle(self, center_x, center_y, radius, options="thick"):
        cmd = f"\\draw[{options}] ({center_x},{center_y}) circle ({radius});"
        self.commands.append(cmd)

    def generate_tikz(self):
        body = "\n".join(self.commands)
        return f"\\begin{{tikzpicture}}\n{body}\n\\end{{tikzpicture}}"

    def plot(self):
        fig, ax = plt.subplots()
        for cmd in self.commands:
            if '--' in cmd:  # crude detection for line
                parts = cmd.split()
                p1 = parts[1].strip('()')
                p2 = parts[3].strip('();')
                x1, y1 = map(float, p1.split(','))
                x2, y2 = map(float, p2.split(','))
                ax.plot([x1, x2], [y1, y2], marker='o')
            if 'circle' in cmd:
                parts = cmd.split()
                p = parts[1].strip('()')
                r = float(parts[-2].strip('()'))
                x, y = map(float, p.split(','))
                circle = plt.Circle((x, y), r, fill=False)
                ax.add_patch(circle)
        ax.set_aspect('equal')
        ax.grid(True)
        plt.show()

# Example usage
picture = TikzPicture()
picture.add_line(0, 0, 2, 2)
picture.add_circle(1, 1, 0.5)

picture.plot()
tikz_code = picture.generate_tikz()
print(tikz_code)
