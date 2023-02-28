"""Import packages and modules."""
from os import abort
import random
from flask import Blueprint, request, render_template, redirect, url_for, flash, make_response, Flask, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import func
from charades_app.models import Category, Word
from charades_app.main.forms import  CategoryForm, WordForm
# WordForm,


# Import app and db from events_app package so that we can run app
from charades_app.extensions import app, db, bcrypt
from charades_app.schema import CategorySchema, WordSchema

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
        cat_id = db.session.query(Category.id).filter(Category.name == form.category.name).first() 
        new_word = Word(
            name=form.name.data,
            hint=form.hint.data,
            category_id = cat_id,
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

# Words
@main.route('/words', methods=['GET'])
@login_required
def words():
    all_words = Word.query.all()
    all_categories = Category.query.all()
    return render_template('words.html', all_words=all_words, all_categories=all_categories)

@main.route('/edit_word/<word_id>', methods=['GET', 'POST'])
def edit_word(word_id):
    word = Word.query.get(word_id)
    form = WordForm(obj=word)
    
    # if form was submitted and contained no errors
    if form.validate_on_submit():
        # cat_id = db.session.query(Category.id).filter(Category.name == form.category.name).first() 
        word.name=form.name.data
        word.hint=form.hint.data
        # word.category_id = form.category.data
        word.category=form.category.data
        
        db.session.commit()

        flash('Word was updated successfully.')
        return redirect(url_for('main.edit_word', word_id=word_id))

    return render_template('edit_word.html', word=word, form=form)

@app.route('/delete_word/<word_id>', methods=['POST'])
@login_required
def delete_word(word_id):
    print(request.method)
    word = Word.query.get(word_id)
    db.session.delete(word)
    db.session.commit()
    flash('Word has been deleted.', 'success')
    return redirect(url_for('main.words'))


@app.context_processor
def inject_categories():
    categories = Category.query.all()
    selected_category = request.cookies.get('category')
    return dict(categories=categories, selected_category=selected_category)

# GAME INSTANCE
@app.route('/category')
def get_categories():
    categories = Category.query.all()
    category_schema = CategorySchema(many=True)
    return jsonify(category_schema.dump(categories))

@app.route('/category/<int:category_id>/words')
def get_words(category_id):
    words = Word.query.filter_by(category_id=category_id).all()
    word_schema = WordSchema(many=True)
    return jsonify(word_schema.dump(words))

@main.route('/game')
def game():
    categories = Category.query.all()
    return render_template('game.html')