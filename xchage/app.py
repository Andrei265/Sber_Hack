from collections import namedtuple

from flask import Flask, render_template, redirect, url_for, request, make_response
from flask_sqlalchemy import SQLAlchemy
import authentication_module
import urllib.parse

from asink_h1h import parser_1


txt = ''
tg = ''
reg = ''
pas = ''
inic = ''
comp = ''
adr = ''
em = ''
nut = ''
rrr = ''
sss = ''
check = 0

app = Flask(__name__)

Prof = namedtuple('prof', 'text tag')
profs = []

Reg = namedtuple('reg', 'Username Password Registered Sign_Up')
regs = []


Dop_data = namedtuple('dd', 'Inicial Company Adres Pochta Num_tel')
dop_datas = []


@app.route("/", methods=['GET'])
def index():
	conten = render_template('index.html', profs=profs, regs = regs, dop_datas = dop_datas)
	res = make_response(conten)
	res.headers['Content'] = 'text/plain'
	return res


@app.route("/about")
def about():
    return "<h1>About site</h1>"


@app.route("/add_prof", methods=['POST'])
def add_prof():
	global txt, tg

	text = request.form['text']
	tag = request.form['tag']
	txt = text
	tg = tag

	profs.append(Prof(text, tag))
	parser_1(txt, tg)

	return redirect(url_for('index'))


@app.route("/autorisation", methods=['POST'])
def autorisation():
	global reg, pas, rrr, sss, inic, comp, adr, em, nut, check

	Username = request.form['Username']
	Password = request.form['Password']
	try:
		Registered = request.form['Registered']
	except:
		Sign_Up = request.form['Sign_Up']
	try:
		Sign_Up = request.form['Sign_Up']
	except:
		Registered = request.form['Registered']
	Inicial = request.form['Inicial']
	Company = request.form['Company']
	Adres = request.form['Adres']
	Pochta = request.form['Pochta']
	Num_tel = request.form['Num_tel']

	reg = Username
	pas = Password
	try:
		rrr = Registered
		check = 1
		Sign_Up = 1
	except:
		sss = Sign_Up
		check = 0
		Registered = 1
	inic = Inicial
	comp = Company
	adr = Adres
	em = Pochta
	nut = Num_tel

	db_auth = authentication_module.Authentication_Table()
	db_auth.close_connection()
	
	if Registered == 'Login':
		db_auth.connect()
		print(db_auth.sign_in_or_check(Username, Password, 'SIGN_IN'))
		db_auth.close_connection()
	else:
		db_auth.connect()
		print(db_auth.sign_in_or_check(Username, Password, 'REGISTRATION'))
		db_auth.close_connection()

	regs.append(Reg(Username, Password, Registered, Sign_Up))
	dop_datas.append(Dop_data(Inicial, Company, Adres, Pochta, Num_tel))
	print(Username, Password, Registered, Sign_Up, Inicial, Company, Adres, Pochta, Num_tel)
	return redirect(url_for('index'))


if __name__ == "__main__":
	app.run(debug=True)