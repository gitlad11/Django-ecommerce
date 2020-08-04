from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    email = models.EmailField()
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    vkontakte_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)

    AUTH_PROFILE_MODULE = 'app.UserProfile'

    @property
    def full_name(self):
        return '%s %s' % (self.first_name , self.last_name)

    def __str__(self):
        return (f'{self.first_name} {self.last_name}')
    
    def create_profile(sender, instance, created, *args, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)
            print('profile has been created!')
    
        
    post_save.connect(create_profile, sender=User)

    #def update_profile(sender, instance, created , **kwargs):
        #if created == False:
            #instance.userprofile.save()
            #print('profile has been updated!')

    #post_save.connect(update_profile, sender=User)


#class UserManager(BaseUserManager):

    #def create_user(self, email, name, password=None):
        #if not email:
            #raise ValueError('email is required!')
       # user = self.model(email=email, name=name)
       # user.set_password(password)
       # user.save(using=self._db)
      #  return user

   # def createsuperuser(self, email, name, password):
 #       user = self.create_user(email, name , password)
    #    user.is_staff = True
     #   user.save(using=self._db)
     #   return user

  #  def get_by_natural_key(self, email_):
       # return self.get(code_number=email_)

#class User(AbstractBaseUser):
   # id = models.IntegerField(primary_key=True, unique=True)
   # name = models.CharField(max_length=40)
   # email = models.EmailField(unique=True)
   # password = models.CharField(max_length=30, blank=False)
   # is_staff = models.BooleanField(default=False)
   # is_active = models.BooleanField(default=True)

   # objects = UserManager()

   # USERNAME_FIELD = 'email'
   # REQUIRED_FIELDS = ['password']

   # def __str__(self):
      #  return self.email