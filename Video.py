from manim import *
import random
from numpy import array_equal

RULE = 191

class Binary(VGroup):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Cell(Square):
    state : int = 0
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.state = 0
        
class Rules(VGroup):
    rule : int = 0
    ruleset = []
    def __init__(self, rule = 0, **kwargs):
        super().__init__(**kwargs)
        self.rule = rule
        self.ruleset = self.rule_to_binary(self.rule)
        ruleblocks = [
            [0, 0, 0],
            [0, 0, 1], 
            [0, 1, 0], 
            [0, 1, 1], 
            [1, 0, 0], 
            [1, 0, 1], 
            [1, 1, 0], 
            [1, 1, 1]
        ]

        for i in range(8):
            for j in range(3):
                s = Cell(stroke_color=WHITE, side_length = 1 / 4)
                s.move_to([j / 4 + i - 3.25, 0, 0])
                if(ruleblocks[i][j] == 1):
                    s.set_fill(WHITE, opacity=1)
                if(j == 1):
                    s1 = Cell(stroke_color=WHITE, side_length = 1 / 4);
                    s1.move_to([j / 4 + i - 3.25, -0.35, 0])
                    self.add(s1)

                    if(self.ruleset[i] == 1):
                        s1.set_fill(WHITE, opacity=1)
                self.add(s)


    def rule_to_binary(self, rule : float):
        binary = [0, 0, 0, 0, 0, 0, 0, 0]
        count = 0;
        for i in range(7, -1, -1):
            bit = pow(2, i)
            if rule >= bit:
                rule -= bit;
                binary[count] = 1;
            count += 1;
                
        return binary

class Grid(VGroup):
    width = 5
    height = 5
    columns = [];
    def __init__(self, width : float = 5, height  : float = 5, **kwargs):
        super().__init__(**kwargs)
        self.width = width;
        self.height = height;
        for y in range(-1, self.height):
            new_column = []
            for x in range(self.width):
                s = Cell(stroke_color=WHITE, side_length = 1 / (width / 5))
                s.move_to([x / (width / 5), y / (height / 5), 0])
                new_column.append(s)
                if len(self.columns) != 0: self.add(s)
            self.columns.append(new_column)
        self.center()
    
    def rule_to_binary(self, rule : float):
        binary = [0, 0, 0, 0, 0, 0, 0, 0]
        count = 0;
        for i in range(7, -1, -1):
            bit = pow(2, i)
            if rule >= bit:
                rule -= bit;
                binary[count] = 1;
            count += 1;
                
        return binary
    
    
    def update_grid(self):	
        binary = self.rule_to_binary(rule = RULE);
        count = 0;
        for cell in self.columns[0]:
            right = 0;
            if count > 0: right = self.columns[0][count - 1].state
            left = 0;
            if count < len(self.columns[0]) - 1: left = self.columns[0][count + 1].state
            arr = [
                right,
                cell.state,
                left]
            
            if array_equal(arr, [0, 0, 0]):
                cell.state = binary[7]
            if array_equal(arr, [0, 0, 1]):
                cell.state = binary[6]
            if array_equal(arr, [0, 1, 0]):
                cell.state = binary[5]
            if array_equal(arr, [0, 1, 1]):
                cell.state = binary[4]
            if array_equal(arr, [1, 0, 0]):
                cell.state = binary[3]
            if array_equal(arr, [1, 0, 1]):
                cell.state = binary[2]
            if array_equal(arr, [1, 1, 0]):
                cell.state = binary[1]
            if array_equal(arr, [1, 1, 1]):
                cell.state = binary[0]
            count +=1

        for i in range(len(self.columns) - 1, 0, -1):
            count = 0
            for cell in self.columns[i]:
                cell.state = self.columns[i - 1][count].state
                count += 1

        for column in self.columns:
            for cell in column:
                if cell.state == 1:
                    cell.set_fill(BLUE_A, opacity=1.0)
                else:
                    cell.set_fill(BLUE_D, opacity=0.5)
        

class Title(Tex):
    def __init__(self, title = "", **kwargs):
        super().__init__(title, **kwargs)
        self.to_corner(UP*2)

class Intro(Scene):
    def construct(self):
        background = Square()
        background.set_fill(GREY_E, opacity=0.75)
        background.scale(10)
        self.add(background)
        title = Title("1D Cellular Automaton")
        self.add(title)
        START = (-3,2.5,0)
        END =   (3,2.5,0)
        line = Line(START,END, stroke_color=YELLOW_C);
        line.set_fill(BLUE_A, opacity=1) 
        self.play(Create(line))
        grid = Grid(width = 15, height = 15);
        grid.set_fill(BLUE_A, opacity=0.1)
        grid.update_grid()
        grid.move_to([0, -0.5, 0])
        self.play(*[FadeIn(_) for _ in grid], Create(line))
        for i in range(14):
            grid.update_grid()
            self.wait(0.175)
        self.wait(0.5)
        self.play(*[FadeOut(_) for _ in grid], FadeOut(title), background.animate.set_fill(BLACK, opacity=1.0), Uncreate(line))

class Description(Scene):
    def construct(self):
        rules = Rules(rule = 1)
        self.add(rules)

class Example(Scene):
    def construct(self):
        pass

class Thumbnail(Scene):
    def construct(self):
        background = Square()
        background.set_fill(GREY_E, opacity=0.75)
        background.scale(10)
        self.add(background)
        title = Title("1D Cellular Automaton")
        self.add(title)
        START = (-3,2.5,0)
        END =   (3,2.5,0)
        line = Line(START,END, stroke_color=YELLOW_C);
        line.set_fill(BLUE_A, opacity=1) 
        grid = Grid(width = 15, height = 15);
        grid.set_fill(BLUE_A, opacity=0.1)
        grid.update_grid()
        grid.move_to([0, -0.5, 0])
        for i in range(14):
            grid.update_grid()
        self.add(grid, line)        
        generation = Text('Generation :').scale(0.7)
        generation.move_to([-0.25, -3.25, 0])
        decimal = DecimalNumber(14, num_decimal_places=0, include_sign=False, unit=None)
        decimal.next_to(generation, RIGHT)
        self.add(grid, generation, decimal)