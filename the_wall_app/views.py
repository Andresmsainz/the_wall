from django.shortcuts import render, redirect
from .models import User, Wall_Message, Comment
from django.contrib import messages
import bcrypt


# Create your views here.
def index(request):
    if 'user_id' in request.session:  #Is the user logged in
        user = User.objects.filter(id=request.session['user_id'])
        if user:
            return redirect("/success") #no matter what success handles the view and the session

    return render(request, "login.html")

def success(request):
    if 'user_id' in request.session:  #Is the user logged in
        user = User.objects.filter(id=request.session['user_id'])
        if user:
            context = {
                'user': user[0], #0 is the first record
                'wall_messages': Wall_Message.objects.all()
            }

            return render(request,'login_success.html', context) #if valid user than we move on to success

        return redirect("/") #if not a valid user then go back to root

    return redirect("/") #if no user then go back to root

def login(request):
    # see if the username provided exists in the database
    user = User.objects.filter(email=request.POST['email']) # why are we using filter here instead of get?
    if user: # note that we take advantage of truthiness here: an empty list will return false
        logged_user = user[0] 
        # assuming we only have one user with this username, the user would be first in the list we get back
        # of course, we should have some logic to prevent duplicates of usernames when we create users
        # use bcrypt's check_password_hash method, passing the hash from our database and the password from the form
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            # if we get True after checking the password, we may put the user id in session
            request.session['user_id'] = logged_user.id
            # never render on a post, always redirect!
            return redirect('/success')
    # if we didn't find anything in the database by searching by username or if the passwords don't match, 
    # redirect back to a safe route
    return redirect("/")
    
def logout(request):
    request.session.clear()
    return redirect("/")

def register(request):
    if request.method == "POST":
        # pass the post data to the method we wrote and save the response in a variable called errors
        errors = User.objects.basic_validator(request.POST)
        # check if the errors dictionary has anything in it
        if len(errors) > 0:
            # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/") #if not a valid request then go back to root
        else:
            # include some logic to validate user input before adding them to the database!
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()  # create the hash    
            print(pw_hash)      # prints something like b'$2b$12$sqjyok5RQccl9S6eFLhEPuaRaJCcH3Esl2RWLm/cimMIEnhnLb7iC'    
            # be sure you set up your database so it can store password hashes this long (60 characters)
            # make sure you put the hashed password in the database, not the one from the form!
            new_user = User.objects.create(
                first_name=request.POST['firstname'],
                last_name=request.POST['lastname'],
                email=request.POST['email'], 
                password=pw_hash
            ) 

            request.session['user_id'] = new_user.id
            messages.success(request, "New User successfully updated")
            return redirect('/success') # never render on a post, always redirect!

    return redirect("/") #if not a valid request then go back to root

def post_message(request):
    if request.method == "POST":
        if 'user_id' in request.session:  #Is the user logged in
            user = User.objects.get(id=request.session['user_id']) #create instance of user to add to record
            Wall_Message.objects.create(
                message=request.POST['post_message'],
                poster=user,
            )

    return redirect("/success") #no matter what success handles the view and the session


def post_comment(request,wall_message_id):
    if request.method == "POST":
        if 'user_id' in request.session:  #Is the user logged in
            user = User.objects.get(id=request.session['user_id']) #create instance of user to add to record
            wall_message = Wall_Message.objects.get(id=wall_message_id) #create instance of wall message to add to record

            Comment.objects.create(
                message=request.POST['post_comment'],
                poster=user,
                wall_message=wall_message
            )

    return redirect("/success") #no matter what success handles the view and the session