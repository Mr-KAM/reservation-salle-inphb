from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user

main = Blueprint('main', __name__)

@main.route('/')
def home():
    """Home page route"""
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('rooms.list_rooms'))
    return render_template('home.html', title='Accueil')

@main.route('/about')
def about():
    """About page route"""
    return render_template('about.html', title='A propos')
