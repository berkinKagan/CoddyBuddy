from django.shortcuts import redirect, render
from django.contrib.auth.models import User, auth
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from .tokens import account_activation_token, password_change_token
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from .models import Post, Profile, TOOL_CHOICES
from django.http import HttpResponse
from django.contrib.sessions.middleware import SessionMiddleware
from django import forms


def home(request):
    currentUser = request.user
    profile = Profile.objects.get(user = currentUser)
    Posts = Post.objects.all()
    Posts = Post.objects.order_by('-created_at')
    choices = TOOL_CHOICES
    return render(request, "home.html", {"currentUser" : currentUser, "profile" : profile, "posts" : Posts, "choices" : choices})

def logOut(request):
    logout(request)
    
    return redirect('logIn') 


    

def logIn(request):
    message1 = ""
    
    if request.method == 'POST':
        usernameUp = request.POST.get('usernameUp')
        emailUp = request.POST.get('emailUp')
        passwordUp = request.POST.get("passwordUp")
        usernameIn = request.POST.get('usernameIn')
        passwordIn = request.POST.get('passwordIn')
        
        if(usernameUp != None and emailUp != None and passwordUp != None):
            if User.objects.filter(email = emailUp).exists() or User.objects.filter(username = usernameUp).exists():
                pass
            else:
                user = User.objects.create_user(username=usernameUp, email=emailUp, password=passwordUp)
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                mail_subject = "Activation link has been sent to your email"
                message = render_to_string("activation.html", {
                    "user" : user,
                    "domain" : current_site.domain,
                    "uid" : urlsafe_base64_encode(force_bytes(user.pk)),
                    "token" : account_activation_token.make_token(user),
                })
                to_email = emailUp
                email = EmailMessage(
                    mail_subject, message , to = [to_email]
                )
                email.send()
                msg = "Please make your email verification"  
        elif(usernameIn != None and passwordIn != None):   
             user = auth.authenticate(username = usernameIn, password = passwordIn)
             if user != None:
                auth.login(request,user)
                return redirect('home')
             else:
                message1 = "Invalid Credential"
                print("check2")
                return render (request,"logIn.html",{"error" : message1}) 
        
    
    return render (request,"logIn.html",{"error" : message1})

def activate(request, uid, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uid))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, "verify.html")
    else:
        return render(request, "verify.html")
    
def changePassword(request):
    currentUser = request.user
    oldPsw = currentUser.password
    if request.method == "POST":
        psw = request.POST.get("input1")
        pswAgain = request.POST.get("input2")
        
        if psw != pswAgain:
            messages.error(request, "Passwords do not match!")
        elif(len(psw) < 8 or len(psw) > 20):
            messages.error(request, "Passwords should be between 8-20 length!")   
        else:
            request.session['newPassword'] = psw
            current_site = get_current_site(request)
            mail_subject = "Password change link has been sent to your email"
            message = render_to_string("confirmPsw.html", {
                "user" : currentUser,
                "domain" : current_site.domain,
                "uid" : urlsafe_base64_encode(force_bytes(currentUser.pk)),
                "token" : password_change_token.make_token(currentUser),
            })
            to_email = currentUser.email
            email = EmailMessage(
                mail_subject, message , to = [to_email]
            )
            email.send()
            messages.success(request, "The link for the change has been sent your mail!")
                   
    return render(request, "changePassword.html", {"currentUser" : currentUser})

def confirmPsw(request, uid, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uid))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and password_change_token.check_token(user, token):
        user.set_password(request.session['newPassword'])
        print(request.session['newPassword'])
        user.save()
        return render(request, "logIn.html")
    else:
        return render(request, "logIn.html")
                

def profile(request,pk):
    currentUser = User.objects.get(id = pk)
    profile = Profile.objects.get(user = currentUser)
    return render(request,'profile.html', {'currentUser' : currentUser, 'profile' : profile})

def editProfile(request):
    currentUser = request.user
    profile = Profile.objects.get(user = currentUser)
    message = ""
    
    if request.method == 'POST':
        newUsername = request.POST.get("username")
        newBio = request.POST.get("bio")
        img = request.FILES.get("img")
        print(img)
        if newUsername != None:
            currentUser.username = newUsername
            currentUser.save()
        if newBio != None:
             profile.bio = newBio
             profile.save() 
        if img != None:
             profile.image = img
             profile.save()          
        
        return redirect("home")
        
            
            
    return render(request, "editProfile.html",{"currentUser" : currentUser, "message" : message, "profile" : profile})

def createPost(request):
    newpost = None
    currentUser = request.user
    if request.method == "POST":
      postTitle = request.POST.get('postTitle')
      answer = request.POST['tool']
      try:
          answer0 = request.POST['tool0']
      except:
          answer0 = ""
      try:
          answer1 = request.POST['tool1']
      except:
          answer1 = ""
      try:
          answer2 = request.POST['tool2']
      except:
          answer2 = ""
      
      try:
          answer3 = request.POST['tool3']
      except:
          answer3 = ""    
      
      answer = answer +"\n"+ answer0+"\n"+answer1+"\n"+answer2+"\n"+answer3
      description = request.POST.get('description')
      numberOfMember = request.POST.get('numberOfMember')
      print(answer)
      if(postTitle != None and answer != None and description != None and numberOfMember != None):
          newpost = Post(owner = currentUser, title = postTitle, tool = answer, description = description, max_capacity = int(numberOfMember))
          print("Check")
          newpost.save()
          return redirect('home')
            
    return render(request, "home.html")