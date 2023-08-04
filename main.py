import db_models as dbm
from flask import Flask, redirect, render_template, request, session, url_for, flash, get_flashed_messages
from db_models import DiscountCode, Item, SalesItem, User, db

app = Flask(__name__)
app.secret_key = 'cs3773g8'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Thelegendofzelda1!@127.0.0.1/retro_shop'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')
def home():
    items = dbm.get_all_items()
    return render_template('index.html', items=items)

def login_required(view_func):
    """decorator to check if the user is logged in before accessing the route."""

    def wrapped_view(*args, **kwargs):
        if 'user_id' in session:
            return view_func(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    wrapped_view.__name__ = view_func.__name__
    return wrapped_view

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            session['user_id'] = user.id
            inventory = Item.query.all()
            return render_template('index.html', current_user=user.id, items=Item.query.all(), inventory=inventory)
        else:
            return render_template('login.html', error='Invalid username or password.')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    user_id = session['user_id']
    inventory = Item.query.all()
    get_flashed_messages()
    return render_template('index.html', current_user=user_id, items=Item.query.all(), inventory=inventory)


@app.route('/admin/items', methods=['GET'])
def admin_items():
    db.session.refresh
    items = db.session.query(Item).all()
    return render_template('admin_items.html', items=items)

@app.route('/admin/items', methods=['POST'])
def admin_update_item():
    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'Update':
            item_id = int(request.form.get('item_id'))
            name = request.form.get('name')
            price = float(request.form.get('price'))
            quantity_available = int(request.form.get('quantity_available'))
            image_url = request.form.get('image_url')

            item = Item.get_item(item_id)
            if item:
                # update the item in the database
                item.name = name
                item.price = price
                item.quantity_available = quantity_available
                item.image_url = image_url
                db.session.commit()
                flash(f'Item with ID {item_id} has been updated.', 'success')
            else:
                flash(f'Item with ID {item_id} not found.', 'error')
                
        elif action == 'Create':
            name = request.form.get('cname')
            price = float(request.form.get('cprice'))
            quantity_available = int(request.form.get('cquantity'))
            image_url = request.form.get('curl')
            
            if not name or price <= 0 or quantity_available < 0:
                flash('Invalid input data for creating item.', 'error')
            else:
                item = Item(name=name, price=price, quantity_available=quantity_available, image_url=image_url)
                db.session.add(item)
                db.session.commit()
                flash('Item has been created.', 'success')

        elif action == 'Delete':
            item_id = int(request.form.get('item_id'))
            item = Item.get_item(item_id)
            if item:
                db.session.delete(item)
                db.session.commit()
                flash(f'Item with ID {item_id} has been deleted.', 'success')
            else:
                flash(f'Item with ID {item_id} not found.', 'error')

    return redirect(url_for('admin_items'))

@app.route('/delete_item/<int:item_id>', methods=['POST'])
def admin_delete_item(item_id):
    item = Item.get_item(item_id)
    if item:
        db.session.delete(item)
        db.session.commit()
        flash(f'Item with ID {item_id} has been deleted.', 'success')
    else:
        flash(f'Item with ID {item_id} not found.', 'error')

    return redirect(url_for('dashboard'))

@app.route('/admin/discount_codes', methods=['GET', 'POST'])
def admin_discount_codes():
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'create':
            code = request.form.get('code')
            percentage_str = request.form.get('percentage')

            try:
                # try converting the percentage string to a float
                percentage = float(percentage_str)

                # check if percentage is within the valid range (0 to 100)
                if 0 <= percentage <= 100:
                    # convert percentage to a valid decimal value
                    percentage = percentage / 100.0

                    # create a new discount code in the database
                    discount_code = DiscountCode(code=code, percentage=percentage)
                    db.session.add(discount_code)
                    db.session.commit()

                else:
                    # if the percentage is outside the valid range, show error message
                    discount_codes = dbm.get_all_discount_codes()
                    return render_template('admin_discount_codes.html', discount_codes=discount_codes, error='Invalid percentage. Percentage must be between 0 and 100.')

            except ValueError:
                # if percentage cannot be converted to a float, show error message
                discount_codes = dbm.get_all_discount_codes()
                return render_template('admin_discount_codes.html', discount_codes=discount_codes, error='Invalid percentage. Please enter a numeric value.')

        elif action == 'delete':
            code_id = request.form.get('code_id')

            # find the discount code in the database and delete it
            discount_code = DiscountCode.query.get(code_id)
            if discount_code:
                db.session.delete(discount_code)
                db.session.commit()

    discount_codes = dbm.get_all_discount_codes()
    return render_template('admin_discount_codes.html', discount_codes=discount_codes)

@app.route('/admin/sales_items', methods=['GET', 'POST'])
def admin_sales_items():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'Create':
            item_id = int(request.form.get('item_id'))
            sale_percentage = float(request.form.get('sale_percentage'))

            # find item in the database
            item = Item.get_item_by_id(item_id)
            if not item:
                print("item not found")
                return render_template('admin_sales_items.html', sales_items=dbm.get_all_sales_items(), error='Item not found.')

            # calculate the new sale price
            if 0 <= sale_percentage <= 100:
                new_price = item.price * (1 - sale_percentage / 100.0)
                new_price = round(new_price, 2)
                # check if a sales item with the same item_id already exists
                existing_sales_item = SalesItem.query.filter_by(item_id=item_id).first()
                if existing_sales_item:
                    # if sales item already exists, update its sale_percentage and sale_price
                    existing_sales_item.sale_percentage = sale_percentage
                    existing_sales_item.sale_price = new_price
                else:
                    # if sales item does not exist, create a new one
                    sales_item = SalesItem(item_id=item.id, sale_percentage=sale_percentage, sale_price=new_price)
                    db.session.add(sales_item)
                
                db.session.commit()
            else:
                return render_template('admin_sales_items.html', sales_items=dbm.get_all_sales_items(), error='Invalid sale percentage. Percentage must be between 0 and 100.')

        elif action == 'Delete':
            sales_item_id = request.form.get('sales_item_id')

            # find the sales item in the database and delete it
            sales_item = SalesItem.query.get(sales_item_id)
            if sales_item:
                db.session.delete(sales_item)
                db.session.commit()

    sales_items = dbm.get_all_sales_items()
    return render_template('admin_sales_items.html', sales_items=sales_items)

@app.route('/admin/users', methods=['GET'])
@login_required
def admin_users():
    users = db.session.query(User).all()
    return render_template('admin_users.html', users=users)

@app.route('/admin/users/<int:user_id>', methods=['POST'])
@login_required
def admin_edit_users(user_id):
    user = User.get_user_by_id(user_id)
    username = request.form.get('username')
    password = request.form.get('password')

    # update the user in the database
    user.username = username
    user.password = password
    db.session.commit()
    flash('User data has been updated.', 'success')

    return redirect('/admin/users')

@app.route('/admin/current_orders', methods=['GET'])
def admin_current_orders():
    orders = dbm.get_all_orders()
    return render_template('admin_current_orders.html', orders=orders)

@app.route('/admin/order_history', methods=['GET'])
def admin_order_history():
    sort_by = request.args.get('sort_by', 'order_date')
    orders = dbm.get_order_history(sort_by=sort_by)
    return render_template('admin_order_history.html', orders=orders)

@app.route('/admin/create_item', methods=['GET', 'POST'])
def admin_create_item():
    if request.method == 'POST':
        name = request.form.get('name')
        price = float(request.form.get('price'))
        quantity_available = int(request.form.get('quantity_available'))
        image_url = request.form.get('image_url')

        # create a new item in the database
        item = Item(name=name, price=price, quantity_available=quantity_available, image_url=image_url)
        session.add(item)
        session.commit()

    return render_template('admin_create_item.html')

@app.route('/admin/edit_item/<int:item_id>', methods=['GET', 'POST'])
def admin_edit_item(item_id):
    item = db.session.query(Item).get(item_id)
    if request.method == 'POST':
        name = request.form.get('name')
        price = float(request.form.get('price'))
        quantity_available = int(request.form.get('quantity_available'))
        image_url = request.form.get('image_url')

        # update the item in the database
        item.name = name
        item.price = price
        item.quantity_available = quantity_available
        item.image_url = image_url
        db.session.commit()

        flash(f'Item data for { name } has been updated.', 'success')
        return redirect(url_for('admin_edit_item', item_id=item_id))

    return render_template('admin_edit_item.html', item=item)

if __name__ == '__main__':
    app.run(debug=True)
