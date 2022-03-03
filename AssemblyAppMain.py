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
    data = ds.Data()
    jobs = data.get_jobs()
    return render_template('index.html', jobs=jobs)


@app.route('/<string:name>', methods=['GET', 'POST'])
def job(name):

    data = ds.Data()
    assemblies_dict = data.load_job(name)
    assemblies = [v for v in assemblies_dict.values()]
    return render_template('job.html', cabs=assemblies, name=name)


@app.route('/unit/<string:name>/<string:number>', methods=['POST', 'GET'])
def assembly(name, number):
    data = ds.Data()

    assemblies = data.load_job(name)
    status = assemblies[number].get_assembly_status()
    return render_template('cab_sheet.html', sheet=f'Build_Sheets/{name}/' + number + '.pdf', status=status, number=number, name=name)


@app.route('/test/<string:toggle>/<string:num>', methods=['POST'])
def test(toggle, num):
    data = ds.Data()
    print(f' >>>>>>>>>>> {num}')
    data.change_state(num, int(toggle))

    return redirect('/unit/' + num)


if __name__ == '__main__':
    read_pdf = reader.pdf_reader()
    app.run("localhost", 5000, debug=True)
