from flask import Flask, request, make_response, render_template, redirect, url_for


app = Flask(__name__)


@app.get('/')
def home():
    return render_template('base.html')

@app.route('/form/', methods=['GET', 'POST'])
def form_to_fill():
    if request.method == 'POST':
       name = request.form.get('username')
       email = request.form.get('email')
       response = make_response(redirect(url_for('answer')))
       response.set_cookie('user', name)
       response.set_cookie('email', email)
       return response
    return render_template('form.html')


@app.route('/answer/', methods=['GET', 'POST'])
def answer():
    if request.method == 'POST':
        response = make_response(redirect(url_for('form_to_fill')))
        response.delete_cookie('user')
        response.delete_cookie('email')
        return response
        
    user_name = request.cookies.get('user')
    if user_name:
        return render_template('hello.html', title='Hello', name=user_name)
    return redirect(url_for('form_to_fill'))


if __name__ == '__main__':
    app.run(debug=True)