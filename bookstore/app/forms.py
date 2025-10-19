from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, Length

class RegisterForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Телефон', validators=[DataRequired(), Length(min=10, max=20)])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Зарегистрироваться')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')

class ReviewForm(FlaskForm):
    rating = SelectField('Оценка', choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], coerce=int, validators=[DataRequired()])
    comment = TextAreaField('Отзыв')
    submit = SubmitField('Оставить отзыв')

class OrderForm(FlaskForm):
    delivery_type = SelectField('Доставка', choices=[('самовывоз', 'Самовывоз'), ('до двери', 'До двери')], validators=[DataRequired()])
    address = StringField('Адрес (если до двери)')
    submit = SubmitField('Оформить заказ')