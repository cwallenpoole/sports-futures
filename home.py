import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)

from db import get_db

bp = Blueprint('poll', __name__, url_prefix='/poll')

@bp.route('/show', methods=['GET'])
def show_poll():
    return render_template('poll/display.html', user_id=1234)

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
    db = get_db()
    poll_id = request.form['poll_id']
    user_id = request.form['user_id']
    option = request.form['option']
    poll = db.execute('SELECT * FROM poll WHERE id=?', (poll_id,)).fetchone()
   
    if not poll:
        from flask import abort
        return abort(404)
    return redirect(url_for('poll.show_result'))

@bp.route('/result', methods=['GET'])
def show_result():
    return render_template('poll/result.html')

