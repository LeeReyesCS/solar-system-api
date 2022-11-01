from app import db
from app.models.planet import Planet
from flask import Blueprint, jsonify, abort, make_response, request

planet_bp = Blueprint("planet",__name__,url_prefix="/planets")

@planet_bp.route("", methods=["GET","POST"])
def handle_planets():
    if request.method == "GET":
        planets = Planet.query.all()
        planets_response = []
        for planet in planets:
            planets_response.append({
                "id": planet.id,
                "name": planet.name,
                "description": planet.description,
                "num_moons": planet.num_moons
            })
            
        return jsonify(planets_response)
    
    elif request.method == "POST":
        request_body = request.get_json()
        new_planet = Planet(name=request_body["name"],
                            description=request_body["description"],
                            num_moons=request_body["num_moons"])
    
        db.session.add(new_planet)
        db.session.commit()
    
    return make_response(f"Planet {new_planet.name} successfully create", 201)
    
# class Planet:
#     def __init__(self, id, name, description, num_moons):
#         self.id = id
#         self.name = name
#         self.description = description
#         self.num_moons = num_moons

# PLANETS = [
#     Planet(1, "Mercury", "Closest to the Sun", 0),
#     Planet(2, "Venus", "The Planet of Love", 0),
#     Planet(3, "Earth", "The Planet of Life", 1),
#     Planet(4, "Mars", "The Red Planet", 2),
#     Planet(5, "Jupiter", "A gas giant planet", 57),
#     Planet(6, "Saturn", "The Planet with Rings",63),
#     Planet(7, "Uranus", "It's really cold here",27),
#     Planet(8, "Neptune", "Dark, Cold, Ice Giant",14)
#     ]


# @planet_bp.route("", methods=["GET"])
# def handle_planets():
#     planet_response = [vars(planet) for planet in PLANETS]
#     return jsonify(planet_response)

# # read one planet
@planet_bp.route('/<id>', methods=["GET"])
def get_one_planet(id):
    planet = validate_planet(id)
    return planet

# helper fx
def validate_planet(id):
    try:
        planet_id = int(id)
    except ValueError:
        return {
            "message": "Invalid planet id"
        }, 400
        
    planet = Planet.query.get(id)
    
    if not planet:
        abort(make_response(jsonify(description="Resource not found"), 404))

    return planet

# # update one planet
@planet_bp.route('/<id>', methods=["PUT"])
def update_one_planet(id):
    planet = validate_planet(id)
    request_body = request.get_json()
    
    planet.name = request_body["name"]
    planet.description = request_body["description"] 
    planet.num_moons = request_body["num_moons"] 
    # We never want to update an id. It's covered by postgreSQL
    
    db.session.commit()
    
    return make_response(f"Planet #{id} successfully updated")

## delete planet
@planet_bp.route("/<id>", methods=["DELETE"])
def delete_plant(id):
    planet = validate_planet(id) # call helper fx   
    
    db.session.delete(planet)
    db.session.commit()
    
    return make_response(f"Planet #{id} successfully deleted")