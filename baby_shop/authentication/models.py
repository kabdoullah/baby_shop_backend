from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, email, first_name, last_name, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('Le phone_number est obligatoire.')
        phone_number = self.normalize(phone_number)
        user = self.model(phone_number=phone_number, email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        # Par défaut, un superutilisateur n'est pas un vendeur
        extra_fields.setdefault('is_vendeur', False)
        return self.create_user(phone_number, email, first_name, last_name, password, **extra_fields)

class CustomUser(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=20, unique=True)
    is_active = models.BooleanField(default=True)
    is_seller = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone_number'

    objects = CustomUserManager()
    
    
    

class Seller(models.Model):
    # OneToOne relationship with the CustomUser model to associate each seller with a user
    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE, related_name='seller')
    boutique_name = models.CharField(max_length=100)  # Nom de la boutique du vendeur
    boutique_description = models.TextField(blank=True, null=True)  # Description de la boutique (optionnelle)
    boutique_address = models.CharField(max_length=255)  # Adresse de la boutique
    phone_number = models.CharField(max_length=15)  # Champ pour stocker le numéro de téléphone du vendeur

    def __str__(self):
        return self.boutique_name

