from tzlocal import get_localzone
from flask import Flask, request, render_template
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import uuid
import json
from collections import OrderedDict
from flask_socketio import SocketIO, emit
from utils.db.database import db_session, init_db
from utils.db.models import Button
from utils.vmix.functions import runScheduleTask


app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

tz = get_localzone()

scheduler = BackgroundScheduler({'apscheduler.timezone': tz})
scheduler.add_jobstore('sqlalchemy', url='sqlite:///schedule.db')
scheduler.start()


def sqlalchemyToJSON(self):
    result = OrderedDict()
    for key in self.__mapper__.c.keys():
        result[key] = getattr(self, key)
    return json.dumps(result)


def POSTtoVMix(one, two, three, four):
    print('posting')

def intervalTest(one,two, three, four):
    print(datetime.now())


@app.route('/')
def index():
    buttons = Button.query.all()
    jobs = scheduler.get_jobs()
    print(buttons)
    return render_template('index.html', jobs=jobs, buttons=buttons)


@app.route('/formSubmit', methods=['POST'])
def schedule():
    form = request.form.to_dict()
    print(form)

    id = str(uuid.uuid4())

    if form['action-type'] == 'create-button':

        new_button = Button(id=id, name=form['event-name'], url=form['api-url'])

        db_session.add(new_button)
        db_session.commit()

        socket_message = {"type": "button", "attributes": json.loads(sqlalchemyToJSON(new_button))}

        socketio.emit('message', socket_message, namespace='/event')

        return sqlalchemyToJSON(new_button), 200

    else:
        start = datetime.strptime(form['start-time-selector'], '%Y-%m-%dT%H:%M')
        if form['interval'] != '':
            name = form['event-name']
            if form['end-time-selector'] != '':
                end = datetime.strptime(form['end-time-selector'], '%Y-%m-%dT%H:%M')
                job = scheduler.add_job(runScheduleTask, trigger='interval', next_run_time=datetime.strptime(form['start-time-selector'], '%Y-%m-%dT%H:%M'), end_date=datetime.strptime(form['end-time-selector'], '%Y-%m-%dT%H:%M') , seconds=int(form['interval']), args=[name, form['api-url'], form['interval'], id])
                socket_message = {"type": "interval", "attributes": {"id": job.id, "name": name, "time": start.strftime('%d-%m-%Y %H:%M'), "end_time": end.strftime('%d-%m-%Y %H:%M'), "interval": form['interval']}}
            else:

                job = scheduler.add_job(runScheduleTask, trigger='interval', next_run_time=datetime.strptime(form['start-time-selector'], '%Y-%m-%dT%H:%M'), seconds=int(form['interval']), args=[name, form['api-url'], form['interval'], id])

                socket_message = {"type": "interval", "attributes": {"id": job.id, "name": name, "time": start.strftime('%d-%m-%Y %H:%M'), "end_time": "", "interval": form['interval']}}
            socketio.emit('message', socket_message, namespace='/event')
        else:
            if form['start-time-selector'] != '' and form['end-time-selector'] != "":
                name = form['event-name'] + ' [Start]'
            else:
                name = form['event-name']

            job = scheduler.add_job(runScheduleTask, trigger='date', next_run_time=datetime.strptime(form['start-time-selector'],'%Y-%m-%dT%H:%M'),args=[name, form['api-url'], '', id])

            socket_message = {"type": "schedule", "attributes": {"id": job.id, "name": name, "time": start.strftime('%d-%m-%Y %H:%M')}}
            socketio.emit('message', socket_message, namespace='/event')

            if form['end-time-selector'] != "":
                end = datetime.strptime(form['end-time-selector'], '%Y-%m-%dT%H:%M')
                id = str(uuid.uuid4())
                name = form['event-name'] + ' [Stop]'

                job = scheduler.add_job(runScheduleTask, trigger='date',next_run_time=datetime.strptime(form['end-time-selector'], '%Y-%m-%dT%H:%M'),args=[name, form['api-url'], '',  id])

                socket_message = {"type": "schedule", "attributes": {"id": job.id, "name": name, "time": end.strftime('%d-%m-%Y %H:%M')}}
                socketio.emit('message', socket_message, namespace='/event')


    return 'Scheduled'


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@socketio.on('create', namespace='/event')
def lightsUpdateEvent(msg):
    print(msg['data'])


@socketio.on('connect', namespace='/event')
def connect():
    emit('my response', {'data': 'Connected', 'count': 0})


@socketio.on('disconnect', namespace='/event')
def disconnect():
    print('Client disconnected')

# run Flask db
if __name__ == "__main__":
    init_db()
    socketio.run(app, host='0.0.0.0')