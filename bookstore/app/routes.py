from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import User, Book, Genre, CartItem, Order, OrderItem, Review
from .forms import RegisterForm, LoginForm, ReviewForm, OrderForm

main = Blueprint('main', __name__)
auth = Blueprint('auth', __name__)

@main.route('/')
def index():
    top_books = Book.query.order_by(Book.rating.desc()).limit(3).all()
    genres = Genre.query.all()
    return render_template('index.html', top_books=top_books, genres=genres)

@main.route('/catalog')
def catalog():
    genre_id = request.args.get('genre', type=int)
    if genre_id:
        books = Book.query.join(Book.genres).filter(Genre.id == genre_id).all()
    else:
        books = Book.query.all()
    genres = Genre.query.all()
    return render_template('catalog.html', books=books, genres=genres, selected_genre=genre_id)

@main.route('/book/<int:book_id>', methods=['GET', 'POST'])
def book_detail(book_id):
    book = Book.query.get_or_404(book_id)
    review_form = ReviewForm()
    if review_form.validate_on_submit() and current_user.is_authenticated:
        existing = Review.query.filter_by(user_id=current_user.id, book_id=book.id).first()
        if existing:
            flash('Вы уже оставляли отзыв на эту книгу.', 'warning')
        else:
            review = Review(
                rating=review_form.rating.data,
                comment=review_form.comment.data,
                user_id=current_user.id,
                book_id=book.id
            )
            db.session.add(review)
            reviews = Review.query.filter_by(book_id=book.id).all()
            book.rating = round(sum(r.rating for r in reviews) / len(reviews), 1)
            book.review_count = len(reviews)
            db.session.commit()
            flash('Спасибо за отзыв!', 'success')
        return redirect(url_for('main.book_detail', book_id=book_id))
    return render_template('book_detail.html', book=book, form=review_form)

@main.route('/add_to_cart/<int:book_id>')
@login_required
def add_to_cart(book_id):
    item = CartItem.query.filter_by(user_id=current_user.id, book_id=book_id).first()
    if item:
        item.quantity += 1
    else:
        item = CartItem(user_id=current_user.id, book_id=book_id, quantity=1)
        db.session.add(item)
    db.session.commit()
    flash('Книга добавлена в корзину!', 'success')
    return redirect(url_for('main.book_detail', book_id=book_id))

@main.route('/cart')
@login_required
def cart():
    items = CartItem.query.filter_by(user_id=current_user.id).all()
    total = sum(item.book.price * item.quantity for item in items)
    return render_template('cart/view.html', items=items, total=total)

@main.route('/cart/remove/<int:item_id>')
@login_required
def remove_from_cart(item_id):
    item = CartItem.query.get_or_404(item_id)
    if item.user_id == current_user.id:
        db.session.delete(item)
        db.session.commit()
        flash('Товар удалён из корзины.', 'info')
    return redirect(url_for('main.cart'))

@main.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    items = CartItem.query.filter_by(user_id=current_user.id).all()
    if not items:
        flash('Корзина пуста.', 'warning')
        return redirect(url_for('main.index'))

    form = OrderForm()
    if form.validate_on_submit():
        order = Order(
            user_id=current_user.id,
            delivery_type=form.delivery_type.data,
            address=form.address.data if form.delivery_type.data == 'до двери' else None
        )
        db.session.add(order)
        db.session.flush()

        for item in items:
            db.session.add(OrderItem(
                order_id=order.id,
                book_id=item.book_id,
                quantity=item.quantity,
                price=item.book.price
            ))

        for item in items:
            db.session.delete(item)

        db.session.commit()
        flash('Заказ оформлен!', 'success')
        return redirect(url_for('main.order_history'))

    return render_template('cart/checkout.html', form=form, items=items)

@main.route('/orders')
@login_required
def order_history():
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.date.desc()).all()
    return render_template('orders/history.html', orders=orders)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из аккаунта.', 'info')
    return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash('Пользователь с таким email уже существует.', 'danger')
            return render_template('auth/register.html', form=form)
        user = User(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            password=generate_password_hash(form.password.data),
            is_verified=True
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Регистрация успешна!', 'success')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Вход выполнен.', 'success')
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Неверный email или пароль.', 'danger')
    return render_template('auth/login.html', form=form)