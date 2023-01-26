from main.models import db, User, Info
from uuid import uuid4
from validate_email import validate_email
import re


def usernameCheck(username):
    # username = input("Enter a username")  # User enters username
    # check username
    # Regex used to make sure username follows:
    # within 2 to 20 char limit
    # alphanumeric only
    # one space that is not a suffix or prefix
    regexUsername = "^[a-zA-Z0-9]+[a-zA-Z0-9 ]?[a-zA-Z0-9]+$"
    if not username:  # Username was left empty
        return False  # "username was left empty"

    # Checks if username was outside the 2-20 char limit:
    if not (2 < len(username) < 20):
        return False  # "The length of the username is incorrect"

    # Checks if the username is within the regex:
    if re.match(regexUsername, username) is None:
        return False  # "Username not allowed within parameters"

    return True


def emailCheck(email):
    # Check email
    # regex expressions used to
    # check if email follows RCF 5322

    if not email:
        return False  # "email was left empty"

    if not validate_email(email):
        return False  # "Email does not follow RCF 5322"

    existed = User.query.filter_by(email=email).all()
    if len(existed) > 0:
        return False  # "this email has been used before"
    return True


def emailCheck_login(email):
    # Check email
    # regex expressions used to
    # This does not check for existed emails
    # check if email follows RCF 5322
    if not email:
        return False  # "email was left empty"

    if not validate_email(email):
        return False  # "Email does not follow RCF 5322"

    return True


def passwordCheck(password):
    # password = input("Enter a password")
    # Check password
    # Regex to make sure password follows:
    # min length 6
    # At least one upper case
    # At least one lower case
    # At least one special char
    regexPassword = '^(?=.*[a-z])(?=.*[A-Z])' \
                    '(?=.*\W)[A-Za-z\d\W]{6,}$'

    if not password:
        return False  # ("password was left empty")

    if re.match(regexPassword, password) is None:
        return False  # "Password does not adhere to specifications")

    return True


def user_login(email, password):
    """
    LOGIN CHECK
    """
    valids = User.query.filter_by(email=email, password=password).all()
    if not emailCheck_login(email) or not passwordCheck(password):
        return False  # email or password checks failed
    if len(valids) != 1:
        return False  # Login Failed
    # Login Successful
    return valids[0]


def user_registration(email, username, password):
    # Function to ask user to input registration data

    if emailCheck(email) and usernameCheck(username) \
            and passwordCheck(password):
        registerUser = User(
            user_id=str(uuid4()), email=email, username=username,
            password=password)
        db.session.add(registerUser)
        db.session.commit()
        # return registerUser  # For Testing
        return True
    return False


def updateProfile(userId, username, email):
    """
    test_user = User(user_id='123345678',
                     email='test@test.com',
                     username='user 00',
                     password='87654321',
    db.session.add(test_user)
    """
    # check if username and email are valid
    if usernameCheck(username) and emailCheck_login(email):
        # find the user with the same user_id as the current user in the db
        updateUser = User.query.filter_by(user_id=userId).first()

        # update rows in the db for the corresponding user
        updateUser.username = username
        updateUser.email = email
        db.session.commit()
        # changes were successful
        return True
