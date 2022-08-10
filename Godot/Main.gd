extends Node2D

export(PackedScene) var Cell;

const CELLSIZE : int = 4;

onready var SCREEN_SIZE = get_viewport_rect().size;

var columns = [];
var rows = 0;
var generation : int = 0;
var selected : Array = [0, 1];
var play : bool = true;
var color : bool = true;
export(int, 0, 255) var rule;

func _ready():
	create_grid();

func create_grid():
	var rng = RandomNumberGenerator.new()
	rows = int(floor(SCREEN_SIZE.y / CELLSIZE));
	for y in range(0, rows):
		var new_column = []
		for x in range(0, SCREEN_SIZE.x / CELLSIZE):
			var cell = Cell.instance();
			cell.position = Vector2(CELLSIZE * x + CELLSIZE / 2, CELLSIZE * y + CELLSIZE / 2);
			cell.pos = Vector2(x, y);
			cell.state = 0
			new_column.append(cell)
			add_child(cell);
		columns.append(new_column)
	
	columns[0][int(round(columns[0].size() / 2))].state = 1

func rule_to_binary(rule : float) -> Array:
	var binary = [0, 0, 0, 0, 0, 0, 0, 0]
	var count = 0;
	for i in range(7, -1, -1):
		var bit = pow(2, i)
		if rule >= bit:
			rule -= bit;
			binary[count] = 1;
		count += 1;
			
	return binary
	

func alive_process():
	
	var binary = rule_to_binary(rule);
	var count = 0;
	for cell in columns[generation]:
		var right = 0;
		if count < columns[generation].size() - 1: right = columns[generation][count + 1].state
		var left = 0;
		if count > 0: left = columns[generation][count - 1].state
		var set = [
			left,
			cell.state,
			right]
		
		match set:
			[0, 0, 0]:
				 columns[generation + 1][count].state = binary[7]
			[0, 0, 1]:
				columns[generation + 1][count].state = binary[6]
			[0, 1, 0]:
				columns[generation + 1][count].state = binary[5]
			[0, 1, 1]:
				columns[generation + 1][count].state = binary[4]
			[1, 0, 0]:
				columns[generation + 1][count].state= binary[3]
			[1, 0, 1]:
				columns[generation + 1][count].state = binary[2]
			[1, 1, 0]:
				columns[generation + 1][count].state = binary[1]
			[1, 1, 1]:
				columns[generation + 1][count].state = binary[0]
	
		count +=1

	generation += 1;
	if generation % (rows - 1) == 0:
		rule = (rule + 1) % 255
		clear()
		if(selected[1] + 1 > columns[selected[0]].size() - 1):
			if(selected[0] + 1 > columns.size() - 1):
				selected[0] = 0;
				selected[1] = 0;
			else:
				selected[0] += 1;
				selected[1] = 0;
		else:
			selected[1] += 1

	
func clear():
	for column in columns:
		for cell in column:
			cell.state = 0;
			
	generation = 0;
	columns[0][int(floor(columns[0].size() / 2))].state = 1
	
func check_box():
	
	for column in columns:
		for cell in column:
			if cell.state:
				cell.state = 0;
				cell.modulate = columns[selected[0]][selected[1]].deadColor;
			else:
				cell.state = 1;
				cell.modulate = columns[selected[0]][selected[1]].aliveColor;
	
func random_grid():
	for column in columns:
		for cell in column:
			var randNumber = rand_range(0, 1);
			if randNumber > 0.85:
				cell.state = 1;
			else:
				cell.state = 0

func _unhandled_input(event):
	if event is InputEventKey:
		if event.pressed and event.scancode == KEY_ESCAPE:
				get_tree().quit();
		if event.pressed and event.scancode == KEY_SPACE:
				play = !play;
		if event.pressed and event.scancode == KEY_C:
			color = !color;
		if event.pressed and event.scancode == KEY_V:
			clear();
		if event.pressed and event.scancode == KEY_RIGHT:
			rule = (rule + 1) % 255
			clear();
		if event.pressed and event.scancode == KEY_LEFT:
			if rule - 1 == -1: 
				rule = 255;
				clear();
			else: 
				rule -= 1;
				clear();
	if event is InputEventMouseButton:
		if event.pressed:
			check_box();

			
func _on_Timer_timeout():
	if(play):
		alive_process();
	for column in columns:
		for cell in column:
			if color:
				if !cell.state:
					cell.modulate = Color(lerp(cell.modulate, columns[selected[0]][selected[1]].deadColor, 0.45))
				else:
					cell.modulate = Color(lerp(cell.modulate, columns[selected[0]][selected[1]].aliveColor, 0.65))
			else:
				if cell.state:
					cell.modulate = Color(lerp(cell.modulate, Color(0, 0, 0), .45))
				else:
					cell.modulate = Color(lerp(cell.modulate, Color(1, 1, 1), .45))
