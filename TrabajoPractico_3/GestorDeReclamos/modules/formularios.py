from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField
from wtforms.validators import DataRequired, EqualTo, Email, Length

class FormRegistro(FlaskForm):
    nombre = StringField(label="Nombre", validators=[DataRequired()])
    nombreDeUsuario = StringField(label = "Nombre De Usuario", validators=[DataRequired()])
    email = StringField(label="Email", validators=[DataRequired(), Email()])
    claustro = StringField(label = "Claustro", validators = [DataRequired()])
    contraseña = PasswordField(label='Contraseña', validators=[DataRequired(), Length(min=4), EqualTo('confirmacion', message='Las contraseñas deben coincidir')])
    confirmacion = PasswordField(label='Repetir contraseña', validators=[DataRequired()])
    submit = SubmitField(label='Registrar')

class FormLogin(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    contraseña = PasswordField(label='contraseña', validators=[DataRequired(), Length(min=4)])
    submit = SubmitField(label='Ingresar')
