import re
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core import validators
from django.contrib.auth.models import send_mail
# from django.conf import settings
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from localflavor.br.models import BRCPFField, BRPostalCodeField, BRStateField


class UserManager(BaseUserManager):

    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        if not email:
            raise ValueError(_('The given email must be set'))
        email = self.normalize_email(email)
        user = self.model(
            username=None,
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            is_trusty=False,
            last_login=now,
            date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        user = self._create_user(email, password, True, True, **extra_fields)
        user.is_active = True
        user.save(using=self._db)
        return user


# Change the default User Model beahavier to login with 'email'.
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        _('username'), max_length=15,
        unique=True,
        help_text=_(
            'Required. 15 characteres or fewer. Letters, numbers and @/./+/-/_ characteres'
        ),
        validators=[
            validators.RegexValidator(
                re.compile(r'^[\w.@+-]+$'), _('Enter a valid username.'), _('invalid')
            )
        ],
        blank=True, null=True, default=None
    )
    email = models.EmailField(_('email address'), max_length=255, unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)

    is_staff = models.BooleanField(_('staff status'), default=False, help_text=_(
        'Designates whether the user can log into this admin site')
    )
    is_active = models.BooleanField(_('active'), default=True, help_text=_(
        'Designates whether this user should be treated as active. Unselect this instead of deleting account')
    )
    is_trusty = models.BooleanField(_('trusty'), default=False, help_text=_(
        'Designates whether this user has confirmed his account.')
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    USERNAME_FIELD = 'email'  # Set email as a default login field
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table = 'user'

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])


class Profile(models.Model):
    CIVIL_CHOICES = [
        (0, 'Solteiro (a)'),
        (1, 'Casado (a)'),
        (2, 'Divorciado (a)'),
        (3, 'Viúvo (a)'),
        (4, 'Outro')
    ]
    user = models.OneToOneField(
        User, verbose_name='Usuário', 
        related_name='users', 
        on_delete=models.CASCADE
    )
    cpf = BRCPFField('CPF', max_length=14, default=None)
    rg = models.CharField('RG', max_length=9, default=None)
    birthday = models.DateField('Data de Nascimento', default=None)
    civil_status = models.IntegerField('Estado Civil', choices=CIVIL_CHOICES, default=0)

    def __str__(self):
        return self.user.get_short_name()
    
    class Meta:
        verbose_name='Usuário'
        verbose_name_plural='Usuários'


class Phone(models.Model):
    profile = models.ForeignKey(
        Profile, verbose_name='Usuário', 
        related_name='phone', 
        on_delete=models.CASCADE
    )
    ddi = models.CharField('DDI', max_length=3, null=True, default=None)
    ddd = models.CharField('DDD', max_length=3, null=True, default=None)
    number = models.CharField('Número', max_length=9, null=True, default=None)
    
    def get_number(self):
        return f'{self.ddi}{self.ddd}{self.number}'
    
    class Meta:
        verbose_name = 'Telefone'
        verbose_name_plural = 'Telefones'


class Address(models.Model):
    profile = models.ForeignKey(
        Profile, verbose_name='Usuário', 
        related_name='address',
        on_delete=models.CASCADE
    )
    postalcode = BRPostalCodeField('CEP', max_length=10, null=True, default=None)
    street_name = models.CharField('Endereço', max_length=255, null=True, default=None)
    street_number = models.CharField('Número', max_length=10, null=True, default=None)
    complement = models.CharField('Complemento', max_length=100, null=True, default=None)
    neighborhood = models.CharField('Bairro', max_length=100, null=True, default=None)
    city = models.CharField('Cidade', max_length=100, null=True, default=None)
    state = BRStateField('Estado', max_length=2, null=True, default=None)

    class Meta:
        verbose_name = 'Endereço'
        verbose_name_plural = 'Endereços'


# class PasswordReset(models.Model):
#     key = models.CharField('Chave', max_length=100, unique=True)
#     confirmed = models.BooleanField('Confirmado?', default=False, blank=True)
#
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL, verbose_name='Usuário',
#         related_name='resets',
#         on_delete=models.CASCADE
#     )
#
#     created_at = models.DateTimeField('Criado em', auto_now_add=True)
#     updated_at = models.DateTimeField('Atualizado em', auto_now=True)
#
#     def __str__(self):
#         return '{0} em {1}'.format(self.user, self.created_at)
#
#     class Meta:
#         verbose_name = 'Nova Senha'
#         verbose_name_plural = 'Novas Senhas'
#         ordering = ['-created_at']


# class Documents(models.Model):
#     cpf = BRCPFField('CPF', max_length=11, unique=True, blank=True)
#
#     user = models.OneToOneField(
#         User, verbose_name='Usuário',
#         related_name='cpf',
#         on_delete=models.CASCADE,
#         default=None
#     )
#
#     created_at = models.DateTimeField('Criado em', auto_now_add=True)
#     updated_at = models.DateTimeField('Atualizado em', auto_now=True)
#
#     def __str__(self):
#         return self.cpf
