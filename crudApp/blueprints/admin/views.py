# crudApp/blueprints/admin/views

from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import admin

from .forms import DepartmentForm, RoleForm, EmployeeAssignForm
from crudApp import db
from crudApp.models import Department, Role, Employee

def check_admin():
	"""
	Prevent non-admins from accessing this page
	"""
	if not current_user.is_admin:
		abort(403)


##### DEPARTMENT #####
##### DEPARTMENT #####


# LIST departments
@admin.route("/departments", methods=["GET", "POST"])
@login_required
def list_departments():
	"""
	List all Departments
	"""
	check_admin()
	departments = Department.query.all()

	return render_template("admin/departments/departments.html", departments=departments, title="Departments")

# ADD department
@admin.route("/departments/add", methods=["GET", "POST"])
@login_required
def add_department():
	"""
	Add a department to database
	"""
	check_admin()

	add_department = True

	deptForm = DepartmentForm()
	if deptForm.validate_on_submit():
		department = Department(name=deptForm.name.data, description=deptForm.description.data)
		try:
			# add department to database
			db.session.add(department)
			db.session.commit()
			flash("You have successfully added a new department.")
		except:
			flash("Error: Department name already exists.")
	
		# redirect to departments page
		return redirect(url_for("admin.list_departments"))
	
	# load department template
	return render_template("admin/departments/department.html", action="Add", add_department=add_department, form=deptForm, title="Add Department")

# EDIT department
@admin.route("/departments/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_department(id):
	"""
	Edit a department
	"""	
	check_admin()

	add_department = False

	department = Department.query.get_or_404(id)
	deptForm = DepartmentForm(obj=department)
	if deptForm.validate_on_submit():
		department.name = deptForm.name.data
		department.description = deptForm.description.data
		db.session.commit()
		flash("You have successfully edited the department")

		# redirect to the departments page
		return redirect(url_for("admin.list_departments"))

	deptForm.description.data = department.description
	deptForm.name.data = department.name
	return render_template("admin/departments/department.html", action="Edit", add_department=add_department, form=deptForm, department=department, title="Edit Department")

# DELETE departments
@admin.route("/departments/delete/<int:id>", methods=["GET", "POST"])
@login_required
def delete_department(id):
	"""
	Delete a department
	"""
	check_admin()

	department = Department.query.get_or_404(id)
	db.session.delete(department)
	db.session.commit()
	flash("You have successfully delete the department.")

	# redirect to the departments page
	return redirect(url_for("admin.list_departments"))

	return render_template(title="Delete Department")


##### ROLE #####
##### ROLE #####

# LIST all roles
@admin.route("/roles")
@login_required
def list_roles():
	"""
	List all roles
	"""
	check_admin()

	qRoles = Role.query.all()
	return render_template("admin/roles/roles.html", roles=qRoles, title="Roles")

# ADD new role
@admin.route("/roles/add", methods=["GET", "POST"])
@login_required
def add_role():
	"""
	Add new role
	"""
	check_admin()

	add_role = True

	rForm = RoleForm()
	if rForm.validate_on_submit():
		role = Role(name=rForm.name.data, description=rForm.description.data)
		try:
			db.session.add(role)
			db.session.commit()
			flash("You have successfully added a new role.")
		except:
			flash("Error: role name already exists.")

		return redirect(url_for("admin.list_roles"))

	return render_template("admin/roles/role.html", add_role=add_role, form=rForm, title="Add Role")

# EDIT a role
@admin.route("/roles/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_role(id):
	"""
	Edit a role
	"""
	check_admin()

	add_role = False

	role = Role.query.get_or_404(id)
	rForm = RoleForm(obj=role)
	if rForm.validate_on_submit():
		role.name = rForm.name.data
		role.description = rForm.description.data
		db.session.add(role)
		db.session.commit()
		flash("You have successfully edited the role.")

		return redirect(url_for("admin.list_roles"))

	rForm.name.data = role.name
	rForm.description.data = role.description
	return render_template("admin/roles/role.html", add_role=add_role, form=rForm, title="Edit Role")

@admin.route("/roles/delete/<int:id>", methods=["GET", "POST"])
@login_required
def delete_role(id):
	check_admin()

	role = Role.query.get_or_404(id)
	db.session.delete(role)
	db.session.commit()
	flash("You have successfully deleted the role.")

	return redirect(url_for("admin.list_roles"))

	return render_template(title="Delete Role")


##### EMPLOYEE #####
##### EMPLOYEE #####
@admin.route("/employees")
@login_required
def list_employees():
	"""
	List all employees
	"""
	check_admin()

	employees = Employee.query.all()
	return render_template("admin/employees/employees.html", employees=employees, title="Employees")

@admin.route("/employees/assign/<int:id>", methods=["GET", "POST"])
@login_required
def assign_employee(id):
	"""
	Assign a department and a role to an employee
	"""
	check_admin()

	employee = Employee.query.get_or_404(id)

	# prevent admin from being assigned to a department or role
	if employee.is_admin:
		abort(403)

	eaForm = EmployeeAssignForm(obj=employee)
	if eaForm.validate_on_submit():
		employee.department = eaForm.department.data
		employee.role = eaForm.role.data
		db.session.add(employee)
		db.session.commit()
		flash("You have successfully assigned a department and role.")

		return redirect(url_for("admin.list_employees"))
		
	return render_template("admin/employees/employee.html", employee=employee, form=eaForm, title="Assign Employee")
