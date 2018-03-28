# _*_ coding: utf-8 _*_


from flask import Flask, request, session, render_template, redirect, url_for, json,render_template_string
from flask_socketio import SocketIO, send

from model.pageDAO import PageDao
from model.pageVO import PageVO
from model.boardVO import BoardVO


from werkzeug import security
import os
import chardet
import uuid
import datetime


app = Flask(__name__)
app.secret_key = 'shutter_sec_'
socket_io = SocketIO(app)


@app.route('/')
@app.route('/account/login')
def login():
    if session.get('logFlag') == True:
        return redirect(url_for('main_view'))
    return render_template('login.html')

@app.route('/account/login_ing', methods = ['POST','GET'])
def login_ing():
    vo = PageVO()
    vo.user_id = request.form.get('user_id')
    vo.user_pw = request.form['user_pw']

    if len(vo.user_id) == 0 or len(vo.user_pw) == 0:
        return ' 로그인 정보를 제대로 입력하지 않았습니다.'

    dao = PageDao()
    ansor = dao.login(vo)

    if (ansor != ()):
        log_id = ansor[0]
        print(type(ansor))
        print(log_id['id'])
        session['logFlag'] = True
        session['user_id'] = log_id['id']
        session['user_no'] = log_id['no']

        return redirect(url_for('main_view'))
    else:
        return '테스트 : 로그인 실패'

@app.route('/account/logout')
def logout():
    session['logFlag'] = False
    session['user_id'] = ''
    session['user_no'] = ''

    return redirect(url_for('login'))


@app.route('/account/create_account.do')
def create_account():
    return render_template('create_account.html')





@app.route('/account/create_account_ing', methods=['POST', 'GET'])
def create_ing():

    dao = PageDao()
    vo = PageVO()

    try:
        vo.user_id = request.form['user_id']
        vo.user_pw = request.form['user_pw']
        vo.user_email = request.form['user_email']
        vo.user_p_num = request.form['user_p_num']

        print(vo.user_id + '//' + vo.user_pw + '//' + vo.user_email)

        dao.new_account(vo)



        return render_template('create_account_ok.html')
    except:
        return redirect(url_for('create_account_fail'))
            #render_template('create_account_fail.html')



@app.route('/account/create_account_fail')
def create_account_fail():
    return render_template('create_account_fail.html')



@app.route('/account/<user>')
def my_profile(user):

    dao = PageDao()

    me = dao.user_info(user, session.get('user_no'));

    print(me)

    return render_template("my_infomation.html", user=me['id'], email=me['email'], phone=me['p_num'])


@app.route("/account/edit", methods=["POST"])
def edit():
    vo = PageVO()
    dao = PageDao()
    vo.user_id = request.form['user_n']
    vo.user_email = request.form['email_n']
    vo.user_p_num = request.form['phone_n']


    vo.user_no = session.get('user_no')
    dao.user_alt(vo)

    return redirect(url_for('logout'))










@app.route('/main')
def main_view():
    if session.get('logFlag') != True:
        return redirect(url_for('login'))

    user = session.get('user_id')
    dao = PageDao()
    max_P = dao.count_board()
    return render_template("board.html", user = user, max = max_P)


@app.route('/main2')
def main_view2():
    user = session.get('user_id')
    dao = PageDao()
    max_P = dao.count_board()
    context = dao.select_board2()


    return render_template_string("board2.html")





@app.route('/board/write', methods = ['POST', 'GET'])
def write():
    vo = BoardVO()
    vo.user = session.get('user_id')
    if request.method == 'POST' and 'file' in request.files:
        vo.title = request.form['title']
        vo.content = request.form['content']
        file = request.files['file']
        vo.file = file.filename
        vo.no = session.get('user_no')
        dir = os.path.dirname(os.path.abspath(__file__)) + "\\static\\Uploads\\" + vo.no
        result = os.path.isdir(dir)
        if result != True:
            os.mkdir(dir)
        file.save(os.path.join(dir, file.filename))

        print(vo.title)
        print(">>" + file.filename + "<<")

        dao = PageDao()
        dao.new_board(vo)
    return render_template("board_write.html", user = vo.user)


@app.route('/board/select', methods=['GET', 'POST'])
def board_select():

    page = request.form['page']
    print(page)

    dao = PageDao()
    result = dao.select_board(page)

    print(result)

    date = result['date']

    date_result = "" + str(date.year) + "년 " + str(date.month) + "월 " + str(date.day) + "일   " + str(date.hour) + "시" + str(date.minute) + "분"

    return json.dumps({'user' : result['user'], 'title' : result['title'], 'content' : result['content'], 'no' : result['no'],
                       'file' : result['file'], 'hit' : result['hit'], 'date' : date_result})




@app.route("/chat")
def chatting():
    if session.get('logFlag') != True:
        return redirect(url_for('main_view'), me=session.get('user_id'))
    else :
        return render_template("chatting.html")




@socket_io.on("message")
def request_msg(message):

    #print("message : " + message)
    to_client = dict()
    to_client['user'] = session.get('user_id')
    if message == 'new_connect':
        to_client['message'] = session.get("user_id")
        to_client['type'] = 'connect'
    else:
        to_client['message'] = str(message)
        to_client['type'] = 'normal'

    send(to_client, broadcast=True)


@socket_io.on('disconnect')
def disconnect():
    session.clear()
    print('Disconnect')





if __name__ == '__main__':
    #app.debug = False
    app.config['UPLOAD_FOLDER'] = 'static/Uploads'
    app.secret_key = 'sample_secreat_key'
    #app.run(host = '0.0.0.0', port=8888)
    socket_io.run(app,host='0.0.0.0' ,port=8520, debug=True)
    #socket_io.run(app, debug=True)



    #, host='0,0,0,0', port=9999
    #, debug=True, port=9999



