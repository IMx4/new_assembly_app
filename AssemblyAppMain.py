# Flask app to display pdf assembly sheets
from flask import Flask, render_template, redirect
import Data_Store as ds
import os

app = Flask(__name__)


# -- debug flask configurations --
# app.run(debug=True)
#app.config["TEMPLATES_AUTO_RELOAD"] = True


### Routes ###

@app.route('/', methods=['GET', 'POST'])
def index():
    name = load_data.get_job_name()
    cabs = load_data.get_assemblies_list()
    print(len(cabs))
    return render_template('index.html', cabs=cabs, name=name)


@app.route('/unit/<string:number>', methods=['POST', 'GET'])
def assembly(number):

    name = load_data.get_job_name()
    cabs = load_data.get_assemblies_dict()
    cab = cabs.get(number)
    status = cab.status
    print(status)
    return render_template('cab_sheet.html', sheet='Build_Sheets/' + number + '.pdf', status=status, number=number, name=name)


@app.route('/test/<string:value><string:num>', methods=['POST'])
def test(value, num):

    load_data.change_state(num, int(value))

    return redirect('/unit/' + num)


if __name__ == '__main__':

    load_data = ds.Data()
    app.run("localhost", 5000, debug=True)
