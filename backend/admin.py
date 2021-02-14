from django.contrib import admin
from django.db.models import Q
from .models import *
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
import uuid
from django.contrib.auth.models import User, Group


class StudentGradeInline(admin.TabularInline):
    verbose_name = 'STUDENT GRADE'
    verbose_name_plural = 'STUDENT GRADES'
    model = Grade
    fields = ('get_student_section', 'get_student_subject',
              'get_numeric_grade',)
    extra = 0
    readonly_fields = (
        'get_student_section', 'get_student_subject', 'get_numeric_grade')

    def get_numeric_grade(self, obj=Grade):
        if obj.numeric_grade == 0:
            return "Not Yet Set"
        return obj.numeric_grade
    get_numeric_grade.short_description = "Grade"

    def get_student_section(self, obj=Grade):
        return obj.section
    get_student_section.short_description = "Section"

    def get_student_subject(self, obj=Grade):
        return obj.subject
    get_student_subject.short_description = "Subject"

    def has_delete_permission(self, request, obj=None):
        False

    def has_add_permission(self, request, obj):
        False


@admin.register(AllStudent)
class AllStudentAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_filter = ['gender']
    search_fields = ['username', 'first_name',
                     'last_name', 'middle_name']
    readonly_fields = ('get_name', 'get_gender', 'get_section')
    inlines = (StudentGradeInline,)

    def get_list_display(self, request, obj=None):
        user = request.user
        if user.is_superuser:
            return ('get_name', 'get_gender', 'get_section')
        return ('get_name', 'get_gender')

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(AllStudentAdmin, self).get_fields(request, obj)
        return (
            ('Profile Details', {
                'fields': ('first_name', 'last_name', 'middle_name', 'gender', 'birth_date', 'email',)
            }),
        )

    def get_queryset(self, request):
        user = request.user
        teacher = None
        students_enrolled = {}
        try:
            teacher = Teacher.objects.get(pk=user)
        except Teacher.DoesNotExist:
            return Student.objects.filter(role__name="Student")
        sec = Section.objects.get(adviser=teacher)
        return Student.objects.filter(section=sec)

    def get_section(self, obj):
        if obj.section is None:
            return "Not Yet Enrolled"
        return obj.section
    get_section.short_description = "Section"

    def get_name(self, obj):
        if obj is None:
            return ""
        return obj.get_full_name()
    get_name.short_description = "Full Name"

    def get_gender(self, obj):
        if obj is None:
            return ""
        return obj.gender
    get_gender.short_description = "Gender"

    def has_change_permission(self, request, obj=None):
        False

    def has_add_permission(self, request, obj=None):
        False

    def has_delete_permission(self, request, obj=None):
        False


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'username', 'get_status', 'is_activated')
    list_per_page = 10
    list_filter = ('status',)
    search_fields = ['username', 'first_name',
                     'last_name', 'middle_name', ]

    def save_model(self, request, obj, form, change):
        def codeGenerator():
            ramdom = uuid.uuid4().hex[:5].lower()
            finalramdom = str(obj.username) + str(ramdom)
            return finalramdom

        if not change:
            raw_pass = codeGenerator()
            obj.my_password = raw_pass
            hashed_password = make_password(raw_pass)
            obj.password = hashed_password
            super(TeacherAdmin, self).save_model(
                request, obj, form, change)
        else:
            if obj.is_activated:
                teacher = Teacher.objects.get(pk=obj.pk)
                obj.is_staff = True
                try:
                    group = Group.objects.get(name='Teacher')
                    teacher.groups.add(group)
                except Group.DoesNotExist:
                    pass
                teacher.save()
            else:
                obj.is_staff = False
            super(TeacherAdmin, self).save_model(
                request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('my_password',)
        return ('get_status', 'get_name')

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(TeacherAdmin, self).get_fields(request, obj)
        if obj is None:
            return (
                ('Profile Details', {
                    'fields': ('username', 'first_name', 'last_name', 'middle_name', 'gender', 'birth_date', 'email',
                               )
                }),
            )
        return (
            ('Profile Details', {
                'fields': ('username', 'my_password', 'first_name', 'last_name', 'middle_name', 'gender', 'birth_date', 'email', 'is_activated'
                           )
            }),
        )

    def get_status(self, obj):
        if obj is None:
            return ""
        return obj.status
    get_status.short_description = "Status"

    def get_name(self, obj):
        if obj is None:
            return ""
        return obj.get_full_name()
    get_name.short_description = "Full Name"


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'username', 'get_status',
                    'get_section', 'is_activated')
    list_per_page = 10
    list_filter = ('status',)
    search_fields = ['username', 'first_name',
                     'last_name', 'middle_name']

    def save_model(self, request, obj, form, change):
        def codeGenerator():
            ramdom = uuid.uuid4().hex[:5].lower()
            finalramdom = str(obj.username) + str(ramdom)
            return finalramdom

        if not change:
            raw_pass = codeGenerator()
            obj.my_password = raw_pass
            hashed_password = make_password(raw_pass)
            obj.password = hashed_password
            super(StudentAdmin, self).save_model(
                request, obj, form, change)
        else:
            if obj.is_activated:
                student = Student.objects.get(pk=obj.pk)
                obj.is_staff = True
                try:
                    group = Group.objects.get(name='Student')
                    student.groups.add(group)
                except Group.DoesNotExist:
                    pass
                student.save()
            else:
                obj.is_staff = False
            super(StudentAdmin, self).save_model(
                request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('my_password', 'get_section')
        return ('get_status', 'get_name', 'get_section')

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(StudentAdmin, self).get_fields(request, obj)
        if obj is None:
            return (
                ('Student Profile Details', {
                    'fields': ('username', 'first_name', 'last_name', 'middle_name', 'gender', 'birth_date', 'email', 'strand',
                               )
                }),
            )
        return (
            ('Student Profile Details', {
                'fields': ('username', 'my_password', 'first_name', 'last_name', 'middle_name', 'gender', 'birth_date', 'email', 'strand', 'get_section', 'is_activated'
                           )
            }),
        )

    def get_section(self, obj):
        if obj.section is None:
            return "Not Yet Enrolled"
        return obj.section
    get_section.short_description = "Section"

    def get_status(self, obj):
        if obj is None:
            return ""
        return obj.status
    get_status.short_description = "Status"

    def get_name(self, obj):
        if obj is None:
            return ""
        return obj.get_full_name()
    get_name.short_description = "Full Name"


@admin.register(YearLevel)
class GradeLevelAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_per_page = 10
    ordering = ('name',)

    fieldsets = [
        ('Details', {'fields': [
            'name']})
    ]


@admin.register(Strand)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('strand_name', 'track')
    list_filter = ['track']
    list_per_page = 10
    fieldsets = [
        ('Strand Details', {'fields': ['strand_name', 'track']})
    ]


class EnrollmentInline(admin.TabularInline):
    verbose_name = 'STUDENT ENROLLED'
    verbose_name_plural = 'STUDENTS ENROLLED'
    model = Enrollment
    fields = ('get_student_name', 'get_student_gender')
    extra = 0
    readonly_fields = ('get_student_name', 'get_student_gender',)

    def get_student_name(self, obj):
        return obj.student.get_full_name()
    get_student_name.short_description = "Student Name"

    def get_student_gender(self, obj):
        return obj.student.gender
    get_student_gender.short_description = "Gender"

    def has_delete_permission(self, request, obj=None):
        False

    def has_change_permission(self, request, obj=None):
        False

    def has_add_permission(self, request, obj):
        False


class GradeInline(admin.TabularInline):
    verbose_name = 'STUDENT'
    verbose_name_plural = 'STUDENTS'
    model = Grade
    fields = ('get_student_name', 'get_student_gender',
              'numeric_grade', 'get_student_section')
    extra = 0
    readonly_fields = ('get_student_name',
                       'get_student_gender', 'get_student_section', 'get_numeric_grade')

    def get_numeric_grade(self, obj=Grade):
        if obj.numeric_grade == 0:
            return "Not Yet Set"
        return obj.numeric_grade
    get_numeric_grade.short_description = "Grade"

    def get_student_name(self, obj=Grade):
        return obj.student.get_full_name()
    get_student_name.short_description = "Student Name"

    def get_student_gender(self, obj=Grade):
        return obj.student.gender
    get_student_gender.short_description = "Gender"

    def get_student_section(self, obj=Grade):
        return obj.section
    get_student_section.short_description = "Section"

    def has_delete_permission(self, request, obj=None):
        False

    def has_add_permission(self, request, obj):
        False


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    fields = ['subject_name', 'subject_code', 'teacher']

    inlines = (GradeInline,)

    def get_list_display(self, request, obj=None):
        user = request.user
        try:
            teacher = Teacher.objects.get(pk=user)
        except Teacher.DoesNotExist:
            return('subject_name', 'subject_code', 'teacher')
        if teacher:
            return('subject_name', 'subject_code')
        return('student', 'subject', 'get_numeric_grade')

    def get_queryset(self, request):
        user = request.user
        teacher = None
        try:
            teacher = Teacher.objects.get(pk=user)
        except Teacher.DoesNotExist:
            return Subject.objects.all()
        return Subject.objects.filter(teacher=teacher)

    def get_readonly_fields(self, request, obj=None):
        user = request.user
        try:
            teacher = Teacher.objects.get(pk=user)
        except Teacher.DoesNotExist:
            return ('get_numeric_grade')
        if teacher:
            return ('subject_name', 'subject_code', 'teacher', 'get_numeric_grade')
        return ('get_numeric_grade')

    def get_numeric_grade(self, obj=Grade):
        if obj.numeric_grade == 0:
            return "Not Yet Set"
        return obj.numeric_grade
    get_numeric_grade.short_description = "Grade"


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('section_name', 'year_level', 'strand', 'adviser')
    list_filter = ['year_level']
    search_fields = ['section_name', 'adviser__middle_name',
                     'adviser__first_name', 'adviser__last_name']
    inlines = (StudentGradeInline,)
    fieldsets = [
        ('Section details', {'fields': [
            'section_name', 'year_level', 'strand', 'adviser']}),
        ('Subject details', {'fields': ['subject']}),
    ]

    def get_queryset(self, request):
        user = request.user
        teacher = None
        try:
            teacher = Teacher.objects.get(pk=user)
        except Teacher.DoesNotExist:
            return Section.objects.all()
        return Section.objects.filter(adviser=teacher)

    def get_readonly_fields(self, request, obj=None):

        if obj:
            return ('section_name', 'year_level', 'strand', 'adviser')
        return ()

    def get_inlines(self, request, obj):
        if obj:
            return (EnrollmentInline,)
        return []

    def save_model(self, request, obj, form, change):
        if not change:
            if obj.adviser.pk is None:
                super(SectionAdmin, self).save_model(
                    request, obj, form, change)
            adviser = Teacher.objects.get(pk=obj.adviser.pk)
            adviser.status = 'IS ASSIGNED'
            adviser.save()
            super(SectionAdmin, self).save_model(request, obj, form, change)

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        if obj is None:
            context['adminform'].form.fields['adviser'].queryset = Teacher.objects.filter(
                Q(role__name__contains='Teacher') &
                Q(status="NOT YET ASSIGNED")
            )
        return super(SectionAdmin, self).render_change_form(request, context, add, change, form_url, obj)


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('section', 'student',)
    list_filter = ('section',)
    search_fields = ['section__section_name']
    fieldsets = [
        ('Details', {'fields': ['section', 'student', ]}),

    ]

    def get_list_filter(self, request, obj=None):
        user = request.user
        if user.is_superuser:
            return ('section',)
        try:
            student = Student.objects.get(pk=user)
        except Student.DoesNotExist:
            return ('section',)
        if student:
            return ()
        if obj:
            return ('section',)
        return ('section',)

    def get_section_adviser(self, obj=Enrollment):
        return obj.section.adviser
    get_section_adviser.short_description = "Adviser"

    def get_all_subjects(self, obj=Enrollment):
        return (', '.join([str(o) for o in obj.section.subject.all()]))
    get_all_subjects.short_description = "All Subject"

    def get_fieldsets(self, request, obj=None):
        user = request.user
        fieldsets = super(EnrollmentAdmin, self).get_fields(request, obj)
        if obj is None:
            return (
                ('Profile Details', {
                    'fields': ('section', 'student',
                               )
                }),
            )

        try:
            student = Enrollment.objects.filter(student__pk=user)
        except Enrollment.DoesNotExist:
            return Enrollment.objects.all()
        if student:
            return (
                ('Details', {
                    'fields': ('section', 'student', 'get_section_adviser', 'get_all_subjects'
                               )
                }),
            )
        return (
            ('Details', {
                'fields': ('section', 'student',
                           )
            }),
        )

    def get_queryset(self, request):
        user = request.user
        teacher = None
        if user.is_superuser:
            return Enrollment.objects.all()
        try:
            student = Enrollment.objects.filter(student__pk=user)
            students = Enrollment.objects.filter(student__pk=user).count()
        except Enrollment.DoesNotExist:
            return Enrollment.objects.all()
        if students == 0:
            return Enrollment.objects.none()
        if student:
            return student
        try:
            teacher = Teacher.objects.get(pk=user)
        except Teacher.DoesNotExist:
            return Enrollment.objects.all()
        if teacher:
            return Enrollment.objects.filter(section__adviser=teacher)

    def get_readonly_fields(self, request, obj=None):
        user = request.user
        try:
            student = Student.objects.get(pk=user)
        except Student.DoesNotExist:
            return ()
        if student:
            return ('section', 'get_section_adviser', 'get_all_subjects')
        if obj:
            return ('section', 'student',)
        return ()

    def save_model(self, request, obj, form, change):
        if not change:
            if obj.student.pk is None:
                super(EnrollmentAdmin, self).save_model(
                    request, obj, form, change)
            student = Student.objects.get(pk=obj.student.pk)
            section = Section.objects.get(pk=obj.section.pk)
            student.status = 'Enrolled'
            student.section = section
            student.save()
            for subj in section.subject.all():
                Grade.objects.create(
                    student=obj.student,
                    subject=subj,
                    section=section
                )
            super(EnrollmentAdmin, self).save_model(request, obj, form, change)

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        if obj is None:
            context['adminform'].form.fields['student'].queryset = Student.objects.filter(
                Q(role__name__contains='Student') & Q(status='Registered'))
        return super(EnrollmentAdmin, self).render_change_form(request, context, add, change, form_url, obj)


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    search_fields = ['section__section_name']
    fieldsets = [
        ('Details', {'fields': ['student', 'subject',
                                'teacher_name', 'get_numeric_grade']}),
    ]
    readonly_fields = ('teacher_name',)

    def get_numeric_grade(self, obj=Grade):
        if obj.numeric_grade == 0:
            return "Not Yet Set"
        return obj.numeric_grade
    get_numeric_grade.short_description = "Grade"

    def teacher_name(self, obj):
        return obj.subject.teacher
    teacher_name.short_description = "Teacher"

    def has_change_permission(self, request, obj=None):
        False

    def get_list_display(self, request, obj=None):
        user = request.user
        try:
            student = Student.objects.get(pk=user)
        except Student.DoesNotExist:
            return('student', 'subject', 'get_numeric_grade')
        if student:
            return('subject', 'teacher_name', 'get_numeric_grade', )
        return('student', 'subject', 'get_numeric_grade')

    def get_list_filter(self, request, obj=None):
        user = request.user
        if obj:
            return ('section',)
        try:
            student = Student.objects.get(pk=user)
        except Student.DoesNotExist:
            return ()
        try:
            teacher = Teacher.objects.get(pk=user)
        except Teacher.DoesNotExist:
            return ()
        if student:
            return ()
        if teacher:
            return ()
        return ('section',)

    def get_queryset(self, request):
        user = request.user
        teacher = None
        try:
            teacher = Teacher.objects.get(pk=user)
        except Teacher.DoesNotExist:
            try:
                student = Student.objects.get(pk=user)
            except Student.DoesNotExist:
                return Grade.objects.all()
            if student:
                return Grade.objects.filter(student=student)

        if teacher:
            try:
                section = Section.objects.get(adviser=teacher)
            except Section.DoesNotExist:
                return Grade.objects.all()
            return Grade.objects.filter(section=section)


admin.site.headers = 'BCCT School Admin'

# # TODO: Customize admin page
