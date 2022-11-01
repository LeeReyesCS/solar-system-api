from app import db
from app.models.planet import Planet
from flask import Blueprint, jsonify, abort, make_response, request

planet_bp = Blueprint("planet",__name__,url_prefix="/planets")

## Getting all planets and creating one planet
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
    
    return make_response(f"Planet {new_planet.name} successfully created", 201)

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

# # # update one planet
# @planet_bp.route('/<id>', methods=["PUT"])
# def update_one_planet(id):
#     planet = validate_planet(id)
#     request_body = request.get_json()
    
#     planet.name = request_body["name"]
#     planet.description = request_body["description"] 
#     planet.num_moons = request_body["num_moons"] 
#     # We never want to update an id. It's covered by postgreSQL
    
#     db.session.commit()
    
#     return make_response(f"Planet #{id} successfully updated", 200)

# ## delete planet
# @planet_bp.route("/<id>", methods=["DELETE"])
# def delete_planet(id):
#     planet = validate_planet(id) # call helper fx   
    
#     db.session.delete(planet)
#     db.session.commit()
    
#     return make_response(f"Planet #{id} successfully deleted", 202)

## Get, put, delete ONE planet
@planet_bp.route("/<id>", methods=["GET", "PUT", "DELETE"])
def handle_planet(id):
    planet = Planet.query.get(id)
    
    if request.method == "GET":
        return {
            "id": planet.id,
            "name": planet.name,
            "description": planet.description,
            "num_moons": planet.num_moons
        }
    elif request.method == "PUT":
        request_body = request.get_json()
        
        planet.name = request_body["name"]
        planet.description = request_body["description"] 
        planet.num_moons = request_body["num_moons"] 
        
        db.session.commit()
        
        return make_response(f"Planet #{id} successfully updated", 200)
    
    elif request.method == "DELETE":
        db.session.delete(planet)
        db.session.commit()
        return make_response(f"Planet #{id} successfully deleted", 202)    
            
            
        