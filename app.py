from flask import Flask, request, jsonify, render_template
from models import util


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('app.html')

@app.route('/get_location_names', methods=['GET'])
def get_location_names():
    response = jsonify({
        'locations': util.get_locations()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


@app.route('/get_area_type', methods=['GET'])
def get_area_type():
    response = jsonify({
        'area_type': util.get_area_type()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


@app.route('/get_availability', methods=['GET'])
def get_availability():
    response = jsonify({
        'availability': util.get_availability()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response



@app.route('/predict_home_price', methods=['GET', 'POST'])
def predict_home_price():
     if request.method=='GET':
        return render_template('home.html')
     else:
        size = int(request.form['size'])
        total_sqft = float(request.form['total_sqft'])
        bath = int(request.form['bath'])
        balcony = int(request.form['balcony'])
        area_type = request.form['area_type']
        location = request.form['location']
        month_availability = request.form['month_availability']

        response = jsonify({
            'estimated_price': util.predict_price(**{'size': size, 'total_sqft': total_sqft, 'bath': bath, 'balcony': balcony,\
                                                    'area_type': area_type, 'location': location, 'month_availability': month_availability})
        })
        response.headers.add('Access-Control-Allow-Origin', '*')

        return response

if __name__ == "__main__":
    print("Starting Python Flask Server For Home Price Prediction...")
    util.load_saved_artifacts()
    app.run(host = "0.0.0.0", port = 8080)
