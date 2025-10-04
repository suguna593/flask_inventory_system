from main import db, Product, Location, app

with app.app_context():
    print("Creating new database and tables...")
    db.create_all()  # This will create the tables according to your models

    # Add initial products
    if not Product.query.first():
        db.session.add_all([
            Product(name="Product A"),
            Product(name="Product B"),
            Product(name="Product C")
        ])
        db.session.commit()
        print("Products added successfully!")

    # Add initial locations
    if not Location.query.first():
        db.session.add_all([
            Location(name="Warehouse X"),
            Location(name="Warehouse Y"),
            Location(name="Warehouse Z")
        ])
        db.session.commit()
        print("Locations added successfully!")
