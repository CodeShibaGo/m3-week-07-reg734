from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from flask_login import  login_user, logout_user, current_user, login_required
from sqlalchemy import text
import sqlalchemy as sa
from app.models import User
from urllib.parse import urlsplit
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime, timezone
from flask_wtf.csrf import validate_csrf, CSRFError



@app.route('/')
@app.route('/index')
@login_required
def index():
    user = {'username': 'Reg'}
    posts =[
        {
            'author':{'username':'John'},
            'body':'Portland 的天氣真好'
        },
        {
            'author':{'username': 'Susan'},
            'body': '復仇者聯盟電影真的很酷！'
        }
    ]
    return render_template('index.html', title='首頁', user=user, posts=posts)

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    errors = {}
    if request.method == 'POST':
        try:
            validate_csrf(request.form.get('csrf_token'))
        except CSRFError:
            errors['csrf'] = 'CSRF 驗證失敗'
            return render_template('login.html', errors=errors)

        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        remember = bool(request.form.get('remember_me'))

        # 基本欄位驗證
        if not username:
            errors['username'] = '請輸入使用者名稱'
        if not password:
            errors['password'] = '請輸入密碼'

        if not errors:
            # 查找使用者
            sql = text("SELECT * FROM user WHERE username = :username")
            result = db.session.execute(sql, {'username': username}).first()

            if result:
                user = User.query.get(result.id)  # 將原始資料轉為 SQLAlchemy model 使用
                if check_password_hash(user.password_hash, password):
                    login_user(user, remember=remember)
                    flash('登入成功！')
                    return redirect(url_for('index'))
                else:
                    errors['password'] = '密碼錯誤'
            else:
                errors['username'] = '使用者不存在'

    return render_template('login.html', errors=errors)
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    errors = {}

    if request.method == 'POST':
        # CSRF 驗證
        try:
            validate_csrf(request.form.get('csrf_token'))
        except CSRFError:
            errors['csrf'] = 'CSRF 驗證失敗'

        # 取得欄位並去除多餘空白
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        password2 = request.form.get('password2', '')

        # 手動表單驗證
        if not username:
            errors['username'] = '請輸入使用者名稱'
        if not email or '@' not in email:
            errors['email'] = '請輸入有效 Email'
        if not password:
            errors['password'] = '請輸入密碼'
        if password != password2:
            errors['password2'] = '密碼不一致'

        # 重複資料驗證（只有在前面沒錯時才進行）
        if not errors:
            sql_user = text("SELECT id FROM user WHERE username = :username")
            if db.session.execute(sql_user, {'username': username}).first():
                errors['username'] = '使用者名稱已存在'

            sql_email = text("SELECT id FROM user WHERE email = :email")
            if db.session.execute(sql_email, {'email': email}).first():
                errors['email'] = 'Email 已被註冊'

        # 若沒有錯誤就寫入 DB
        if not errors:
            hashed_password = generate_password_hash(password)
            sql_insert = text("""
                INSERT INTO user (username, email, password_hash)
                VALUES (:username, :email, :password_hash)
            """)
            db.session.execute(sql_insert, {
                'username': username,
                'email': email,
                'password_hash': hashed_password
            })
            db.session.commit()
            flash('註冊成功！')
            return redirect(url_for('login'))

    return render_template('register.html', errors=errors)

@app.route('/user/<username>')
@login_required
def user(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    posts = [
        {'author': user, 'body': '測試貼文 #1'},
        {'author': user, 'body': '測試貼文 #2'}
    ]
    return render_template('user.html', user=user, posts=posts)
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)
