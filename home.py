import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)

from db import get_db

bp = Blueprint('poll', __name__, url_prefix='/poll')

@bp.route('/show', methods=['GET'])
def show_poll():
    return render_template('poll/display.html')

@bp.route('/current')
def show_current_poll():
    db = get_db()
    result = db.execute('SELECT * FROM poll ORDER BY id DESC LIMIT 1').fetchone()
    if result:
        return jsonify({
            'id': result['id'],
            'title': result['title'],
            'options': result['options'].split(',')
        })

    return jsonify({})

@bp.route('/answer', methods=['POST'])
def answer_poll():
    pass

@bp.route('/result', methods=['GET'])
def show_result():
    return render_template('poll/result.html')

