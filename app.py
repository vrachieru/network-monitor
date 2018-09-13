from os import environ
from datetime import datetime
from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from speedtest import Speedtest

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "database.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)

scheduler = BackgroundScheduler(daemon=True)
scheduler.start()


class Speed(db.Model):
    timestamp = db.Column(db.DateTime(), unique=True, nullable=False, primary_key=True)
    ping = db.Column(db.Float(), unique=False, nullable=False, primary_key=False)
    download = db.Column(db.Float, unique=False, nullable=False, primary_key=False)
    upload = db.Column(db.Float, unique=False, nullable=False, primary_key=False)


@scheduler.scheduled_job(id='speedtest', trigger=CronTrigger.from_crontab(environ.get('SPEEDTEST_CRON', '0 * * * *')))
def speedtest_job():
    speedtest = Speedtest()
    speedtest.get_servers()
    speedtest.get_best_server()
    speedtest.download()
    speedtest.upload()

    result = {
        'download': round(speedtest.results.download / 1000.0 / 1000.0, 2), # Mbit/s
        'upload': round(speedtest.results.upload / 1000.0 / 1000.0, 2), # Mbit/s
        'ping': speedtest.results.ping, # ms
        'timestamp': datetime.now()
    }

    try:
        db.session.add(Speed(**result))
        db.session.commit()
    except Exception as e:
        print(e)
        print('Failed to log speedtest')


@app.route('/')
def home():
  return render_template('index.html', speedtests=Speed.query.all())

@app.route('/db/initialize')
def initialize_db():
  db.create_all()
  return 'OK'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
