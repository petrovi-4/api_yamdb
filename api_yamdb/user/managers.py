from django.contrib.auth import models


class UserManager(models.UserManager):
    def create_user(self, email, password=None, last_login=None, **kwargs):
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, last_login=None, **kwargs):
        user = self.model(
            email=email, is_staff=True, is_superuser=True, **kwargs
        )
        user.set_password(password)
        user.save()
        return user
