import os
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session,  make_response, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import random

from helpers import login_required


UPLOAD_FOLDER = 'static/userpics'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


account_pic = ''


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL('sqlite:///freezme.db')


@app.route("/signup", methods=["GET", "POST"])
def signup():
    # Forget any user_id
    session.clear()

    if request.method == 'POST':
        if not request.form.get('email') or not request.form.get('password') or not request.form.get('password_repeat'):
            # no input
            return error('No input', 'All the fields must be filled to sign up!')
        else:
            if request.form.get('password') != request.form.get('password_repeat'):
                # passwords not match
                return error('Passwords doesn\'t match', 'Try again')
            else:
                # if all Ok
                email = request.form.get('email')
                password = request.form.get('password')

                # check if account with this email is exists
                account = db.execute(
                    'SELECT email FROM accounts WHERE email = :email', email=email)
                if len(account) != 0:
                    # Account with this email already exists
                    return error('Account with the email already exists', 'Try to sign in — you may be already registred')

                hashed = generate_password_hash(password)

                pic_default = "default.png"

                supported_languages = ['en-EN', 'ru-RU', 'en', 'ru']
                browser_lang = request.accept_languages.best_match(
                    supported_languages)

                db.execute('INSERT INTO accounts(email, hash, account_pic, lang) VALUES (:email, :hashed, :pic_default, :browser_lang)',
                           email=email, hashed=hashed, pic_default=pic_default, browser_lang=browser_lang)

                return render_template('signin.html')

    else:
        print('TEST # 11')
        return render_template('signup.html')


@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == 'POST':
        # Forget any user_id
        session.clear()

        if not request.form.get('email') or not request.form.get('password'):
            return "no input"
        email = request.form.get('email')
        password = request.form.get('password')
        # Quety database for email
        account = db.execute(
            'SELECT * FROM accounts WHERE email = :email', email=email)

        if len(account) != 1 or not check_password_hash(account[0]['hash'], password):
            return error('Wrong E-mail / Password', 'Try again')

        # Remember which user has logged in
        session['account_id'] = account[0]['account_id']
        print(session)

        return redirect('/')
    # if logged in but try to open signin page again
    elif request.method == 'GET':
        if len(session) == 1:
            print('HELLO')
            return redirect('/')
        else:

            # Forget any user_id
            session.clear()
            return render_template('signin.html')


@app.route('/history', methods=["GET", "POST"])
@login_required
def history():
    """fridge history"""

    if request.get_json():
        req = request.get_json()
        if req['action'] == 'clearHistory':
            clearHistory()

    account_id = session["account_id"]

    account_pic = db.execute(
        'SELECT account_pic FROM accounts WHERE account_id = :account_id', account_id=account_id)
    account_pic = account_pic[0]['account_pic']

    history = db.execute(
        "SELECT * FROM history WHERE account_id = :account_id ORDER BY history_id DESC", account_id=account_id)
    lang = userlangcheck()
    return render_template('history.html', items=history, lang=lang, account_pic=account_pic)


def addtohistory(item, descr, qnt, unit, evnt, account_id):

    now = datetime.now()
    date = now.strftime("%d/%m/%Y %H:%M:%S")

    addhistory = db.execute('INSERT INTO history (history_item, descr, history_quantity, history_qnt_units, history_event, date, account_id) VALUES (:item, :descr, :qnt, :unit, :evnt, :date, :account_id)',
                            item=item, descr=descr, qnt=qnt, unit=unit, evnt=evnt, date=date, account_id=account_id)

    return redirect('/history')


def clearHistory():
    account_id = session["account_id"]
    db.execute('DELETE FROM history WHERE account_id = :account_id',
               account_id=account_id)
    print('DONE CLEAN')


@app.route('/', methods=["GET", "POST"])
@app.route('/fridge', methods=["GET", "POST"])
@login_required
def fridge():
    """fridge list"""
    account_id = session["account_id"]

    account_pic = db.execute(
        'SELECT account_pic FROM accounts WHERE account_id = :account_id', account_id=account_id)
    account_pic = account_pic[0]['account_pic']

    if request.method == "POST":
        if request.form.get('add'):
            return add()
        elif request.form.get('edit'):

            return edit()
        else:

            items = request.get_json()
            if items['action'] == 'remove':
                remove(items)
            items = db.execute(
                'SELECT * FROM items WHERE account_id = :account_id ORDER BY item_id DESC', account_id=account_id)
            lang = userlangcheck()
            return render_template('fridge.html', items=items, lang=lang, account_pic=account_pic)
    else:
        items = db.execute(
            'SELECT * FROM items WHERE account_id = :account_id ORDER BY item_id DESC', account_id=account_id)
        lang = userlangcheck()
        return render_template('fridge.html', items=items, lang=lang, account_pic=account_pic)


def userlangcheck():
    account = session["account_id"]
    userlang = db.execute(
        'SELECT lang FROM accounts WHERE account_id = :account', account=account)
    return userlang[0]['lang']


@app.route('/wishlist', methods=["GET", "POST"])
@login_required
def wishlist():
    """wishlist"""
    account = session["account_id"]
    account_pic = db.execute(
        'SELECT account_pic FROM accounts WHERE account_id = :account', account=account)
    account_pic = account_pic[0]['account_pic']

    if request.method == 'POST':
        if request.get_json():
            req = request.get_json()
            if req['action'] == 'remove_wishlist':
                remove_wishlist(req)
                return 'test'
            elif req['action'] == 'done_wish':
                return doneWish(req)
        else:
            return addWish()
    else:

        wishlist = db.execute(
            'SELECT * FROM wishlist WHERE account_id = :account ORDER BY wishlist_id DESC', account=account)
        lang = userlangcheck()
        return render_template('wishlist.html', wishlist=wishlist, lang=lang, account_pic=account_pic)


def addWish():
    if not request.form.get('item-name') or not request.form.get('quantity'):
        return error('No input', 'No item name or no quantity inputed')
    else:
        wishlist_item = request.form.get('item-name').capitalize()
        wishlist_descr = request.form.get('descr').capitalize()
        wishlist_quantity = request.form.get('quantity')
        wishlist_qnt_units = request.form.get('qnt-units')

        account_id = session["account_id"]

        account_pic = db.execute(
            'SELECT account_pic FROM accounts WHERE account_id = :account_id', account_id=account_id)
        account_pic = account_pic[0]['account_pic']

        exists = db.execute('SELECT * FROM wishlist WHERE wishlist_item = :wishlist_item AND account_id = :account_id ORDER BY wishlist_item DESC',
                            wishlist_item=wishlist_item, account_id=account_id)

        if len(exists) == 1:
            # Items with this name already exists!!!
            return "editWish function"
            # return editWish(wishlist_item)

        # save date for trades table in db
        now = datetime.now()
        # dd/mm/YY H:M:S
        date = now.strftime("%d/%m/%Y %H:%M:%S")

        db.execute('INSERT INTO wishlist(wishlist_item, descr, wishlist_quantity, wishlist_qnt_units, date, account_id) VALUES (:wishlist_item, :wishlist_descr, :wishlist_quantity, :wishlist_qnt_units, :date, :account_id)',
                   wishlist_item=wishlist_item, wishlist_descr=wishlist_descr, wishlist_quantity=wishlist_quantity, wishlist_qnt_units=wishlist_qnt_units, date=date, account_id=account_id)

        # items = db.execute('SELECT * FROM items WHERE account_id = :account_id ORDER BY substr(date, 4) DESC', account_id=account_id)
        wishlist = db.execute(
            'SELECT * FROM wishlist WHERE account_id = :account_id ORDER BY wishlist_id DESC', account_id=account_id)
        # items = db.execute('SELECT * FROM items ORDER BY substr(date, 4) DESC')
        lang = userlangcheck()
        return render_template('wishlist.html', wishlist=wishlist, lang=lang, account_pic=account_pic)


def edit(itemfromadd='noadd'):
    # itemfromadd.capitalize()
    evnt = 'Updated'
    quantity_old = request.form.get('quantity_old')
    current_item_id = request.form.get('id_old')
    descr_old = request.form.get('descr_old')
    name_old = request.form.get('name_old')
    qnt_units_old = request.form.get('qnt_units_old')
    qnt_units = request.form.get('qnt-units')

    # by default updated values are the same as old, but after a checks they might be rewrited
    item_name_updated = name_old
    descr_updated = descr_old
    quantity_updated = quantity_old
    qnt_units_updated = qnt_units

    now = datetime.now()
    # dd/mm/YY H:M:S
    date = now.strftime("%d/%m/%Y %H:%M:%S")

    account_id = session["account_id"]
    account_pic = db.execute(
        'SELECT account_pic FROM accounts WHERE account_id = :account_id', account_id=account_id)
    account_pic = account_pic[0]['account_pic']

    # if no changes at all do nothing
    if not request.form.get('item-name') and not request.form.get('quantity') and not request.form.get('descr'):
        if qnt_units == qnt_units_old:
            # No changes at all!
            print("No changes at all!!!")
            # refresh the page
            items = db.execute(
                'SELECT * FROM items WHERE account_id = :account_id ORDER BY item_id DESC', account_id=account_id)
            lang = userlangcheck()
            return render_template('fridge.html', items=items, lang=lang, account_pic=account_pic)

    if request.form.get('item-name'):
        item_name = request.form.get('item-name')
        # if no changes
        if item_name == name_old:
            # "No changes in name!"
            print("No changes in name!")
        else:
            # name was changed
            item_name_updated = item_name

    if request.form.get('quantity'):
        quantity = request.form.get('quantity')
        # if no changes
        if quantity == quantity_old:

            print("No changes in quantity!")
        else:
            # qantity changed
            quantity_updated = quantity

    if request.form.get('qnt-units'):
        # if no changes
        if qnt_units == qnt_units_old:

            print("No changes in units!")
        else:
            # units was changed
            qnt_units_updated = qnt_units

    if request.form.get('descr'):
        descr = request.form.get('descr')
        # if no changes
        if descr == descr_old:
            print("No changes in descr!")
        else:
            # descr was changed
            descr_updated = descr

    # updating history if something was changed
    addtohistory(item_name_updated, descr_updated,
                 quantity_updated, qnt_units_updated, evnt, account_id)

    # update the item
    db.execute('UPDATE items SET item = :item_name_updated, descr = :descr_updated, quantity = :quantity_updated, qnt_units = :qnt_units_updated, date = :date, account_id = :account_id WHERE item_id = :current_item_id OR item = :itemfromadd',
               item_name_updated=item_name_updated, descr_updated=descr_updated, quantity_updated=quantity_updated, qnt_units_updated=qnt_units_updated, date=date, account_id=account_id, current_item_id=current_item_id, itemfromadd=itemfromadd)

    # refresh the page
    items = db.execute(
        'SELECT * FROM items WHERE account_id = :account_id ORDER BY item_id DESC', account_id=account_id)
    lang = userlangcheck()
    return render_template('fridge.html', items=items, lang=lang, account_pic=account_pic)


def remove(x):
    item_id = x['id']
    evnt = 'Removed'
    updateitem = x['name']
    quantity_updated = x['qantity']
    qnt_units = x['units']
    descr = x['descr']
    account_id = session["account_id"]

    addtohistory(updateitem, descr, quantity_updated,
                 qnt_units, evnt, account_id)

    db.execute('DELETE FROM items WHERE item_id = :id AND account_id = :account_id',
               id=item_id, account_id=account_id)


def error(args1, args2):
    ErrHeader = args1
    ErrText = args2
    return render_template('error.html', ErrHeader=ErrHeader, ErrText=ErrText)


def remove_wishlist(req):
    account_id = session["account_id"]
    evnt = req['action']
    wish_id = req['id']

    for wish_id in wish_id:
        db.execute('DELETE FROM wishlist WHERE wishlist_id = :wish_id AND account_id = :account_id',
                   wish_id=int(wish_id), account_id=account_id)


def doneWish(req):
    account_id = session["account_id"]

    wishitemslist = req['id']
    for row in wishitemslist:
        id = row
        doneWishItem = db.execute(
            'SELECT * FROM wishlist WHERE account_id = :account_id AND wishlist_id = :id', account_id=account_id, id=id)

        item = doneWishItem[0]['wishlist_item']
        descr = doneWishItem[0]['descr']
        quantity = float(doneWishItem[0]['wishlist_quantity'])
        qnt_units = doneWishItem[0]['wishlist_qnt_units']

        add(item, descr, quantity, qnt_units)
        db.execute('DELETE FROM wishlist WHERE wishlist_item = :item AND account_id = :account_id',
                   item=item, account_id=account_id)

    print('update page here')
    items = db.execute(
        'SELECT * FROM items WHERE account_id = :account_id ORDER BY item_id DESC', account_id=account_id)
    lang = userlangcheck()
    return render_template('fridge.html', items=items, lang=lang, account_pic=account_pic)


def add(item='no input', descr='no input', quantity='no input', qnt_units='no input'):
    evnt = 'Added'
    # save date for trades table in db
    now = datetime.now()
    # dd/mm/YY H:M:S
    date = now.strftime("%d/%m/%Y %H:%M:%S")

    if item != 'no input':
        item = item
        descr = descr
        quantity = quantity
        qnt_units = qnt_units
    else:
        if not request.form.get('item-name') or not request.form.get('quantity'):
            return error('No input', 'No item name or no quantity input')
        else:
            item = request.form.get('item-name').capitalize()
            descr = request.form.get('descr').capitalize()
            quantity = request.form.get('quantity')
            qnt_units = request.form.get('qnt-units')

    account_id = session["account_id"]

    account_pic = db.execute(
        'SELECT account_pic FROM accounts WHERE account_id = :account_id', account_id=account_id)
    account_pic = account_pic[0]['account_pic']

    exists = db.execute(
        'SELECT * FROM items WHERE item = :item AND account_id = :account_id ORDER BY item_id DESC', item=item, account_id=account_id)
    if len(exists) == 1:
        # Items with this name already exists!!!

        # check if donewish
        if item != 'no input':
            evnt = 'Updated'

            # update the item
            db.execute('UPDATE items SET item = :item_name_updated, descr = :descr_updated, quantity = :quantity_updated, qnt_units = :qnt_units_updated, date = :date, account_id = :account_id WHERE item = :item_name',
                       item_name_updated=item, descr_updated=descr, quantity_updated=quantity, qnt_units_updated=qnt_units, date=date, account_id=account_id, item_name=item)
            addtohistory(item, descr, quantity, qnt_units, evnt, account_id)
            items = db.execute(
                'SELECT * FROM items WHERE account_id = :account_id ORDER BY item_id DESC', account_id=account_id)
            lang = userlangcheck()
            return render_template('fridge.html', items=items, lang=lang, account_pic=account_pic)
        else:
            return edit(item)

    addtohistory(item, descr, quantity, qnt_units, evnt, account_id)

    db.execute('INSERT INTO items(item, descr, quantity, qnt_units, date, account_id) VALUES (:item, :descr, :quantity, :qnt_units, :date, :account_id)',
               item=item, descr=descr, quantity=quantity, qnt_units=qnt_units, date=date, account_id=account_id)

    items = db.execute(
        'SELECT * FROM items WHERE account_id = :account_id ORDER BY item_id DESC', account_id=account_id)
    lang = userlangcheck()
    return render_template('fridge.html', items=items, lang=lang, account_pic=account_pic)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/user', methods=['GET', 'POST'])
@login_required
def user():

    account = session["account_id"]
    account_pic = db.execute(
        'SELECT account_pic FROM accounts WHERE account_id = :account', account=account)
    account_pic = account_pic[0]['account_pic']
    email = db.execute(
        'SELECT email FROM accounts WHERE account_id =:account', account=account)[0]['email']

    if request.method == 'POST':
        # print(f'request.form length: {len(request.form)}')
        # print(f'request.files length: {len(request.files)}')

        if len(request.form) != 0:
            return langchange(account)
        elif len(request.files) != 0:
            return upload_file()

    else:
        lang = userlangcheck()
        return render_template('user.html', account_pic=account_pic, lang=lang, email=email)


def upload_file():
    account = session["account_id"]
    account_pic = db.execute(
        'SELECT account_pic FROM accounts WHERE account_id = :account', account=account)
    account_pic = account_pic[0]['account_pic']
    email = db.execute(
        'SELECT email FROM accounts WHERE account_id =:account', account=account)[0]['email']

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            #  remove previous photo file and
            try:
                if account_pic != 'default.png':
                    path = f'static/userpics/{account_pic}'
                    os.remove(path)
            except:
                print('No file, can\'t remove it')

            # set a filename with specific format includes account_id, random float (1-100) and original file name + it's extension
            rand = random.uniform(1, 100)
            filename = str(account) + '_' + str(rand) + '_' + filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            db.execute('UPDATE accounts SET account_pic = :account_pic WHERE account_id = :account',
                       account_pic=filename, account=account)

            # return redirect(url_for('file_', filename=filename))
            return redirect('/user')

    # account = session["account_id"]
    else:
        lang = userlangcheck()
        return render_template('user.html', account_pic=account_pic, lang=lang, email=email)


def langchange(accountid):
    account_id = accountid
    choosenLang = request.form.get('lang')
    db.execute('UPDATE accounts SET lang = :choosenLang WHERE account_id = :account_id',
               choosenLang=choosenLang, account_id=account_id)
    return redirect('/user')


@app.route("/logout", methods=['GET', 'POST'])
def logout():
    session.clear()
    return render_template('signin.html')


@app.errorhandler(404)
def page_not_found(e):
    return error('404', 'Page not found'), 404


@app.route('/restore_pass', methods=['GET', 'POST'])
def restore():

    return render_template('restore_pass.html')
