from flask import Flask, redirect, render_template, request, url_for
from databaseHandler import addPlantToDB, showNewPlants, showPlant
from uuid import uuid4

app = Flask(__name__)

@app.route("/")
def index():
    raw_data = showNewPlants()
    return render_template('index.html', raw_data=raw_data)

@app.route("/admin")
def admin():
    return render_template('admin.html')

@app.route("/plant/add/", methods=["POST"])
def addPlant():
    uuid = str(uuid4())
    plant_data = (uuid, request.form.get('eng-name'), request.form.get('local-name'), request.form.get('sci-name'), request.form.get('family'), request.form.get('category'), request.form.get('plant-image-paths'))
    # print(plant_data)
    addPlantToDB(plant_data[0],plant_data[1],plant_data[2],plant_data[3],plant_data[4],plant_data[5],plant_data[6])
    return redirect(url_for('plant', plant_id=uuid)) 

@app.route("/plant?<plant_id>", methods=["GET"])
def plant(plant_id):
    plant_data = None if plant_id is None else showPlant(plant_id)
    return render_template("_plant.html", plant_data=plant_data)

if __name__ == "__main__":
    app.run(debug=False)