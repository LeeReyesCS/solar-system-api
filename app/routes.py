from flask import Blueprint, jsonify, abort, make_response


class Planet:
    def __init__(self, id, name, description, num_moons):
        self.id = id
        self.name = name
        self.description = description
        self.num_moons = num_moons

PLANETS = [
    Planet(1, "Mercury", "Closest to the Sun", 0),
    Planet(2, "Venus", "The Planet of Love", 0),
    Planet(3, "Earth", "The Planet of Life", 1),
    Planet(4, "Mars", "The Red Planet", 2),
    Planet(5, "Jupiter", "A gas giant planet", 57),
    Planet(6, "Saturn", "The Planet with Rings",63),
    Planet(7, "Uranus", "It's really cold here",27),
    Planet(8, "Neptune", "Dark, Cold, Ice Giant",14)
    ]

planet_bp = Blueprint("planet",__name__,url_prefix="/planets")

@planet_bp.route("", methods=["GET"])
def handle_planets():
    planet_response = [vars(planet) for planet in PLANETS]
    return jsonify(planet_response)

# read one planet
@planet_bp.route('/<id>', methods=["GET"])
def get_one_planet(id):
    planet = validate_planet(id)
    return planet

def validate_planet(id):
    try:
        planet_id = int(id)
    except ValueError:
        return {
            "message": "Invalid planet id"
        }, 400
        
    for planet in PLANETS:
        if planet.id == planet_id:
            return vars(planet)
        
    abort(make_response(jsonify(description="Resource not found"), 404))


