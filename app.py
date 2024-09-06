from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# MySQL configuration (update credentials)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://username:password@localhost/food_booking_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Define the booking model
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    food_item = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

# Route to create a new booking
@app.route('/api/book', methods=['POST'])
def book():
    data = request.json
    new_booking = Booking(customer_name=data['customer_name'], food_item=data['food_item'], quantity=data['quantity'])
    db.session.add(new_booking)
    db.session.commit()
    return jsonify({"message": "Booking successful"}), 201

# Route to view bookings
@app.route('/api/bookings', methods=['GET'])
def get_bookings():
    bookings = Booking.query.all()
    result = [{"customer_name": b.customer_name, "food_item": b.food_item, "quantity": b.quantity} for b in bookings]
    return jsonify(result)

if __name__ == '__main__':
    db.create_all()  # Create the database tables
    app.run(debug=True)
