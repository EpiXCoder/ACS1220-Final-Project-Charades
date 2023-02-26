"""Import packages and modules."""
from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
# from flask_login import login_user, logout_user, login_required, current_user
from charades_app.models import Category, Word
# Word, GameInstance, User
from charades_app.main.forms import  CategoryForm, WordForm
# WordForm,

# Import app and db from events_app package so that we can run app
from charades_app.extensions import app, db, bcrypt

main = Blueprint("main", __name__)

##########################################
#           Routes                       #
##########################################


@main.route('/')
def homepage():
    return render_template('home.html')

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
        return redirect(url_for('main.contribute'))
    
    # if form was not valid, or was not submitted yet
    return render_template('create_category.html', form=form)



@main.route('/create_word', methods=['GET', 'POST'])
@login_required
def create_word():
    form = WordForm()

    # if form was submitted and contained no errors
    if form.validate_on_submit(): 
        new_word = Word(
            name=form.name.data,
            hint=form.hint.data,
            category=form.category.data
        )
        db.session.add(new_word)
        db.session.commit()

        flash('New word was created successfully.')
        return redirect(url_for('main.contribute')) 
        # changed the above code to redirect to homepage - if you decide to include a word details page - chage this back
    return render_template('create_word.html', form=form)

# Contribute page
@main.route('/contribute', methods=['GET'])
@login_required
def contribute():
    all_categories = Category.query.all()
    return render_template('contribute.html', all_categories=all_categories)


# NEED TO CREATE GAME INSTANCE PAGE