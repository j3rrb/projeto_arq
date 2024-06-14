from django.apps import AppConfig
from os import environ
from django.db.models.signals import post_migrate, pre_init
from django.dispatch import receiver


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"

    def ready(self) -> None:
        from core import observers


@receiver(pre_init)
def check_admin_vars(sender, **kwargs):
    admin_username = environ.get("ADMIN_USERNAME")
    admin_pass = environ.get("ADMIN_PASSWORD")

    if not admin_username or not admin_pass:
        raise Exception(
            "Variáveis de ambiente para admin não estão criadas, utilize o arquivo .env.example para criar um arquivo .env com as variáveis de .env.example"
        )


@receiver(post_migrate)
def create_superuser(sender, **kwargs):
    from django.contrib.auth.models import User

    admin_username = environ.get("ADMIN_USERNAME")
    admin_pass = environ.get("ADMIN_PASSWORD")

    admin_exists = User.objects.filter(username=admin_username).exists()

    if not admin_exists:
        print("Usuário admin não encontrado! Criando...")
        User.objects.create_superuser(username=admin_username, password=admin_pass)
        print("Criado!")


@receiver(post_migrate)
def create_employee_group(sender, **kwargs):
    from django.contrib.auth.models import Group

    group_exists = Group.objects.filter(name="employee").exists()

    if not group_exists:
        print("Criando grupo de funcionários...")
        Group.objects.create(name="employee")
        print("Criado!")
