from main import db, Product, Location, Movement, app
from datetime import datetime, timedelta
import random

with app.app_context():
    db.create_all()

    # Add Products
    if not Product.query.first():
        products = [Product(name=f"Product {c}") for c in ["A", "B", "C", "D"]]
        db.session.add_all(products)
        db.session.commit()
        print("Products added!")

    # Add Locations
    if not Location.query.first():
        locations = [Location(name=f"Warehouse {c}") for c in ["X", "Y", "Z", "W"]]
        db.session.add_all(locations)
        db.session.commit()
        print("Locations added!")

    # Make 20 random movements
    if not Movement.query.first():
        products = Product.query.all()
        locations = [l.name for l in Location.query.all()]
        for _ in range(20):
            product = random.choice(products)
            from_loc = random.choice(locations + [None])
            to_loc = random.choice(locations)
            quantity = random.randint(1, 5)
            movement = Movement(
                product_id=product.id,
                from_location=from_loc,
                to_location=to_loc,
                quantity=quantity,
                timestamp=datetime.utcnow() - timedelta(days=random.randint(0, 10))
            )
            db.session.add(movement)
        db.session.commit()
        print("20 movements added!")
