from flask import Flask, render_template, request
from locate import *

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('form.html')
    
@app.route("/results", methods=['GET', 'POST'])
def results():
    if request.method == 'GET':
        return f"The URL /results accessed directly. Go to homepage and search."
    if request.method == 'POST':
        postcode = request.form.get("Postcode")
        address = request.form.get("Address")
        results = get_results(address, postcode)
        if len(results) == 0:
            return render_template('no-results.html')
        else:
            return render_template('results.html', tables=[results.to_html(index=False, classes='data')], titles=results.columns.values)
        
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)