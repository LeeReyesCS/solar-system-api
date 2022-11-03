from app.models.planet import Planet

def test_get_all_planets_with_empty_db_return_empty_list(client):
    #'client' is the ficture we registered fromt he conftest.py
    # pytest automatically tries to match each test param to a
    # fixture with the same name.
    
    response = client.get('/planets') 
    
    response_body = response.get_json()
    
    assert response_body == []
    assert response.status_code == 200
    
def test_get_one_planet(client, two_saved_planets):
    # Act
    response = client.get('/planets/1') 
    response_body = response.get_json()
    
    planet1 = {
        "id": 1,
        "name": "winston",
        "description": "terrier",
        "num_moons": 100}
    
    # Assert
    assert response.status_code == 200
    assert response_body == planet1