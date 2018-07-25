import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify, make_response
)

from db import get_db

bp = Blueprint('poll', __name__, url_prefix='/poll')


@bp.route('/set_id', methods=('GET',))
def index():
    resp = make_response('')
    resp.set_cookie('user_id', request.args['user_id'])
    return resp

def get_user_id():
    return request.cookies.get('user_id')

@bp.route('/show', methods=['GET'])
def show_poll():
    return render_template('poll/display.html', user_id=get_user_id())

@bp.route('/current')
def show_current_poll():
    db = get_db()
    result = db.execute('SELECT * FROM poll ORDER BY id DESC LIMIT 1').fetchone()
    if result:
        return jsonify({
            'id': result['id'],
            'poll_time': result['poll_time'],
            'title': result['title'],
            'expired': result['expired'],
            'options': result['options'].split(',')
        })

    return jsonify({})

@bp.route('/answer', methods=['POST'])
def answer_poll():
    db = get_db()
    poll_id = request.form['poll_id']
    user_id = request.form['user_id']
    choice = request.form['option']
    
    choice = choice or 0

    poll = db.execute('SELECT * FROM poll WHERE id=?', (poll_id,)).fetchone()
   
    if not poll:
        from flask import abort
        return abort(404)

    db.execute(
            'INSERT INTO bet (user_id, poll_id, choice) VALUES (?,?,?)',  
            (user_id, poll_id, choice - 1))

    db.commit()

    return redirect(url_for('poll.show_result'))

@bp.route('/result', methods=['GET'])
def show_result():
    return render_template('poll/result.html', user_id=get_user_id())

@bp.route('/result/user', methods=('GET',))
def user_data():
    return overall_data(user_id=get_user_id())

@bp.route('/result/overall', methods=('GET',))
def overall_data(user_id = None):
    db = get_db()
    poll_query = db.execute('SELECT *, strftime(\'%s\', poll_time) as pt FROM poll WHERE expired != 2 ORDER BY id')

    result = {}
    for poll_row in poll_query:
        options = poll_row['options'].split(',')

        poll = {
                'choices': {opt: 0 for opt in options},
                'scores': {opt: 0 for opt in options}
                
                }
        poll['total_score'] = 0
        poll['options'] = options[:]
        options.insert(0, 'No answer')
        poll['title'] = poll_row['title']
        result[poll_row['id']] = poll

        if user_id:
            user_query = db.execute(
                'SELECT *, strftime(\'%s\', created) as ct  FROM bet '+
                'WHERE user_id=? AND poll_id=? ORDER BY id', (user_id, poll_row['id'],))

        else:
            user_query = db.execute(
                'SELECT *, strftime(\'%s\', created) as ct  FROM bet WHERE poll_id=? ORDER BY id', (poll_row['id'],))
        
        option_name = None
        for user_row in user_query:
            choice = user_row['choice']
            option_name = options[choice] if choice >= 0 else 'none'
            poll['choices'][option_name] += 1
            if poll_row['correct_value'] == choice:
                score = calculate_score(poll_row, user_row)
                poll['scores'][option_name] += score
                poll['total_score'] += score

        if user_id and not option_name is None:
            poll['choice'] = option_name
        elif user_id:
            del result[poll_row['id']]
        else:
            poll['choice'] = options[poll_row['correct_value'] + 1]

    return jsonify(result)

BASE_SCORE = 1000
def calculate_score(poll, choice):
    time_diff = int(choice['ct']) - int(poll['pt'])
    offset = round(time_diff/30)
    return BASE_SCORE // offset
