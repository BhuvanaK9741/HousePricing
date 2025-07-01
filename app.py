from flask import Flask ,render_template,request
import pickle


app=Flask(__name__)

@app.route("/",methods=['GET'])
def index():
    return render_template('index.html')

@app.route("/about",methods=['GET'])
def about():
    return render_template('about.html')


#contact
@app.route("/contact",methods=['GET'])
def contact():
    return render_template('contact.html')

#methodology
@app.route("/methodology",methods=['GET'])
def methodology():
    return render_template('methodology.html')

#predict
with open("house-rf-model.pkl","rb") as f:
    model=pickle.load(f)

def predict_house_price(area=7420, bedrooms=4, bathrooms=2, stories=3,
                        mainroad=1, guestroom=0, basement=0, hotwaterheating=0,
                        airconditioning=1, parking=2, prefarea=1, furnishingstatus='unfurnished'):

    def yes_no_to_int(val):
        if isinstance(val, str):
            return 1 if val.lower() == 'yes' else 0
        return val

    furnishing_map = {
        'unfurnished': 0,
        'semi-furnished': 1,
        'furnished': 2
    }

    mainroad = yes_no_to_int(mainroad)
    guestroom = yes_no_to_int(guestroom)
    basement = yes_no_to_int(basement)
    hotwaterheating = yes_no_to_int(hotwaterheating)
    airconditioning = yes_no_to_int(airconditioning)
    prefarea = yes_no_to_int(prefarea)

    if isinstance(furnishingstatus, str):
        furnishingstatus = furnishing_map.get(furnishingstatus.lower(), 0)  # default 0 if unknown

    features = [
        area,
        bedrooms,
        bathrooms,
        stories,
        mainroad,
        guestroom,
        basement,
        hotwaterheating,
        airconditioning,
        parking,
        prefarea,
        furnishingstatus
    ]

    prediction = model.predict([features])
    return prediction[0]


@app.route("/predict", methods=['GET', 'POST'])
def predict():
    res = None  
    if request.method == 'POST':
        # Extract form data
        price = None  # Usually this is the output, so we don't extract it
        area = float(request.form.get('area'))
        bedrooms = int(request.form.get('bedrooms'))
        bathrooms = int(request.form.get('bathrooms'))
        stories = int(request.form.get('stories'))
        mainroad = request.form.get('mainroad')  # Expecting 'yes'/'no'
        guestroom = request.form.get('guestroom')
        basement = request.form.get('basement')
        hotwaterheating = request.form.get('hotwaterheating')
        airconditioning = request.form.get('airconditioning')
        parking = int(request.form.get('parking'))
        prefarea = request.form.get('prefarea')
        furnishingstatus = request.form.get('furnishingstatus')

        # Predict using model
        res = predict_house_price(area, bedrooms, bathrooms, stories,
                            mainroad, guestroom, basement,
                            hotwaterheating, airconditioning, parking,
                            prefarea, furnishingstatus)
        print("Predicted House Price:", res)

    return render_template('predict.html', prediction=res)



if __name__=='__main__':
    app.run(debug=True,port=3500)