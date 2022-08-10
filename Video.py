from manim import *
import random
from numpy import array_equal
import math

def rule_to_binary(rule : float):
        binary = [0, 0, 0, 0, 0, 0, 0, 0]
        count = 0;
        for i in range(7, -1, -1):
            bit = pow(2, i)
            if rule >= bit:
                rule -= bit;
                binary[count] = 1;
            count += 1;
                
        return binary

def binary_to_rule(binary : []):
    count = 0;
    for i in range(len(binary)):
        bit = pow(2, binary[i] * i);
        count += bit;

    return count;


class Exponent(VGroup):
    power = 0
    digit = 0
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        


class Binary(VGroup):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        for x in range(7):
            pass



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
        self.ruleset = rule_to_binary(self.rule)
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
                s = Cell(stroke_color=WHITE, side_length = 1 / (width / 5))
                s.move_to([j / 4 + i - 3.25, 0, 0])
                if(ruleblocks[i][j] == 1):
                    s.set_fill(BLACK, opacity=1)
                if(j == 1):
                    s1 = Cell(stroke_color=WHITE);
                    s1.move_to([j / 4 + i - 3.25, -0.35, 0])
                    self.add(s1)

                    if(self.ruleset[i] == 1):
                        s1.set_fill(WHITE, opacity=1)
                self.add(s)



class Grid(VGroup):
    width = 5
    height = 5
    columns = [];
    rule = 150
    generation = 0;
    def __init__(self, width : float = 5, height : float = 0, rule = 150, **kwargs):
        super().__init__(**kwargs)
        self.rule = rule
        if height == 0: self.height = width
        else: self.height = height;
        self.width = width;
        self.generation = 0;
        for y in range(self.height, 0, -1):
            new_column = []
            for x in range(self.width):
                s = Cell(stroke_color=BLACK, side_length = 1 / (width / 5), stroke_width = 1)
                s.move_to([x / (width / 5), y / (width / 5), 0])
                new_column.append(s)
                self.add(s)
            self.columns.append(new_column)
        self.center()
        self.clear();

        for column in self.columns:
            for cell in column:
                if cell.state == 1:
                    cell.set_fill(WHITE, opacity=1.0)
                else:
                    cell.set_fill(BLACK, opacity = 1.0)


    def clear(self):
        for column in self.columns:
            for cell in column:
                cell.state = 0;
        
        self.generation = 0;
        self.columns[0][math.floor(len(self.columns[0]) / 2)].state = 1;
    
    def update_grid(self):	
        binary = rule_to_binary(rule = self.rule);
        count = 0;
        for cell in self.columns[self.generation]:
            left = 0;
            if count > 0: left = self.columns[self.generation][count - 1].state
            right = 0;
            if count < len(self.columns[self.generation]) - 1: right = self.columns[self.generation][count + 1].state
            arr = [
                left,
                self.columns[self.generation][count].state,
                right]
            if array_equal(arr, [0, 0, 0]):
                self.columns[self.generation + 1][count].state = binary[7]
            if array_equal(arr, [0, 0, 1]):
                self.columns[self.generation + 1][count].state = binary[6]
            if array_equal(arr, [0, 1, 0]):
                self.columns[self.generation + 1][count].state = binary[5]
            if array_equal(arr, [0, 1, 1]):
                self.columns[self.generation + 1][count].state = binary[4]
            if array_equal(arr, [1, 0, 0]):
                self.columns[self.generation + 1][count].state = binary[3]
            if array_equal(arr, [1, 0, 1]):
                self.columns[self.generation + 1][count].state = binary[2]
            if array_equal(arr, [1, 1, 0]):
                self.columns[self.generation + 1][count].state = binary[1]
            if array_equal(arr, [1, 1, 1]):
                self.columns[self.generation + 1][count].state = binary[0]
            count+=1;


        for column in self.columns:
            for cell in column:
                if cell.state == 1:
                    cell.set_fill(WHITE, opacity=1.0)
                else:
                    cell.set_fill(BLACK, opacity = 1.0)

        print(self.generation)
        self.generation += 1

        if(self.generation % (self.height - 1)== 0):
            self.generation = 0


class Title(Tex):
    def __init__(self, title = "", **kwargs):
        super().__init__(title, **kwargs)
        self.to_corner(UP*2)

class Intro(Scene):
    def construct(self):
        background = Square()
        background.set_fill(GREY_E, opacity=0.75)
        background.scale(10)
        title = Title("Elementary Cellular Automaton")
        self.add(background, title)
        START = (-3.5,2.5,0)
        END =   (3.5,2.5,0)
        line = Line(START,END, stroke_color=YELLOW_C);
        line.set_fill(BLUE_A, opacity=1) 
        grid = Grid(width = 25);
        grid.move_to([0, -0.5, 0])
        self.play(*[FadeIn(_) for _ in grid], Create(line))
        self.wait(0.175)
        for i in range(grid.width):
            grid.update_grid()
            self.wait(0.175)
        self.wait(0.5)
        self.play(*[FadeOut(_) for _ in grid], FadeOut(title), background.animate.set_fill(BLACK, opacity=1.0), Uncreate(line))
        self.wait(0.5)

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
        title = Title("Elementary Cellular Automaton")
        self.add(title)
        START = (-3.5,2.5,0)
        END =   (3.5,2.5,0)

        line = Line(START,END, stroke_color=YELLOW_C);
        line.set_fill(BLUE_A, opacity=1) 
        grid = Grid(width = 100, rule = 182);
        grid.set_fill(BLUE_A, opacity=0.1)
        grid.move_to([0, -0.5, 0])
        tracker = ValueTracker(1)   
        for i in range(grid.height):
            grid.update_grid()
            tracker.set_value(float(i) + 1);
        decimal = DecimalNumber(tracker.get_value(), num_decimal_places=0, include_sign=False, unit=None)
        self.add(grid, line)        
        generation = Text('Generation :').scale(0.7)
        generation.move_to([-0.5, -3.25, 0])
        decimal.next_to(generation, RIGHT)
        self.add(grid, generation, decimal)