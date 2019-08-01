from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from notify.signals import notify
from pages.models import Documents, Profile
from pages.forms import SignUpForm, ProfileForm, DocumentForm


def index(request):
    """
    login view
    :param request:user name, password
    :return:provides authentication to session page
    """
    if request.method == "POST":
        un = request.POST.get("username", None)
        utype = request.POST.get("type", None)
        print(utype)
        if un:
            psw = request.POST.get("password", None)
            print(psw)
            user = authenticate(request, username=un, password=psw)
            if user:
                login(request, user)
                profile = Profile.objects.filter(user=request.user)
                profile = profile.first()
                user_type = profile.user_type
                if user_type == utype:
                    if user_type == "admin":
                        return redirect('/upload')
                    elif user_type == "user2":
                        return redirect('/document_list')
                    else:
                        return HttpResponse(" invalid user type")

    return render(request, 'login.html', locals())


def signup(request):
    """
    Register form
    :param request: creating new account
    :return: create an account and return to next page
    """
    if request.method == 'POST':
        user_form = SignUpForm(request.POST, prefix="user")
        profile_form = ProfileForm(request.POST, prefix="user-profile")
        if user_form.is_valid() and profile_form.is_valid():
            u = user_form.save(commit=False)
            u.set_password(u.password)
            u.save()
            up = profile_form.save(commit=False)
            up.user = u
            up.save()
            print("save successfully.")
            if up.user_type == "admin":
                return redirect('/upload')
            elif up.user_type == "user2":
                return redirect('/document_list')
            else:
                return HttpResponse("user type must to be either admin or user 2")
    else:
        user_form = SignUpForm(prefix="user")
        profile_form = ProfileForm(prefix="user-profile")
    return render(request, 'home.html', locals())


@login_required(login_url="/")
def upload(request):
    """
    for uploading file
    :param request: file to be uploaded(1st user)
    :return:
    """
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            profile = Profile.objects.filter(user_type="user2")
            profile = profile.first()
            profile_list = [profile.user]
            notify.send(request.user, recipient_list=profile_list, actor=request.user, verb='uploaded.')
            return redirect('list_document')
    else:
        form = DocumentForm()
    return render(request, 'upload_document.html', locals())


@login_required(login_url="/")
def list_document(request):
    """
    for displaying all the files(1nd user)
    :param request:
    :return: uploaded files details
    """
    document = Documents.objects.all()
    return render(request, 'list_document.html', locals())


@login_required(login_url="/")
def document_list(request):
    """
    for displaying all the files(2nd user)
    :param request:
    :return: uploaded files details with delete and download
    """
    document = Documents.objects.all()
    return render(request, 'document_list.html', locals())


@login_required(login_url="/")
def delete_document(request, pk):
    """
    For deleting the file(2nd user)
    :param request:
    :param pk: file to be deleted
    :return: deleting the file from list and displaying remaining files
    """
    if request.method == 'POST':
        document = Documents.objects.get(pk=pk)
        document.delete()
    return redirect('document_list')


@login_required(login_url="/")
def logout_view(request):
    """

    :param request:
    :return: closing the project
    """
    logout(request)
    return render(request, 'logout.html')
