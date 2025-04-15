from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from app import db
from app.models import Trip, Budget, Expense, User

expenses_bp = Blueprint('expenses', __name__)

# Helper function to check if user is logged in
def is_logged_in():
    return 'user' in session

@expenses_bp.route('/', methods=['GET', 'POST'])
def expenses():
    if not is_logged_in():
        flash('Please log in to access your expenses.', 'warning')
        return redirect(url_for('auth.login'))
    
    user = User.query.filter_by(email=session['user']).first()
    if not user:
        flash('User not found. Please login again.', 'danger')
        return redirect(url_for('auth.login'))
    
    trip_id = request.args.get('trip_id')  # Get trip ID from URL

    if request.method == 'POST':
        category = request.form.get('category')
        amount = float(request.form.get('amount'))

        # Find the trip by ID and verify ownership
        trip = Trip.query.get(trip_id)
        if not trip or trip.user_id != user.id:
            flash('Trip not found or you do not have permission to access this trip.', 'danger')
            return redirect(url_for('itinerary.itinerary'))

        # Create and save the new expense
        expense = Expense(trip_id=trip.id, category=category, amount=amount)
        db.session.add(expense)
        db.session.commit()

        flash('Expense added successfully!', 'success')
        return redirect(url_for('expenses.expenses', trip_id=trip_id))

    # Get the trip data
    trip = Trip.query.get(trip_id)
    if not trip or trip.user_id != user.id:
        flash('Trip not found or you do not have permission to access this trip.', 'danger')
        return redirect(url_for('itinerary.itinerary'))

    # Calculate total expenses for the trip
    total_expenses = db.session.query(db.func.sum(Expense.amount)) \
        .filter(Expense.trip_id == trip_id) \
        .scalar() or 0  # If no expenses, default to 0

    total_budget = trip.budget.total_budget if trip and trip.budget else 0
    balance = total_budget - total_expenses

    # Get the distribution of expenses by category
    expense_distribution = db.session.query(Expense.category, db.func.sum(Expense.amount)) \
        .filter(Expense.trip_id == trip_id) \
        .group_by(Expense.category).all()

    # Prepare data for the pie chart
    expense_labels = [item[0] for item in expense_distribution]
    expense_values = [item[1] for item in expense_distribution]

    return render_template('expenses.html',
                           title="Expense Tracker",
                           expenses=Expense.query.filter_by(trip_id=trip_id).all(),
                           total_expenses=total_expenses,
                           total_budget=total_budget,
                           balance=balance,
                           trip_id=trip_id,
                           expense_labels=expense_labels,
                           expense_values=expense_values)


@expenses_bp.route('/data', methods=['GET'])
def expenses_data_api():
    if not is_logged_in():
        return jsonify({"error": "Authentication required"}), 401
    
    trip_id = request.args.get('trip_id')
    user = User.query.filter_by(email=session['user']).first()
    
    # Verify trip belongs to user
    trip = Trip.query.get(trip_id)
    if not trip or trip.user_id != user.id:
        return jsonify({"error": "Trip not found or access denied"}), 403
    
    # Return expenses data for API consumption
    expenses_data = db.session.query(Expense.category, Expense.amount).filter(Expense.trip_id == trip_id).all()
    return jsonify([{"category": cat, "amount": amt} for cat, amt in expenses_data])