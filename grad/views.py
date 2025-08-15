# views.py
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.shortcuts import render
from .models import Student

import csv


def student_lookup_page(request):
    return render(request, "student_lookup.html")


def get_student_by_regnum(request, reg_num):
    # Find student or return 404
    print(reg_num)
    student = get_object_or_404(Student, reg_num=reg_num)
    print(student)
    # Prepare response
    data = {
        "name": student.name,
        "reg_counter": student.reg_counter,
        "seat": student.seat,
        "reg_num": student.reg_num,
        "session": student.session,
        "student_category": student.student_category,
    }
    return JsonResponse(data)


def get_all_students(request):
    students = Student.objects.all()
    for student in students:
        data = [
            {
                "reg_num": student.reg_num,
                "name": student.name,
                "day": student.day,
                "stand": student.stand,
                "seat": student.seat,
            }
        ]
    return JsonResponse(data, safe=False)


def upload_students_csv(request):
    if request.method == "POST":
        csv_file = request.FILES.get("file")

        if not csv_file:
            return HttpResponse("No file uploaded", status=400)
        if not csv_file.name.endswith(".csv"):
            return HttpResponse("File is not CSV type", status=400)

        # Decode and read CSV
        decoded_file = csv_file.read().decode("utf-8").splitlines()
        reader = csv.DictReader(decoded_file)

        students_to_create = []
        for row in reader:
            student = Student(
                reg_num=row["REGISTER_NUMBER"].strip(),
                name=row["STUDENT_NAME"].strip(),
                session=row["SESSION"].strip(),
                reg_counter=row["Registration Counter"].strip(),
                seat=row["Seat No"].strip(),
                school_name=row["SCHOOL"].strip(),
            )
            students_to_create.append(student)

        # Bulk insert for efficiency
        Student.objects.bulk_create(students_to_create, ignore_conflicts=True)

        return HttpResponse(
            f"Imported {len(students_to_create)} students successfully."
        )

    return render(request, "upload_csv.html")
