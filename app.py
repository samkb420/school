#importing required modules
import os

from flask import Flask, url_for,redirect,jsonify
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#project_dir = os.path.dirname(os.path.abspath(__file__))
#database_file = "sqlite:///{}".format(os.path.join(project_dir, "students.db"))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///students.db'
db = SQLAlchemy(app)

class Students(db.Model):
	"""docstring for Students"""
	id=db.Column(db.Integer,primary_key=True)
	name=db.Column(db.String(80),nullable=False)
	Class=db.Column(db.String(80),nullable=False)
	fee=db.Column(db.Integer,nullable=False)

	def __repr__(self):
		return "<Student %r>" % self.id





@app.route('/')

def Home():
	#render index page
	return render_template('index.html')
@app.route('/Student') #table
def Student():
	#fetch all student in table
	students=Students.query.order_by(Students.id).all()

	return render_template('students.html',students=students)
@app.route('/Add_Students',methods=['POST','GET']) #table
def Add_Students():

	if request.method == 'POST':
		stud_name=request.form['name']
		stud_class=request.form['Class']
		stud_fee=request.form['fee']
		
		new_stud=Students(name=stud_name,Class=stud_class,fee=stud_fee)

		try:

			db.session.add(new_stud)
			db.session.commit()

			return redirect('/Student')
		except:
			return "Error occured plz try again"
	else:
		return render_template('add_student.html')
	#fetch all student in table
@app.route('/delete/<int:id>')
def delete(id):
	students_to_del=Students.query.get_or_404(id)
	try:
		db.session.delete(students_to_del)
		db.session.commit()
		return redirect('/Student')
	except:
		return "There was a Problem in Deleting."
@app.route('/update/<int:id>',methods=['POST','GET'])
def update(id):
	student=Students.query.get_or_404(id)
	if request.method=='POST':
		student.name=request.form['name']
		student.Class=request.form['Class']
		student.fee=request.form['fee']
		student.new_stud=Students(name=student.name,Class=student.Class,fee=student.fee)
		try:
			db.session.commit()
			return redirect('/Student')
		except:
			return 'error'
	else:
		return render_template('update_student.html',student=student)

		

if __name__=='__main__':
	app.run(debug=True)
