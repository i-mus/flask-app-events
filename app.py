# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from models import Base, engine, SessionLocal, Event
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'

# Create tables at startup
Base.metadata.create_all(bind=engine)


# Helper: Get DB session
def get_db():
    db = SessionLocal()
    try:
        return db
    except:
        db.close()
        raise


# Routes
@app.route('/')
def index():
    db = get_db()
    events = db.query(Event).all()
    db.close()
    return render_template('index.html', events=events)


@app.route('/add', methods=['GET', 'POST'])
def add_event():
    if request.method == 'POST':
        db = get_db()
        try:
            event = Event(
                name=request.form['name'],
                start_date=datetime.strptime(request.form['start_date'], '%Y-%m-%d').date(),
                end_date=datetime.strptime(request.form['end_date'], '%Y-%m-%d').date(),
                start_time=datetime.strptime(request.form['start_time'], '%H:%M').time(),
                end_time=datetime.strptime(request.form['end_time'], '%H:%M').time(),
                venue=request.form['venue'],
                location=request.form['location'],
                booking_url=request.form['booking_url'] or None,
                ticket_price=float(request.form['ticket_price']),
                category=request.form['category'],
                description=request.form['description']
            )
            db.add(event)
            db.commit()
            flash("Event added successfully!", "success")
        except Exception as e:
            db.rollback()
            flash(f"Error: {str(e)}", "danger")
        finally:
            db.close()
        return redirect(url_for('index'))

    return render_template('add_event.html')


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_event(id):
    db = get_db()
    event = db.query(Event).filter(Event.id == id).first()
    if not event:
        db.close()
        flash("Event not found.", "danger")
        return redirect(url_for('index'))

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

            db.commit()
            flash("Event updated successfully!", "success")
        except Exception as e:
            db.rollback()
            flash(f"Error: {str(e)}", "danger")
        finally:
            db.close()
        return redirect(url_for('index'))

    db.close()
    return render_template('edit_event.html', event=event)


@app.route('/delete/<int:id>', methods=['POST'])
def delete_event(id):
    db = get_db()
    event = db.query(Event).filter(Event.id == id).first()
    if event:
        try:
            db.delete(event)
            db.commit()
            flash("Event deleted successfully!", "success")
        except Exception as e:
            db.rollback()
            flash(f"Error: {str(e)}", "danger")
    else:
        flash("Event not found.", "danger")
    db.close()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, port=4000)