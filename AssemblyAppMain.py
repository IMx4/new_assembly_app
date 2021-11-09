# Flask app to display pdf assembly sheets
from flask import Flask, render_template, redirect
import Data_Store as ds
import PDF_Reader as reader
import os

app = Flask(__name__)


# -- debug flask configurations --
# app.run(debug=True)
#app.config["TEMPLATES_AUTO_RELOAD"] = True


### Routes ###

@app.route('/', methods=['GET', 'POST'])
def index():
    name = data.get_job_name()
    cabs = data.get_assemblies_list()
    return render_template('index.html', cabs=cabs, name=name)


@app.route('/unit/<string:number>', methods=['POST', 'GET'])
def assembly(number):

    name = data.get_job_name()
    cabs = data.get_assemblies_dict()
    cab = cabs.get(number)
    status = cab.status
    # print(status)
    return render_template('cab_sheet.html', sheet='Build_Sheets/' + number + '.pdf', status=status, number=number, name=name)


@app.route('/test/<string:toggle>/<string:num>', methods=['POST'])
def test(toggle, num):

    print(f' >>>>>>>>>>> {num}')
    data.change_state(num, int(toggle))

    return redirect('/unit/' + num)


if __name__ == '__main__':

    data = ds.Data()
    read_pdf = reader.pdf_reader(data)
    app.run("localhost", 5000, debug=True)
