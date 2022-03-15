from django.shortcuts import render, redirect, get_object_or_404
from .forms import LoginForm, RegisterForm
from django.http import HttpResponse
from .models import Student, Question, Exams
from django.contrib import messages
from datetime import datetime,date

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.success(request, "Successfully saved")
            return  redirect('/login')
    else:
        form = RegisterForm()

    return render(request, 'reg_form.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            exam = Exams.objects.all()
            ur = form.cleaned_data['username']
            print(ur)
            pd = form.cleaned_data['password']
            print("this is password",pd)
            dbuser = Student.objects.filter(user=ur, password=pd)
            if not dbuser:
                return HttpResponse('Login failed')
            else:
                request.session['z'] = ur
                print("This is ur",ur)
                request.session.get_expiry_age()
                instance = get_object_or_404(Student, user=ur)
                return render(request, 'examopt.html', {'exam': exam, 'ur': ur, 'instance': instance})
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})


def exams(request):
    if request.session.has_key('z'):
        print(request.session.has_key('z'),"Has key")
        name = request.GET.get('name')
        print(name)
        name=request.session['name'] =name
        a = request.session['z']
        exam = Exams.objects.filter(exam_name=name)
        context = {
            'exam': exam,
            'ur': a,
            'exam_name': name,
        }
        return render(request, 'exams1.html', context)


def home(request):
    return render(request, 'index.html')



def start_exam(request):
    if request.session.has_key('z'):
        name = request.session['name']
        exam = Exams.objects.filter(exam_name=name)
        print("Exam:",exam)
        time=datetime.now()
        current_time = time.strftime("%H:%M:%S")
        print(current_time)
        ques = Question.objects.all().filter(exam_name__in=exam)
        print("ques",ques)

        return render(request, '1.html', {'ques': ques,"TIME":current_time})


def report(request):
    ur = request.session['z']
    print("report",request.method)
    # print(ur,"Hello Ajay")
    name = request.session['name']
    context = {
        'ur': ur,
        'name': name,
    }
    return render(request, 'REPORT.html', context)

def view_result(request):
    ur = request.session['z']        # user
    name = request.session['name']   # subject name
    print(name)
    exam = Exams.objects.filter(exam_name=name)[0]
    date1=date.today().strftime('%d/%m/%Y') 
    print(request.method)
    d={"ur":ur,"name":name,"exam":exam,"date":date1}
    return render(request,"view_result.html",d)


def logout(request):
    if request.session.has_key('z'):
        request.session.flush()
    return redirect('/home')
