from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import json
from college_management_app.forms import AddStudentForm, EditStudentForm
from college_management_app.models import Courses, CustomUser, Teachers, Subjects, Students, SessionYearModel, FeedbackStudent, FeedbackTeachers, LeaveReportStudent, LeaveReportTeacher, Attendance, AttendanceReport, StudentFee


def admin_home(request):
    student_count=Students.objects.all().count()
    teacher_count=Teachers.objects.all().count()
    subject_count=Subjects.objects.all().count()
    course_count=Courses.objects.all().count()

    course_all=Courses.objects.all()
    course_name_list=[]
    subject_count_list=[]
    student_count_list_in_course=[]
    for course in course_all:
        subjects=Subjects.objects.filter(course_id=course.id).count()
        students=Students.objects.filter(course_id=course.id).count()
        course_name_list.append(course.course_name)
        subject_count_list.append(subjects)
        student_count_list_in_course.append(students)

    subjects_all=Subjects.objects.all()
    subject_list=[]
    student_count_list_in_subject=[]
    for subject in subjects_all:
        course=Courses.objects.get(id=subject.course_id.id)
        student_count=Students.objects.filter(course_id=course.id).count()
        subject_list.append(subject.subject_name)
        student_count_list_in_subject.append(student_count)

    teachers=Teachers.objects.all()
    attendance_present_list_teacher=[]
    attendance_absent_list_teacher=[]
    teacher_name_list=[]
    for teacher in teachers:
        subject_ids=Subjects.objects.filter(teacher_id=teacher.admin.id)
        attendance=Attendance.objects.filter(subject_id__in=subject_ids).count()
        leaves=LeaveReportTeacher.objects.filter(teacher_id=teacher.id,leave_status=1).count()
        attendance_present_list_teacher.append(attendance)
        attendance_absent_list_teacher.append(leaves)
        teacher_name_list.append(teacher.admin.username)

    students_all=Students.objects.all()
    attendance_present_list_student=[]
    attendance_absent_list_student=[]
    student_name_list=[]
    for student in students_all:
        attendance=AttendanceReport.objects.filter(student_id=student.id,status=True).count()
        absent=AttendanceReport.objects.filter(student_id=student.id,status=False).count()
        leaves=LeaveReportStudent.objects.filter(student_id=student.id,leave_status=1).count()
        attendance_present_list_student.append(attendance)
        attendance_absent_list_student.append(leaves+absent)
        student_name_list.append(student.admin.username)
    return render(request,"hod_template/home_content.html",{"student_count":student_count,"teacher_count":teacher_count,"subject_count":subject_count,"course_count":course_count,"course_name_list":course_name_list,"subject_count_list":subject_count_list,"student_count_list_in_course":student_count_list_in_course,"student_count_list_in_subject":student_count_list_in_subject,"subject_list":subject_list,"teacher_name_list":teacher_name_list,"attendance_present_list_teacher":attendance_present_list_teacher,"attendance_absent_list_teacher":attendance_absent_list_teacher,"student_name_list":student_name_list,"attendance_present_list_student":attendance_present_list_student,"attendance_absent_list_student":attendance_absent_list_student})

def add_teacher(request):
    return render(request,"hod_template/add_teacher_template.html")

def add_teacher_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        address=request.POST.get("address")
        try:
            user=CustomUser.objects.create_user(username=username,password=password,email=email,last_name=last_name,first_name=first_name,user_type=2)
            user.teachers.address=address
            user.save()
            messages.success(request,"Successfully Added Teacher")
            return HttpResponseRedirect(reverse("add_teacher"))
        except:
            messages.error(request,"Failed to Add Teacher")
            return HttpResponseRedirect(reverse("add_teacher"))

def add_course(request):
    return render(request,"hod_template/add_course_template.html")

def add_course_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        course=request.POST.get("course")
        try:
            course_model=Courses(course_name=course)
            course_model.save()
            messages.success(request,"Successfully Added Course")
            return HttpResponseRedirect(reverse("add_course"))
        except:
            messages.error(request,"Failed To Add Course")
            return HttpResponseRedirect(reverse("add_course"))

def add_student(request):
    form=AddStudentForm()
    return render(request,"hod_template/add_student_template.html",{"form":form})

def add_student_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        form=AddStudentForm(request.POST,request.FILES)
        if form.is_valid():
            first_name=form.cleaned_data["first_name"]
            last_name=form.cleaned_data["last_name"]
            username=form.cleaned_data["username"]
            email=form.cleaned_data["email"]
            password=form.cleaned_data["password"]
            address=form.cleaned_data["address"]
            session_year_id=form.cleaned_data["session_year_id"]
            course_id=form.cleaned_data["course"]
            gender=form.cleaned_data["gender"]

            profile_pic=request.FILES['profile_pic']
            fs=FileSystemStorage()
            filename=fs.save(profile_pic.name,profile_pic)
            profile_pic_url=fs.url(filename)

            try:
                user=CustomUser.objects.create_user(username=username,password=password,email=email,last_name=last_name,first_name=first_name,user_type=3)
                user.students.address=address
                course_obj=Courses.objects.get(id=course_id)
                user.students.course_id=course_obj
                session_year=SessionYearModel.object.get(id=session_year_id)
                user.students.session_year_id=session_year
                user.students.gender=gender
                user.students.profile_pic=profile_pic_url
                user.save()
                messages.success(request,"Successfully Added Student")
                return HttpResponseRedirect(reverse("add_student"))
            except:
                messages.error(request,"Failed to Add Student")
                return HttpResponseRedirect(reverse("add_student"))
        else:
            form=AddStudentForm(request.POST)
            return render(request,"hod_template/add_student_template.html",{"form":form})



def add_subject(request):
    courses=Courses.objects.all()
    teachers=CustomUser.objects.filter(user_type=2)
    return render(request,"hod_template/add_subject_template.html",{"teachers":teachers,"courses":courses})

def add_subject_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        subject_name=request.POST.get("subject_name")
        course_id=request.POST.get("course")
        course=Courses.objects.get(id=course_id)
        teacher_id=request.POST.get("teacher")
        teacher=CustomUser.objects.get(id=teacher_id)
    
        try:
            subject=Subjects(subject_name=subject_name,course_id=course,teacher_id=teacher)
            subject.save()
            messages.success(request,"Successfully Added Subject")
            return HttpResponseRedirect(reverse("add_subject"))
        except:
            messages.error(request,"Failed to Add Subject")
            return HttpResponseRedirect(reverse("add_subject"))

def manage_teacher(request):
        teachers=Teachers.objects.all()
        return render(request,"hod_template/manage_teacher_template.html",{"teachers":teachers})

def manage_student(request):
        students=Students.objects.all()
        return render(request,"hod_template/manage_student_template.html",{"students":students})

def manage_course(request):
        courses=Courses.objects.all()
        return render(request,"hod_template/manage_course_template.html",{"courses":courses})

def manage_subject(request):
        subjects=Subjects.objects.all()
        return render(request,"hod_template/manage_subject_template.html",{"subjects":subjects})

def edit_teacher(request,teacher_id):
    teacher=Teachers.objects.get(admin=teacher_id)
    return render(request,"hod_template/edit_teacher_template.html",{"teacher":teacher, "id":teacher_id})

def edit_teacher_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        teacher_id=request.POST.get("teacher_id")
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        email=request.POST.get("email")
        username=request.POST.get("username")
        address=request.POST.get("address")

        try:
            user=CustomUser.objects.get(id=teacher_id)
            user.first_name=first_name
            user.last_name=last_name
            user.email=email
            user.username=username
            user.save()

            teacher_model=Teachers.objects.get(admin=teacher_id)
            teacher_model.address=address
            teacher_model.save()
            messages.success(request,"Successfully Edited Teacher")
            return HttpResponseRedirect(reverse("edit_teacher",kwargs={"teacher_id":teacher_id}))
        except:
            messages.error(request,"Failed to Edit Teacher")
            return HttpResponseRedirect(reverse("edit_teacher",kwargs={"teacher_id":teacher_id}))

def edit_student(request,student_id):
    request.session['student_id']=student_id
    student=Students.objects.get(admin=student_id)
    form=EditStudentForm()
    form.fields['email'].initial=student.admin.email
    form.fields['first_name'].initial=student.admin.first_name
    form.fields['last_name'].initial=student.admin.last_name
    form.fields['username'].initial=student.admin.username
    form.fields['address'].initial=student.address
    form.fields['course'].initial=student.course_id.id
    form.fields['gender'].initial=student.gender
    form.fields['session_year_id'].initial=student.session_year_id.id
    return render(request,"hod_template/edit_student_template.html",{"form":form,"id":student_id,"username":student.admin.username})

def edit_student_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        student_id=request.session.get("student_id")
        if student_id==None:
            return HttpResponseRedirect(reverse("manage_student"))

        form=EditStudentForm(request.POST,request.FILES)
        if form.is_valid():
            first_name=form.cleaned_data["first_name"]
            last_name=form.cleaned_data["last_name"]
            username=form.cleaned_data["username"]
            email=form.cleaned_data["email"]
            address=form.cleaned_data["address"]
            session_year_id=form.cleaned_data["session_year_id"]
            course_id=form.cleaned_data["course"]
            gender=form.cleaned_data["gender"]

            if request.FILES.get('profile_pic',False):
                profile_pic=request.FILES['profile_pic']
                fs=FileSystemStorage()
                filename=fs.save(profile_pic.name,profile_pic)
                profile_pic_url=fs.url(filename)
            else:
                profile_pic_url=None


            try:
                user=CustomUser.objects.get(id=student_id)
                user.first_name=first_name
                user.last_name=last_name
                user.username=username
                user.email=email
                user.save()

                student=Students.objects.get(admin=student_id)
                student.address=address
                session_year=SessionYearModel.object.get(id=session_year_id)
                student.session_year_id=session_year
                student.gender=gender
                course=Courses.objects.get(id=course_id)
                student.course_id=course
                if profile_pic_url!=None:
                    student.profile_pic=profile_pic_url
                student.save()
                del request.session['student_id']
                messages.success(request,"Successfully Edited Student")
                return HttpResponseRedirect(reverse("edit_student",kwargs={"student_id":student_id}))
            except:
                messages.error(request,"Failed to Edit Student")
                return HttpResponseRedirect(reverse("edit_student",kwargs={"student_id":student_id}))
        else:
            form=EditStudentForm(request.POST)
            student.Students.objects.get(admin=student_id)
            return render(request,"hod_template/edit_student_template.html",{"form":form,"id":student_id,"username":student.admin.username})

def edit_subject(request,subject_id):
    subject=Subjects.objects.get(id=subject_id)
    courses=Courses.objects.all()
    teachers=CustomUser.objects.filter(user_type=2)
    return render(request,"hod_template/edit_subject_template.html",{"subject":subject,"teachers":teachers,"courses":courses,"id":subject_id})

def edit_subject_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        subject_id=request.POST.get("subject_id")
        subject_name=request.POST.get("subject_name")
        teacher_id=request.POST.get("teacher")
        course_id=request.POST.get("course")

        try:
            subject=Subjects.objects.get(id=subject_id)
            subject.subject_name=subject_name
            teacher=CustomUser.objects.get(id=teacher_id)
            subject.teacher_id=teacher
            course=Courses.objects.get(id=course_id)
            subject.course_id=course
            subject.save()
            
            messages.success(request,"Successfully Edited Subject")
            return HttpResponseRedirect(reverse("edit_subject",kwargs={"subject_id":subject_id}))
        except:
            messages.error(request,"Failed to Edit Subject")
            return HttpResponseRedirect(reverse("edit_subject",kwargs={"subject_id":subject_id}))


def edit_course(request,course_id):
    course=Courses.objects.get(id=course_id)
    return render(request,"hod_template/edit_course_template.html",{"course":course,"id":course_id})

def edit_course_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        course_id=request.POST.get("course_id")
        course_name=request.POST.get("course")

        try:
            course=Courses.objects.get(id=course_id)
            course.course_name=course_name
            course.save()
            messages.success(request,"Successfully Edited Course")
            return HttpResponseRedirect(reverse("edit_course",kwargs={"course_id":course_id}))
        except:
            messages.error(request,"Failed to Edit Course")
            return HttpResponseRedirect(reverse("edit_course",kwargs={"course_id":course_id}))

def manage_session(request):
    return render(request,"hod_template/manage_session_template.html")

def add_session_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("manage_session"))
    else:
        session_start_year=request.POST.get("session_start")
        session_end_year=request.POST.get("session_end")

        try:
            sessionyear=SessionYearModel(session_start_year=session_start_year,session_end_year=session_end_year)
            sessionyear.save()
            messages.success(request,"Successfully Added Session")
            return HttpResponseRedirect(reverse("manage_session"))
        except:
            messages.error(request,"Failed to Add Session")
            return HttpResponseRedirect(reverse("manage_session"))

@csrf_exempt
def check_email_exist(request):
    email=request.POST.get("email")
    user_obj=CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)

@csrf_exempt
def check_username_exist(request):
    username=request.POST.get("username")
    user_obj=CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)

def teacher_feedback_message(request):
    feedbacks=FeedbackTeachers.objects.all()
    return render(request,"hod_template/teacher_feedback_template.html",{"feedbacks":feedbacks})

@csrf_exempt
def teacher_feedback_message_replied(request):
    feedback_id=request.POST.get("id")
    feedback_message=request.POST.get("message")

    try:
        feedback=FeedbackTeachers.objects.get(id=feedback_id)
        feedback.feedback_reply=feedback_message
        feedback.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")


def student_feedback_message(request):
    feedbacks=FeedbackStudent.objects.all()
    return render(request,"hod_template/student_feedback_template.html",{"feedbacks":feedbacks})

@csrf_exempt
def student_feedback_message_replied(request):
    feedback_id=request.POST.get("id")
    feedback_message=request.POST.get("message")

    try:
        feedback=FeedbackStudent.objects.get(id=feedback_id)
        feedback.feedback_reply=feedback_message
        feedback.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")

def teacher_leave_view(request):
    leaves=LeaveReportTeacher.objects.all()
    return render(request,"hod_template/teacher_leave_view.html",{"leaves":leaves})

def teacher_approve_leave(request,leave_id):
    leave=LeaveReportTeacher.objects.get(id=leave_id)
    leave.leave_status=1
    leave.save()
    return HttpResponseRedirect(reverse("teacher_leave_view"))

def teacher_disapprove_leave(request,leave_id):
    leave=LeaveReportTeacher.objects.get(id=leave_id)
    leave.leave_status=2
    leave.save()
    return HttpResponseRedirect(reverse("teacher_leave_view"))


def student_leave_view(request):
    leaves=LeaveReportStudent.objects.all()
    return render(request,"hod_template/student_leave_view.html",{"leaves":leaves})

def student_approve_leave(request,leave_id):
    leave=LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status=1
    leave.save()
    return HttpResponseRedirect(reverse("student_leave_view"))

def student_disapprove_leave(request,leave_id):
    leave=LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status=2
    leave.save()
    return HttpResponseRedirect(reverse("student_leave_view"))

def admin_view_attendance(request):
    subjects=Subjects.objects.all()
    session_year_id=SessionYearModel.object.all()
    return render(request,"hod_template/admin_view_attendance.html",{"subjects":subjects,"session_year_id":session_year_id})

@csrf_exempt
def admin_get_attendance_dates(request):
    subject=request.POST.get("subject")
    session_year_id=request.POST.get("session_year_id")
    subject_obj=Subjects.objects.get(id=subject)
    session_year_obj=SessionYearModel.object.get(id=session_year_id)
    attendance=Attendance.objects.filter(subject_id=subject_obj,session_year_id=session_year_obj)
    attendance_obj=[]
    for attendance_single in attendance:
        data={"id":attendance_single.id,"attendance_date":str(attendance_single.attendance_date),"session_year_id":attendance_single.session_year_id.id}
        attendance_obj.append(data)

    return JsonResponse(json.dumps(attendance_obj),safe=False)

@csrf_exempt
def admin_get_attendance_student(request):
    attendance_date=request.POST.get("attendance_date")
    attendance=Attendance.objects.get(id=attendance_date)

    attendance_data=AttendanceReport.objects.filter(attendance_id=attendance)
    list_data=[]

    for student in attendance_data:
        data_small={"id":student.student_id.admin.id,"name":student.student_id.admin.first_name+" "+student.student_id.admin.last_name,"status":student.status}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)

def admin_profile(request):
    user=CustomUser.objects.get(id=request.user.id)
    return render(request,"hod_template/admin_profile.html",{"user":user})


def admin_profile_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("admin_profile"))
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        password=request.POST.get("password")
        try:
            customuser=CustomUser.objects.get(id=request.user.id)
            customuser.first_name=first_name
            customuser.last_name=last_name
            if password!=None and password!="":
                customuser.set_password(password)
            customuser.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("admin_profile"))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("admin_profile"))

def admin_add_fee(request):
    courses=Courses.objects.all()
    #courses=Courses.objects.filter(course_id=course_id_id)
    session_years=SessionYearModel.object.all()
    return render(request,"hod_template/admin_add_fee.html",{"courses":courses,"session_years":session_years})

@csrf_exempt
def get_students_admin(request):
    course_id=request.POST.get("course")
    session_year=request.POST.get("session_year")

    course=Courses.objects.get(id=course_id)
    session_model=SessionYearModel.object.get(id=session_year)
    students=Students.objects.filter(course_id=course,session_year_id=session_model) 
    list_data=[]

    for student in students:
        data_small={"id":student.admin.id,"name":student.admin.first_name+" "+student.admin.last_name}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)

def save_student_fee(request):
    if request.method!='POST':
        return HttpResponseRedirect('admin_add_fee')
    student_admin_id=request.POST.get('student_list')
    given_date=request.POST.get('given_date')
    due_date=request.POST.get('due_date')
    fee_amount=request.POST.get('fee_amount')
    course_id=request.POST.get('course')


    student_obj=Students.objects.get(admin=student_admin_id)
    course_obj=Courses.objects.get(id=course_id)

    try:
        check_exist=StudentFee.objects.filter(course_id=course_obj,student_id=student_obj).exists()
        if check_exist:
            fee=StudentFee.objects.get(course_id=course_obj,student_id=student_obj)
            fee.given_date=given_date
            fee.due_date=due_date
            fee.fee_amount=fee_amount
            fee.save()
            messages.success(request, "Successfully Updated Fee")
            return HttpResponseRedirect(reverse("admin_add_fee"))
        else:
            fee=StudentFee(student_id=student_obj,course_id=course_obj,given_date=given_date,due_date=due_date,fee_amount=fee_amount)
            fee.save()
            messages.success(request, "Successfully Added Fee")
            return HttpResponseRedirect(reverse("admin_add_fee"))
    except:
        messages.error(request, "Failed to Add Fee")
        return HttpResponseRedirect(reverse("admin_add_fee"))




        



        
    




    








       