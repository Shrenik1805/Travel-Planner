from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models import Trip, Budget, User

budget_bp = Blueprint('budget', __name__)

# Helper function to check if user is logged in
def is_logged_in():
    return 'user' in session

@budget_bp.route('/', methods=['GET', 'POST'])
def budget():
    if not is_logged_in():
        flash('Please log in to access your budgets.', 'warning')
        return redirect(url_for('auth.login'))
    
    user = User.query.filter_by(email=session['user']).first()
    if not user:
        flash('User not found. Please login again.', 'danger')
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        # Get trip id from the form
        trip_id = request.form.get('trip_id')  # Assuming trip_id is passed from the trip page
        
        # Get budget data from form
        total_budget = float(request.form.get('total_budget'))
        categories = request.form.getlist('category[]')
        amounts = request.form.getlist('amount[]')

        # Find the trip by ID and verify ownership
        trip = Trip.query.get(trip_id)
        
        if not trip or trip.user_id != user.id:
            flash('Trip not found or you do not have permission to access this trip.', 'danger')
            return redirect(url_for('budget.budget'))

        # Check if budget already exists for this trip and update it
        existing_budget = Budget.query.filter_by(trip_id=trip.id).first()
        if existing_budget:
            existing_budget.total_budget = total_budget
            existing_budget.categories = {cat: float(amt) for cat, amt in zip(categories, amounts)}
            db.session.commit()
            flash('Budget updated successfully!', 'success')
        else:
            # Create a new budget entry
            budget = Budget(
                trip_id=trip.id,
                total_budget=total_budget,
                categories={cat: float(amt) for cat, amt in zip(categories, amounts)}
            )
            
            # Add the budget to the session and commit to save it to the database
            db.session.add(budget)
            db.session.commit()
            flash('Budget planned successfully!', 'success')
            
        return redirect(url_for('budget.budget'))

    # Get all trips for the current user
    trips = Trip.query.filter_by(user_id=user.id).all()
    return render_template('budget.html', title="Budget Planner", trips=trips)