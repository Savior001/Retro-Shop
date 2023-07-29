from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from db_models import Item, DiscountCode, SalesItem, User, Order, Base, get_all_items, get_all_discount_codes, get_all_sales_items, get_all_users, get_all_orders, get_order_history

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a random secret key for security.
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'  # Change to 'danger' for a Bootstrap-styled warning.

@login_manager.user_loader
def load_user(user_id):
    return session.query(User).get(user_id)


# Replace this dictionary with actual user data stored in your database.
users = {'user_id_1': {'username': 'user1', 'password': 'password1'}}

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/')
def home():
    return render_template('/rt/dashboard.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_id = 'user_id_' + str(len(users) + 1)
        hashed_password = generate_password_hash(password)

        # Save the new user data to the 'users' dictionary (or your database).
        users[user_id] = {'username': username, 'password': hashed_password}

        return redirect(url_for('login'))

    return render_template('/rt/register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Replace this with your actual login logic
        user = session.query(User).filter_by(username=username).first()
        if user is None or not check_password_hash(user.password, password):
            # Invalid credentials, show a flash message and redirect back to the login page.
            flash('Invalid username or password. Please try again.', 'danger')
            return redirect(url_for('login'))

        # Valid credentials, log the user in.
        login_user(user)
        return redirect(url_for('dashboard'))

    return render_template('/rt/login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('/rt/dashboard.html', current_user=current_user)

# Routes/Views for admin backend
@app.route('/rt/admin/items')
@login_required
def admin_items():
    # Retrieve items from the database (or your data storage) and pass them to the template.
    items = get_all_items()
    return render_template('/rt/admin/items.html', items=items)

@app.route('/rt/admin/discount_codes')
@login_required
def admin_discount_codes():
    # Retrieve discount codes from the database (or your data storage) and pass them to the template.
    discount_codes = get_all_discount_codes()
    return render_template('/rt/admin/discount_codes.html', discount_codes=discount_codes)

@app.route('/rt/admin/sales_items')
@login_required
def admin_sales_items():
    # Retrieve sales items from the database (or your data storage) and pass them to the template.
    sales_items = get_all_sales_items()
    return render_template('/rt/admin/sales_items.html', sales_items=sales_items)

@app.route('/rt/admin/users')
@login_required
def admin_users():
    # Retrieve users from the database (or your data storage) and pass them to the template.
    users = get_all_users()
    return render_template('/rt/admin/users.html', users=users)

@app.route('/rt/admin/orders')
@login_required
def admin_orders():
    # Retrieve placed orders from the database (or your data storage) and pass them to the template.
    orders = get_all_orders()
    return render_template('/rt/admin/orders.html', orders=orders)

@app.route('/rt/admin/order_history')
@login_required
def order_history():
    # Retrieve order history from the database (or your data storage) and pass them to the template.
    order_history = get_order_history()
    return render_template('/rt/admin/order_history.html', order_history=order_history)

# Connection to Database
# Replace 'sqlite:///your_database_name.db' with the actual database URL for your chosen database.
engine = create_engine('mysql+mysqlconnector://root:pass@host/retro_shop')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


# Database Queries
def get_all_items():
    return session.query(Item).all()

def get_all_discount_codes():
    return session.query(DiscountCode).all()

def get_all_sales_items():
    return session.query(SalesItem).all()

def get_all_users():
    return session.query(User).all()

def get_all_orders():
    return session.query(Order).all()

def get_order_history(sort_by='order_date'):
    # Available sorting options: 'order_date', 'customer', 'order_size'
    if sort_by == 'order_date':
        return session.query(Order).order_by(desc(Order.order_date)).all()
    elif sort_by == 'customer':
        return session.query(Order).join(User).order_by(User.username).all()
    elif sort_by == 'order_size':
        return session.query(Order).order_by(desc(Order.total_amount)).all()
    else:
        return session.query(Order).all()
