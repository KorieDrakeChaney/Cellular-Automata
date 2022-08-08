extends MeshInstance2D

var state : int = 0;
var prevState : int;
var pos : Vector2;
var deadColor : Color;
var aliveColor : Color;
var index : int;

func _ready():
	randomize()
	deadColor = Color(rand_range(0.1, 0.5), rand_range(0.1, 0.5), rand_range(0.1, 0.5), 0.875);
	aliveColor = Color(rand_range(0.5, 1), rand_range(0.5, 1), rand_range(0.5, 1), 1);
	scale = Vector2(3, 3)
