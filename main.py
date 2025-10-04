from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Models
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class Movement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    from_location = db.Column(db.String(100))
    to_location = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    product = db.relationship('Product')

# Create tables
with app.app_context():
    db.create_all()

# Home route
@app.route('/')
def home():
    return render_template('home.html')

# Products route
@app.route('/products')
def products():
    products = Product.query.all()
    return render_template('products.html', products=products)

# Locations route
@app.route('/locations')
def locations():
    locations = Location.query.all()
    return render_template('locations.html', locations=locations)

# Movements route
@app.route('/movements', methods=['GET', 'POST'])
def movements():
    products = Product.query.all()
    locations = Location.query.all()
    if request.method == 'POST':
        product_id = request.form['product']
        from_location = request.form.get('from_location')
        to_location = request.form['to_location']
        quantity = int(request.form['quantity'])
        new_move = Movement(
            product_id=product_id,
            from_location=from_location,
            to_location=to_location,
            quantity=quantity
        )
        db.session.add(new_move)
        db.session.commit()
        return redirect(url_for('movements'))

    movements_history = Movement.query.order_by(Movement.timestamp.desc()).all()
    return render_template('movements.html', products=products, locations=locations, movements=movements_history)

# Balance route
@app.route('/balance')
def balance():
    products = Product.query.all()
    locations = Location.query.all()
    balances = []

    for product in products:
        for location in locations:
            # Total moved to location
            qty_in = db.session.query(db.func.sum(Movement.quantity)).filter(
                Movement.product_id == product.id,
                Movement.to_location == location.name
            ).scalar() or 0

            # Total moved from location
            qty_out = db.session.query(db.func.sum(Movement.quantity)).filter(
                Movement.product_id == product.id,
                Movement.from_location == location.name
            ).scalar() or 0

            qty = qty_in - qty_out
            balances.append({
                'product': product.name,
                'location': location.name,
                'quantity': qty
            })

    return render_template('balance.html', balances=balances)

# Run app
if __name__ == '__main__':
    app.run(debug=True)
