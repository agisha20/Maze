## Solve-a-simple-maze with Python3

Solving binary-image mazes recursively with OpenCV2

Maze must...
- be image
- be binary
- white pixels are traversable
- black pixels are walls
- entry point must be on top or left border
- finish point must be on bottom or right border
- there must be ONLY ONE SOLUTION

Output...
- gray pixels: the program traversed these pixels but did not include them in solution
- white pixels: pixels not traversed
- red pixels: solution