"""Import packages and modules."""
from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
# from flask_login import login_user, logout_user, login_required, current_user
from charades_app.models import Category
# Word, GameInstance, User
from charades_app.main.forms import  CategoryForm
# WordForm,

# Import app and db from events_app package so that we can run app
from charades_app.extensions import app, db, bcrypt

main = Blueprint("main", __name__)

##########################################
#           Routes                       #
##########################################


@main.route('/')
def homepage():
    all_categories = Category.query.all()
    return render_template('home.html',
        all_categories=all_categories)

@main.route('/create_category', methods=['GET', 'POST'])
@login_required
def create_category():
    form = CategoryForm()
    if form.validate_on_submit():
        new_category = Category(
            name=form.name.data
        )
        db.session.add(new_category)
        db.session.commit()

        flash('New category created successfully.')
        return redirect(url_for('main.homepage'))
    
    # if form was not valid, or was not submitted yet
    return render_template('create_genre.html', form=form)
