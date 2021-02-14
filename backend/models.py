from django.contrib.auth.models import User, Group
from django.db import models


class Profile(User):
    class Meta:
        verbose_name_plural = 'Profile'

    Gender = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    my_password = models.CharField(
        max_length=150, blank=True, verbose_name="Password")
    middle_name = models.CharField(max_length=150, blank=True)
    gender = models.CharField(
        choices=Gender, max_length=255, default="", verbose_name='Gender')
    is_activated = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.get_full_name()}'

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.first_name = self.first_name.upper()
            self.middle_name = self.middle_name.upper()
            self.last_name = self.last_name.upper()
            self.role.name == "Teacher"
            if self.role.name == "Teacher":
                self.status = "NOT YET ASSIGNED"
        super(Profile, self).save(*args, **kwargs)


class Student(Profile):
    class Meta:
        verbose_name_plural = 'Student Profile'
    STATUS = (
        ('Registered', 'Registered'),
        ('Enrolled', 'Enrolled'),
    )
    section = models.ForeignKey(
        'Section', on_delete=models.CASCADE, null=True, blank=True)
    role = models.ForeignKey(
        to=Group, on_delete=models.CASCADE, verbose_name='Role', default=1)
    birth_date = models.DateField(verbose_name='Birthday', blank=True)
    status = models.CharField(
        choices=STATUS, max_length=64, default="Registered")
    strand = models.ForeignKey(
        to='Strand', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'{self.get_full_name()} - {self.strand}'

    def save(self, *args, **kwargs):

        if self.pk is None:
            self.role.name = "Student"
        super(Student, self).save(*args, **kwargs)


class Teacher(Profile):
    class Meta:
        verbose_name_plural = 'Teacher Profile'
    STATUS = (
        ('IS ASSIGNED', 'IS ASSIGNED'),
        ('NOT YET ASSIGNED', 'NOT YET ASSIGNED'),

    )
    role = models.ForeignKey(
        to=Group, on_delete=models.CASCADE, verbose_name='Role', default=2)
    birth_date = models.DateField(verbose_name='Birthday', blank=True)
    status = models.CharField(
        choices=STATUS, max_length=64, default='NOT YET ASSIGNED')

    def __str__(self):
        return f'{self.get_full_name()}'

    def save(self, *args, **kwargs):
        if self.pk is None:
            if self.role.name == "Teacher":
                self.status = "NOT YET ASSIGNED"
        super(Teacher, self).save(*args, **kwargs)


class YearLevel(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Subject(models.Model):
    subject_name = models.CharField(max_length=64)
    subject_code = models.CharField(max_length=64)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def __str__(self):
        return self.subject_name


class Strand(models.Model):
    TRACK_CHOICES = [
        ('Academic', 'Academic'),
        ('Non-academic', 'Non-academic'),
        ('Technical-Vocational-Livelihood', 'Technical-Vocational-Livelihood'),
    ]
    strand_name = models.CharField(max_length=60)
    track = models.CharField(max_length=100, choices=TRACK_CHOICES)

    def __str__(self):
        return self.strand_name


class Section(models.Model):
    section_name = models.CharField(max_length=64)
    year_level = models.ForeignKey(YearLevel, on_delete=models.CASCADE)
    adviser = models.ForeignKey(
        Teacher, on_delete=models.CASCADE, null=True, blank=True)
    strand = models.ForeignKey(Strand, on_delete=models.CASCADE)
    subject = models.ManyToManyField(Subject)

    def __str__(self):
        return f'{self.year_level} - {self.strand} | {self.section_name}'


class Enrollment(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.student} - {self.section}"


class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    section = models.ForeignKey(
        Section, on_delete=models.CASCADE, null=True, blank=True)
    numeric_grade = models.SmallIntegerField(default=0, verbose_name="Grade")

    def __str__(self):
        return f"{self.student} - {self.numeric_grade}"


class AllStudent(Student):
    class Meta:
        proxy = True
