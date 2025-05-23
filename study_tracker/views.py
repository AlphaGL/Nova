from django.shortcuts import render, get_object_or_404, redirect
from .models import Semester, Course
from .forms import CourseForm
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'study_tracker/index.html')


@login_required(login_url='/users/login')
def calculate_cgpa_for_semester(semester, user):
    courses = Course.objects.filter(semester=semester, user=user)
    total_points = sum(course.credits * float(course.grade.points) for course in courses)
    total_credits = sum(course.credits for course in courses)
    return round(total_points / total_credits, 2) if total_credits > 0 else 0


@login_required(login_url='/users/login')
def semester_detail(request, semester_id):
    semester = get_object_or_404(Semester, id=semester_id)

    # Only courses owned by the current user
    courses = Course.objects.filter(semester=semester, user=request.user)

    cgpa = calculate_cgpa_for_semester(semester, request.user)

    # CGPA chart data for all semesters
    semesters = Semester.objects.all().order_by('year', 'name')
    labels = []
    data = []
    for sem in semesters:
        sem_cgpa = calculate_cgpa_for_semester(sem, request.user)
        labels.append(f"{sem.name} {sem.year}")
        data.append(sem_cgpa)

    context = {
        'semester': semester,
        'courses': courses,
        'cgpa': cgpa,
        'chart_labels': labels,
        'chart_data': data,
        'form': CourseForm(),
    }
    return render(request, 'study_tracker/cgpa.html', context)



@login_required(login_url='/users/login')
def add_course(request, semester_id):
    semester = get_object_or_404(Semester, id=semester_id)
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.semester = semester
            course.user = request.user  # Assign logged-in user
            course.save()
    return redirect('semester-detail', semester_id=semester.id)

@login_required(login_url='/users/login')
def edit_course(request, pk):
    course = get_object_or_404(Course, pk=pk)

    # Make sure only owner can edit
    if course.user != request.user:
        return redirect('semester-detail', semester_id=course.semester.id)

    semester = course.semester

    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('semester-detail', semester_id=semester.id)
    else:
        form = CourseForm(instance=course)

    context = {
        'form': form,
        'course': course,
        'semester': semester,
    }
    return render(request, 'study_tracker/cgpa.html', context)

@login_required(login_url='/users/login')
def delete_course(request, pk):
    course = get_object_or_404(Course, pk=pk)

    # Block delete if not owned by user
    if course.user != request.user:
        return redirect('semester-detail', semester_id=course.semester.id)

    semester_id = course.semester.id
    course.delete()
    return redirect('semester-detail', semester_id=semester_id)
