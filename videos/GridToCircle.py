from manim import *

class GridToCircle(Scene):
    def construct(self):
        # Create a grid
        grid = NumberPlane()
        
        # Show the grid
        self.play(Create(grid))
        
        # Transform the grid into a circle
        circle = Circle()
        self.play(Transform(grid, circle))

        self.wait(1)
