from flask import Blueprint, render_template, request, flash, redirect, url_for

home = Blueprint("home", __name__, url_prefix='/')

@home.route('/')
def index():
    return render_template('home.html')