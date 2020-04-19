from app import app
from flask import render_template, redirect, url_for


@app.errorhandler(404)
def not_found(e):
    return render_template('errors/not_found.jinja2')


@app.errorhandler(401)
def unauthorized(e):
    return redirect(url_for('login'))
