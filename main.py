from flask import Flask, render_template, request
from locate import *

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('form.html')
    
@app.route("/data")
def data():
    if request.method == 'GET':
        return f"The URL /results accessed directly. Go to homepage and search."
    if request.method == 'POST':
        form_data = request.form
        postcode = request.form.get("Postcode")
        address = request.form.get("Address")
        results = get_results(address, postcode)
        return render_template('data.html', form_data = results)
    
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)