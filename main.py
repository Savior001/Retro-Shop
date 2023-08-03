from flask import Flask, render_template, request, session
from db_models import DiscountCode, Item, SalesItem, User, db, get_all_discount_codes, get_all_items, get_all_orders, get_all_sales_items, get_all_users, get_order_history

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:password@host/retro_shop'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')
def home():
    items = get_all_items()
    return render_template('index.html', items=items)

@app.route('/admin/items', methods=['GET', 'POST'])
def admin_items():
    if request.method == 'POST':
        item_id = request.form.get('item_id')
        name = request.form.get('name')
        price = float(request.form.get('price'))
        quantity_available = int(request.form.get('quantity_available'))
        image_url = request.form.get('image_url')

        # update the item in the database
        item = session.query(Item).get(item_id)
        item.name = name
        item.price = price
        item.quantity_available = quantity_available
        item.image_url = image_url
        session.commit()

    items = get_all_items()
    return render_template('admin_items.html', items=items)

@app.route('/admin/discount_codes', methods=['GET', 'POST'])
def admin_discount_codes():
    if request.method == 'POST':
        code = request.form.get('code')
        percentage = float(request.form.get('percentage'))

        # create a new discount code in the database
        discount_code = DiscountCode(code=code, percentage=percentage)
        session.add(discount_code)
        session.commit()

    discount_codes = get_all_discount_codes()
    return render_template('admin_discount_codes.html', discount_codes=discount_codes)

@app.route('/admin/sales_items', methods=['GET', 'POST'])
def admin_sales_items():
    if request.method == 'POST':
        item_id = int(request.form.get('item_id'))
        sale_percentage = float(request.form.get('sale_percentage'))

        # create a new sales item in the database
        sales_item = SalesItem(item_id=item_id, sale_percentage=sale_percentage)
        session.add(sales_item)
        session.commit()

    sales_items = get_all_sales_items()
    return render_template('admin_sales_items.html', sales_items=sales_items)

@app.route('/admin/users', methods=['GET', 'POST'])
def admin_users():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        username = request.form.get('username')
        password = request.form.get('password')

        # update the user in the database
        user = session.query(User).get(user_id)
        user.username = username
        user.password = password
        session.commit()

    users = get_all_users()
    return render_template('admin_users.html', users=users)

@app.route('/admin/current_orders', methods=['GET'])
def admin_current_orders():
    orders = get_all_orders()
    return render_template('admin_current_orders.html', orders=orders)

@app.route('/admin/order_history', methods=['GET'])
def admin_order_history():
    sort_by = request.args.get('sort_by', 'order_date')
    orders = get_order_history(sort_by=sort_by)
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
    item = session.query(Item).get(item_id)
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
        session.commit()

    return render_template('admin_edit_item.html', item=item)

if __name__ == '__main__':
    app.run(debug=True)
