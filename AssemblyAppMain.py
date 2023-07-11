# Flask app to display pdf assembly sheets
from flask import Flask, render_template, redirect, url_for, session
import Data_Store as ds
import PDF_Reader as reader
from flask import request
from threading import Thread, Lock
from datetime import timedelta


app = Flask(__name__)
app.secret_key = "theKey"
app.permanent_session_lifetime = timedelta(seconds=14)

data = ds.Data()
users = data.get_users()


### Routes ###
@app.route('/', methods=['GET', 'POST'])
def index():

    data = ds.Data()
    jobs = data.get_jobs()

    return render_template('index.html', jobs=jobs)


@app.route('/jobs/<string:name>', methods=['GET', 'POST'])
def job(name):

    data = ds.Data()
    assemblies_dict = {}

    if len(assemblies_dict) == 0:
        assemblies_dict = data.load_job(name)
    assemblies = [v for v in assemblies_dict.values()]
    return render_template('job.html', cabs=assemblies, name=name)


@app.route('/unit/<string:name>/<string:number>', methods=['GET', 'POST'])
def user(name, number):

    return render_template('users.html', users=users, number=number, name=name)


@app.route('/unit/<string:name>/<string:number>/<string:user>', methods=['GET', 'POST'])
def assembly(name, number, user):

    session[f'{user}'] = user
    data = ds.Data()
    assemblies_dict = data.load_job(name)
    status = assemblies_dict[number].get_assembly_status()

    os_type = request.headers.get('User-Agent')
    if 'Android' in os_type:
        print('Android')
        return render_template('cab_sheet.html', sheet=f'Build_Sheets/{name}/{number}.png', status=status, number=number, name=name, user=user)

    return render_template('cab_sheet.html', sheet=f'Build_Sheets/{name}/{number}.pdf', status=status, number=number, name=name, user=user)


@app.route('/cab/<string:toggle>/<string:num>/<string:name>/<string:user>/<string:part>', methods=['POST'])
def cab(toggle, num, name, user, part):

    if user not in session:
        return redirect(url_for('index'))

    assemblies_dict = data.load_job(name)
    cabinet = assemblies_dict.get(num)
    cabinet.set_complete(toggle)
    data.write_log(name, num, part, user)
    print(f'Toggle: {toggle} - Number: {num}')

    lock = Lock()
    t = Thread(target=data.write_status, args=(assemblies_dict, name, lock))
    t.start()
    t.join()

    return redirect(f'/unit/{name}/{num}/{user}')


@app.route('/load', methods=['GET'])
def load():
    read_pdf = reader.pdf_reader()
    return redirect(url_for('index'))


@app.route('/logs', methods=['GET'])
def logs():
    name = request.args.get('name')
    logs = data.get_logs(name)
    return render_template('logs.html', logs=logs)


if __name__ == '__main__':

    app.run(host="0.0.0.0", port=5000, debug=True)
