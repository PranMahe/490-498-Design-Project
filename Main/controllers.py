from flask import render_template, request, session, redirect
from main.models import User, Info
from main import app
from main.backend import (user_login, user_registration,
                          updateProfile, usernameCheck,
                          emailCheck_login, passwordCheck,
                          emailCheck)


def authenticate(inner_function):
    """
    :param inner_function: any python function that accepts a user object
    Wrap any python function and check the current session to see if
    the user has logged in. If login, it will call the inner_function
    with the logged in user object.
    To wrap a function, we can put a decoration on that function.
    Example:
    @authenticate
    def home_page(user):
        pass
    """
    def wrapped_inner(*args, **kwargs):
        # check did we store the key in the session
        if 'logged_in' in session:
            user_id = session['logged_in']
            try:
                user = User.query.filter_by(user_id=user_id).one_or_none()
                if user:
                    # if the user exists, call the inner_function
                    # with user as parameter
                    return inner_function(user, *args, **kwargs)

            except Exception as e:
                print(e)
                return redirect('/login')
        else:
            # else, redirect to the login page
            return redirect('/login')

    # Renaming the function name:
    wrapped_inner.__name__ = inner_function.__name__
    # return the wrapped version of the inner_function:
    return wrapped_inner


@app.route('/login', methods=['GET'])
def login_get():
    return render_template('login.html', message='Please login')


@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    user = user_login(email, password)
    if user:
        session['logged_in'] = user.user_id
        """
        Session is an object that contains sharing information 
        between a user's browser and the end server. 
        Typically it is packed and stored in the browser cookies. 
        They will be past along between every request the browser made 
        to this services. Here we store the user object into the 
        session, so we can tell if the client has already login 
        in the following sessions.
        """
        # success! go back to the home page
        # code 303 is to force a 'GET' request
        return redirect('/', code=303)
    else:
        if emailCheck_login(email) is False:
            error_message = "Email input incorrect format"
        elif passwordCheck(password) is False:
            error_message = "Password input incorrect format"
        else:
            error_message = "Login Failed"

        return render_template('login.html', message=error_message)


@app.route('/', methods=['GET', 'POST'])
@authenticate
def home(user):
    # authentication is done in the wrapper function
    # see above.
    # by using @authenticate, we don't need to re-write
    # the login checking code all the time for other
    # front-end portals


    return render_template('index.html', user=user)


@app.route('/register', methods=['GET'])
def register_get():
    # templates are stored in the templates folder
    return render_template('register.html', message='')


@app.route('/register', methods=['POST'])
def register_post():
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    error_message = None

    if password != password2:
        error_message = "The passwords do not match"
    else:
        # use backend api to register the user
        success = user_registration(email, username, password)
        if not success:
            if emailCheck(email) is False:
                error_message = "Email input failed."
            elif usernameCheck(username) is False:
                error_message = "Username input failed."
            elif passwordCheck(password) is False:
                error_message = "Password input failed."

    # if there is any error messages when registering new user
    # at the backend, go back to the register page.
    if error_message:
        return render_template('register.html', message=error_message)
    else:
        return redirect('/login')


@app.route('/updateUser', methods=['GET'])
@authenticate
def update_get(user):
    # stored in the webpages folder
    return render_template('/updateUser.html', user=user, message="")


@app.route('/updateUser', methods=['POST'])
@authenticate
def update_post(user):
    user_ID = user.user_id
    username = request.form.get('username')
    user_email = request.form.get('email')
    billing_address = request.form.get('billingAddress')
    postal_code = request.form.get('postalCode')
    error_message = None

    success = updateProfile(user_ID, username, user_email)
    if not success:
        if usernameCheck(username) is False:
            error_message = 'Invalid Username'
        elif emailCheck(user_email) is False:
            error_message = 'Invalid Email'

    if error_message:
        return render_template('updateUser.html',
                               user=user, message=error_message)
    else:
        return redirect('/')
