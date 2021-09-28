from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone
from django.db import models
from . import validators

####################
#      MIXINS      #
####################


class ModelActivityTrackingMixin(models.Model):
    """Because classes in Python can inherit from multiple classes,
    we use a mixin here to declare re-usable fields for tracking
    the C and U of the CRUD activities.
    """
    class Meta:
        """Django way of marking a model abstract so that no
        database table is created for it.
        """
        abstract = True

    created_by = models.ForeignKey(
        'User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='+',  # Django way to disable reverse lookup
        help_text='Who created this object.',
    )
    created_date = models.DateTimeField(
        default=timezone.now,
        help_text='When was this object created.',
    )
    updated_by = models.ForeignKey(
        'User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='+',  # Django way to disable reverse lookup 
        help_text='Who updated this object.',
    )
    updated_date = models.DateTimeField(
        default=timezone.now,
        help_text='When was this object updated.',
    )


######################
#      GENERICS      #
######################


class LookupCode(ModelActivityTrackingMixin, AbstractBaseUser):
    """Simplified implementation of lookup codes for storing generic
    codes for various models. Omits functionality to set 
    active/inactive for simplicity.
    
    In particular, used by:
    - Activity model to store activity category
    - ActivityAttendee model to store attendee role
    """
    # PK `id` field is automatically added by Django, but
    # for the sake of verbosity for the challenge, declare
    # it explicitly
    id = models.AutoField(primary_key=True)
    type = models.ForeignKey(
        'LookupCodeType',
        on_delete=models.PROTECT,
        related_name='lookup_codes',
    )
    code = models.CharField(max_length=25)
    description = models.CharField(
        max_length=250,
        null=True,
        blank=True,
    )


class LookupCodeType(ModelActivityTrackingMixin, AbstractBaseUser):
    """Simplified lookup code types for categorising look up codes.
    Omits functionality to set active/inactive for simplicity.
    """
    # PK `id` field is automatically added by Django, but
    # for the sake of verbosity for the challenge, declare
    # it explicitly
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=25)
    description = models.CharField(
        max_length=250,
        null=True,
        blank=True,
    )


######################
#      ACCOUNTS      #
######################


class User(ModelActivityTrackingMixin, AbstractBaseUser):
    """A custom user model to accomodate for the challenge requirements.

    `password` field + hashing and `last_login` field + tracking,
    along with some Django's user-specific functionalities are 
    inherited from AbstractBaseUser.
    """
    # The setting to determine which field is used as the
    # username when when no explicit username field exists
    USERNAME_FIELD = 'email'

    # PK `id` field is automatically added by Django, but
    # for the sake of verbosity for the challenge, declare
    # it explicitly
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(
        max_length=150,
        blank=True,
        null=True,
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
        null=True,
    )
    email = models.EmailField(
        unique=True
    )  # Used as the username, required, unique
    is_super_user = models.BooleanField(
        default=False,
        help_text='Designates whether the user can log into the admin site.',
    )
    is_active = models.BooleanField(
        default=True,
        help_text=(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    # Making an assumption a user will only be linked to 1 school at a time
    school = models.ForeignKey(
        'School',
        on_delete=models.PROTECT,  # Don't allow deletion if users exist
        null=True,  # Allow null for super users
        related_name='users',  # Reverse lookup
    )
    # Making an assumption here that a user will have only 1 account type
    account_type = models.ForeignKey(
        'UserAccountType',
        on_delete=models.PROTECT,  # Don't allow deletion if users exist
        null=True,  # Allow null for super users
        related_name='users',  # Reverse lookup
    )

    # Reference to custom manager, which allows to make database queries
    # by calling:
    #
    # User.objects.desired_database_query_method()
    #
    objects = BaseUserManager()


class UserAccountType(ModelActivityTrackingMixin, models.Model):
    """A model representing user account types, e.g. staff, student,
    volunteer, etc.

    Stored in a separate table for future extendibility.
    """
    # PK `id` field is automatically added by Django, but
    # for the sake of verbosity for the challenge, declare
    # it explicitly
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)  # Required


#####################
#      SCHOOLS      #
#####################


class School(ModelActivityTrackingMixin, models.Model):
    # PK `id` field is automatically added by Django, but
    # for the sake of verbosity for the challenge, declare
    # it explicitly
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)  # Required
    location = models.ForeignKey(
        'Location',
        on_delete=models.PROTECT,
        related_name='+',
    )


#######################
#      LOCATIONS      #
#######################


class States(models.TextChoices):
    """A list of all Australian states and territories.

    For the sake of simplicity, an assumption is made that the
    SimpleSIS operates in Australia only. Normally, the list of
    countries and states would be stored in a separate table.
    """
    NSW = 'NSW'
    QLD = 'QLD'
    SA = 'SA'
    TAS = 'TAS'
    VIC = 'VIC'
    WA = 'WA'
    ACT = 'ACT'
    NT = 'NT'


class Location(ModelActivityTrackingMixin, models.Model):
    """A generic model to store physical addresses and contact
    details of organisations/places. Used by both the School and
    the Venue models.

    For the sake of simplicity, this table omits phones, emails,
    etc.
    """
    # PK `id` field is automatically added by Django, but
    # for the sake of verbosity for the challenge, declare
    # it explicitly
    id = models.AutoField(primary_key=True)
    address_line_1 = models.CharField(max_length=150)
    address_line_2 = models.CharField(max_length=150, null=True, blank=True)
    city = models.CharField(max_length=150)
    # To simplify implementation here, use Django's native validation
    # against a list of choices, i.e. a list of Australian states
    # and territories
    state = models.CharField(
        max_length=3,
        choices=States.choices,
    )
    # Same assumption applies here, we only expect Autralian postcodes,
    # but we validate them to ensure they're real
    postcode = models.CharField(
        max_length=4, validators=[validators.validate_postcode]
    )


########################
#      ACTIVITIES      #
########################


class Activity(ModelActivityTrackingMixin, models.Model):
    """A model representing an event/activity as per the challenge
    requirements.
    """
    # PK `id` field is automatically added by Django, but
    # for the sake of verbosity for the challenge, declare
    # it explicitly
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)  # Required
    description = models.TextField()  # Unlimited length, required
    # Making an assumption here that an activity will never fall
    # under several categories
    category = models.ForeignKey(
        'LookupCode',
        on_delete=models.PROTECT,  # Don't allow deletion if activities exist
        related_name='+',  # Disable reverse lookup
    )
    start_date = models.DateTimeField()  # Required
    location = models.ForeignKey(
        'Location',
        on_delete=models.PROTECT,  # Protect if activities exist
        related_name='+',  # Disable reverse lookup
    )
    distance_from_school = models.IntegerField(default=0)  # In metres


class ActivityAttendee(ModelActivityTrackingMixin, models.Model):
    """A model for keeping track of organisers and attendees of a venue."""
    # PK `id` field is automatically added by Django, but
    # for the sake of verbosity for the challenge, declare
    # it explicitly
    id = models.AutoField(primary_key=True)
    # Using a reference to the User model here instead of an arbitrary
    # model with an assumption that students/parents/volunteers have
    # SimpleSIS user accounts with respecitive access/permissions
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,  # Delete with user
        related_name='+',  # Disable reverse lookup
    )
    user_role = models.ForeignKey(
        'LookupCode',
        on_delete=models.PROTECT,  # Don't allow deletion if attendees exist
        related_name='+',  # Disable reverse lookup
    )
    activity = models.ForeignKey(
        'Activity',
        on_delete=models.CASCADE,  # Delete with activity
        related_name='+',  # Disable reverse lookup
    )
    # Making an assumption here that the checks/confirmations/payments
    # will be handled externally and translated into the approval status.
    # While this could be tracked as a simple boolean field, a datetime
    # is a better choice as not only it allows for the status to be
    # tracked, but also timestamped
    approved_at = models.DateTimeField(null=True)  # null = not approved
    approved_by = models.ForeignKey(
        'User',
        on_delete=models.PROTECT,  # Require manual check
        null=True,
        related_name='+',  # Disable reverse lookup
    )
    # Similarly to tracking approval, use datetime here to record
    # the attendance status and a timestamp. The assumption is made
    # here that the organisers will record attendees on entry with
    # a digital tablet/mobile device
    attended_at = models.DateTimeField(null=True)


####################
#      VENUES      #
####################


class Venue(ModelActivityTrackingMixin, models.Model):
    # PK `id` field is automatically added by Django, but
    # for the sake of verbosity for the challenge, declare
    # it explicitly
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)  # Required
    description = models.TextField(
        null=True, blank=True
    )  # Optional description
    address = models.ForeignKey(
        'Location',
        on_delete=models.PROTECT,
        related_name='+',
    )