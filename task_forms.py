from flask_wtf import FlaskForm
from wtforms import DateField, RadioField, StringField
from wtforms.validators import DataRequired, Optional


class TaskEditForm(FlaskForm):
    description = StringField("Task description", validators=[DataRequired()])
    due_date = DateField("Due date", validators=[Optional()])
    priority = RadioField(
        "Enter priority",
        choices=[("H", "High"), ("M", "Medium"), ("L", "Low")],
        validators=[Optional()],
    )
    email_date = DateField("Date of email", validators=[Optional()])
    tags = StringField("Enter tags (seperated by commas)", validators=[Optional()])
    project = StringField("Enter project", validators=[Optional()])
    annotate = StringField("Enter annotations", validators=[Optional()])
    wait_date = DateField("Enter wait date", validators=[Optional()])
