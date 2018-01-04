#crudApp/auth/views.py

from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user

from . import auth

from .forms import LoginForm, RegistrationForm
from crudApp import db
from crudApp.models import Employee

@auth.route("/register", methods=["GET", "POST"])
def register():
	"""
	Handles request to the /register route
	Adds an employee to the database through the registration form
	"""
	regForm = RegistrationForm()
	if regForm.validate_on_submit():
		employee = Employee(email=regForm.email.data, username=regForm.username.data, first_name=regForm.first_name.data, last_name=regForm.last_name.data, password=regForm.password.data)

		# add employee to database
		db.session.add(employee)
		db.session.commit()
		flash("You have successfully registered! You may now login.")

		# redirect to the login page
		return redirect(url_for("auth.login"))

	# load registration template
	return render_template("auth/register.html", form=regForm, title="Register")

@auth.route("/login", methods=["GET", "POST"])
def login():
	"""
	Handles request to the /login route
	Log an employee in through the login form
	"""
	liForm = LoginForm()
	if liForm.validate_on_submit():
		employee = Employee.query.filter_by(email=liForm.email.data).first()
		if employee is not None and employee.verify_password(liForm.password.data):
			login_user(employee)

			# redirect to the dashboard page after login
			if employee.is_admin:
				return redirect(url_for("home.admin_dashboard"))
			else:
				return redirect(url_for("home.dashboard"))
		else:
			flash("Invalid email or password.")

	# load login template
	return render_template("auth/login.html", form=liForm, title="Login")

@auth.route("/logout")
@login_required
def logout():
	"""
	Handles requests to the /logout route
	Log an employee out through the logout link
	"""
	logout_user()
	flash("You have successfully been logged out")

	# redirect to login page
	return redirect(url_for("auth.login"))