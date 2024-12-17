from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from account.managers import CustomUserManager
from account.utils import uzbek_phone_regex

BUSY, NOT_BUSY, LEADER, PROGRAMMER, EMPLOYEE = ('band', 'band emas', 'rahbar', 'dasturchi', 'hodim')
NOT_ACCEPTED, IN_PROCESS, DONE = ('qabul qilinmagan', 'jarayonda', 'bajarildi')


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(BaseModel, AbstractUser):
    STATUS = (
        (BUSY, BUSY),
        (NOT_BUSY, NOT_BUSY),
    )
    ROLE = (
        (LEADER, LEADER),
        (PROGRAMMER, PROGRAMMER),
        (EMPLOYEE, EMPLOYEE),
    )
    profile_image = models.ImageField(upload_to='user/image/')
    phone_number = models.CharField(max_length=15, validators=[uzbek_phone_regex], unique=True)
    status = models.CharField(max_length=15, choices=STATUS)
    role = models.CharField(max_length=15, choices=ROLE)

    username = None
    objects = CustomUserManager()
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.phone_number}'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @classmethod
    def get_user_role_list(cls):
        return [choice[1] for choice in cls.ROLE]

    @classmethod
    def get_user_status_list(cls):
        return [choice[1] for choice in cls.STATUS]

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')


class Problem(BaseModel):
    STATUS = (
        (NOT_ACCEPTED, NOT_ACCEPTED),
        (IN_PROCESS, IN_PROCESS),
        (DONE, DONE),
    )

    comment = models.TextField()
    image = models.ImageField(upload_to='problem/images/', null=True, blank=True)
    status = models.CharField(max_length=25, choices=STATUS, default=NOT_ACCEPTED)
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='problems_employee')
    programmer = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='problems_programmer')
    is_solved = models.BooleanField(default=False)
    programmer_is_solve = models.BooleanField(default=False)
    solve_date = models.DateField(null=True, blank=True)
    solve_time = models.TimeField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    problem_solve_time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.programmer} - {self.comment}'

    class Meta:
        verbose_name = _('problem')
        verbose_name_plural = _('problems')


class KeepBusy(BaseModel):
    programmer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='keepbusy')
    start_time = models.TimeField(auto_now_add=True)
    end_time = models.TimeField(null=True, blank=True)
    comment = models.TextField()
    image = models.ImageField(upload_to='keepbusy/images/', null=True, blank=True)

    def __str__(self):
        return self.programmer.full_name

    class Meta:
        verbose_name = _('keep busy')
        verbose_name_plural = _('keep busy')


class Board(BaseModel):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('board')
        verbose_name_plural = _('boards')


class Task(BaseModel):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='tasks')
    name = models.CharField(max_length=250)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    programmers = models.ManyToManyField(User, related_name='tasks')
    comment = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("task")
        verbose_name_plural = _("tasks")

