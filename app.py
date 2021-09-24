from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail
from datetime import date

app = Flask(__name__)

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:goodgirL6@localhost/Tamu-basic'
else:
    app.debug = False
    SQLALCHEMY_DATABASE_URI = 'postgres://clrgatshhkcbiq:8771ff5375b1dcf81a263f9dfd182471ef2febdd8f1071bd157da1a6eabdd949@ec2-34-234-12-149.compute-1.amazonaws.com:5432/d3udt3305d83d7'.replace("://", "ql://", 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Feedback(db.Model):
    __tablename__ = 'feedback'
    id=db.Column(db.Integer, primary_key=True, unique = True)
    student = db.Column(db.String(200), unique = False)
    lect = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())
    muddiest = db.Column(db.Text())
    date = db.Column(db.Date())
    def __init__(self, student, lect, rating, comments, muddiest, date):
        self.student = student
        self.lect = lect
        self.rating = rating
        self.comments = comments
        self.muddiest = muddiest
        self.date = date
@app.route('/')
def index():
  return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        student = request.form['student']
        lect = request.form['lect']
        rating = request.form['rating']
        comments = request.form['comments']
        muddiest = request.form['muddiest']
        date = request.form['date']
        #print(student, lect, rating, comments)
        if student == '' or lect =='':
            return render_template('index.html', message='Please fill in the required fields.')
        if db.session.query(Feedback).filter(Feedback.student == student).filter(Feedback.date == date).count() == 0:
            data = Feedback(student,lect, rating, comments, muddiest, date)
            db.session.add(data)
            db.session.commit()
            send_mail(student, lect, rating, comments, muddiest, date)
            return render_template('success.html')
        data = Feedback(student,lect, rating, comments, muddiest, date)
        db.session.update(data)
        db.session.commit()
        return render_template('index.html', message='You have already submitted the feedback. Thanks')
if __name__ == '__main__':
  app.debug=True
  app.run()
