import re
from flask import Flask, render_template, request, make_response
import os

app = Flask(__name__)
application = app

prefix = os.environ.get('URL_PREFIX', '')
if prefix:
    class PrefixMiddleware:
        def __init__(self, wsgi_app, prefix):
            self.wsgi_app = wsgi_app
            self.prefix = prefix
        def __call__(self, environ, start_response):
            environ['SCRIPT_NAME'] = self.prefix
            return self.wsgi_app(environ, start_response)
    app.wsgi_app = PrefixMiddleware(app.wsgi_app, prefix)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/url_params')
def url_params():
    return render_template('url_params.html', params=request.args)


@app.route('/headers')
def headers():
    return render_template('headers.html', headers=request.headers)


@app.route('/cookies', methods=['GET', 'POST'])
def cookies():
    if request.method == 'POST':
        key = request.form.get('key', '')
        value = request.form.get('value', '')
        resp = make_response(render_template('cookies.html', cookies=request.cookies))
        if key:
            resp.set_cookie(key, value)
        return resp
    return render_template('cookies.html', cookies=request.cookies)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form_data = None
    if request.method == 'POST':
        form_data = {
            'login': request.form.get('login', ''),
            'password': request.form.get('password', '')
        }
    return render_template('login.html', form_data=form_data)


ALLOWED_CHARS = set('0123456789 ()-.+')

def validate_phone(raw):
    if not raw or raw.strip() == '':
        return None, 'Недопустимый ввод. В номере телефона встречаются недопустимые символы.'

    for ch in raw:
        if ch not in ALLOWED_CHARS:
            return None, 'Недопустимый ввод. В номере телефона встречаются недопустимые символы.'

    digits = re.sub(r'\D', '', raw)

    if raw.strip().startswith('+7') or raw.strip().startswith('8'):
        if len(digits) != 11:
            return None, 'Недопустимый ввод. Неверное количество цифр.'
    else:
        if len(digits) != 10:
            return None, 'Недопустимый ввод. Неверное количество цифр.'

    # normalize to 10-digit base
    if len(digits) == 11:
        digits = digits[1:]

    formatted = f'8-{digits[0:3]}-{digits[3:6]}-{digits[6:8]}-{digits[8:10]}'
    return formatted, None


@app.route('/phone', methods=['GET', 'POST'])
def phone():
    phone_value = ''
    error = None
    formatted = None
    if request.method == 'POST':
        phone_value = request.form.get('phone', '')
        formatted, error = validate_phone(phone_value)
    return render_template('phone.html', phone_value=phone_value, error=error, formatted=formatted)