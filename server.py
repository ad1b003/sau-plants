from flask import Flask, redirect, render_template, request, session, url_for
from databaseHandler import addPlantToDB, getSecret, searchPlants, searchPlantsWhere, showNewPlants, showPlant
from uuid import uuid4
import os

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY')

@app.route("/")
def index():
    raw_data = showNewPlants()
    # return raw_data
    return render_template('index.html', raw_data=raw_data)

@app.route("/admin")
def admin():
    if session.get('user') is None:
        return render_template('admin.html')
    else:
        return render_template('admin.html', session=session.get('user'))
    
@app.route("/in", methods=["POST"])
def getIn():
    if request.form.get('secret') == getSecret():
        session['user'] = 'admin'
        return redirect(url_for('admin'))
    else:
        return "get out"
    
@app.route("/out")
def getOut():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route("/plant/add/", methods=["POST"])
def addPlant():
    if session.get('user') is None: redirect(url_for('index'))
    uuid = str(uuid4())
    plant_data = (uuid, request.form.get('eng-name'), request.form.get('local-name'), request.form.get('sci-name'),
                  request.form.get('family'), request.form.get('categories'), request.form.get('plant-image-paths'))
    addPlantToDB(*plant_data)
    return redirect(url_for('plant', plant_id=uuid))

@app.route("/plant:<plant_id>", methods=["GET"])
def plant(plant_id):
    previous_page = request.headers.get('Referer', url_for('index'))
    plant_data = None if plant_id is None else showPlant(plant_id)
    # return plant_data
    return render_template("_plant.html", plant_data=plant_data, previous_page=previous_page)

@app.route('/searchPage')
def searchPage():
    # return searchPlants(where, term)
    return render_template('_search.html')

@app.route('/search')
def search():
    search_term = request.args.get('search_term')
    return render_template('_search_result.html', search_results=searchPlants(search_term)) if search_term else []

@app.route('/search/<where>/<term>', methods=['GET'])
def searchBy(where:str, term: str):
    # return searchPlants(where, term)
    return render_template('_search_result.html', where=str(where), search_term=term, search_results=searchPlantsWhere(where, term))

if __name__ == "__main__":
    app.run()
