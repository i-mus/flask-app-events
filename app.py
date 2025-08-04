# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Event
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'
app.config['SECRET_KEY'] = 'your-secret-key'
db.init_app(app)

# Create tables
# Create tables
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def index():
    events = Event.query.all()
    return render_template('index.html', events=events)

@app.route('/add', methods=['GET', 'POST'])
def add_event():
    if request.method == 'POST':
        try:
            # Parse form data
            name = request.form['name']
            start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d').date()
            end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d').date()
            start_time = datetime.strptime(request.form['start_time'], '%H:%M').time()
            end_time = datetime.strptime(request.form['end_time'], '%H:%M').time()
            venue = request.form['venue']
            location = request.form['location']
            booking_url = request.form['booking_url'] or None
            ticket_price = float(request.form['ticket_price'])
            category = request.form['category']
            description = request.form['description']

            # Create new event
            event = Event(
                name=name,
                start_date=start_date,
                end_date=end_date,
                start_time=start_time,
                end_time=end_time,
                venue=venue,
                location=location,
                booking_url=booking_url,
                ticket_price=ticket_price,
                category=category,
                description=description
            )

            db.session.add(event)
            db.session.commit()
            flash("Event added successfully!", "success")
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f"Error: {str(e)}", "danger")

    return render_template('add_event.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_event(id):
    event = Event.query.get_or_404(id)
    if request.method == 'POST':
        try:
            event.name = request.form['name']
            event.start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d').date()
            event.end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d').date()
            event.start_time = datetime.strptime(request.form['start_time'], '%H:%M').time()
            event.end_time = datetime.strptime(request.form['end_time'], '%H:%M').time()
            event.venue = request.form['venue']
            event.location = request.form['location']
            event.booking_url = request.form['booking_url'] or None
            event.ticket_price = float(request.form['ticket_price'])
            event.category = request.form['category']
            event.description = request.form['description']

            db.session.commit()
            flash("Event updated successfully!", "success")
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f"Error: {str(e)}", "danger")

    return render_template('edit_event.html', event=event)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_event(id):
    event = Event.query.get_or_404(id)
    try:
        db.session.delete(event)
        db.session.commit()
        flash("Event deleted successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error: {str(e)}", "danger")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=4000)