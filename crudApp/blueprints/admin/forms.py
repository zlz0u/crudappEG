# crudApp/blueprints/admin/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
# from wtforms.ext.sqlalchemy.fields import QuerySelectField --> old version
from wtforms_sqlalchemy.fields import QuerySelectField


from crudApp.models import Department, Role

class DepartmentForm(FlaskForm):
	"""
	Form for admin to add or edit a department
	"""
	name = StringField("Name", validators=[DataRequired()])
	description = StringField("Description", validators=[DataRequired()])
	submit = SubmitField("Submit")

class RoleForm(FlaskForm):
	"""
	Form for admin to add or edit a role
	"""
	name = StringField("Name", validators=[DataRequired()])
	description = StringField("Description", validators=[DataRequired()])
	submit = SubmitField("Submit")

class EmployeeAssignForm(FlaskForm):
	"""
	Form for admin to assign departments and roles to employees 
	"""
	department = QuerySelectField(query_factory=lambda: Department.query, get_label="name", allow_blank=False)
	role = QuerySelectField(query_factory=lambda: Role.query, get_label="name", allow_blank=True)
	submit = SubmitField("Submit")