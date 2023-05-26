from mainapp.models import AppConfig


def get_instance_mail_settings(instance_name):
    app_config = AppConfig.objects.filter(app="main").first()
    email = None
    email_config = None
    if app_config is None:
        return {
            'email': email,
            'email_config': email_config
        }
    else:
        email = getattr(app_config, f'{instance_name}_email', None)
        email_config = getattr(app_config, f'{instance_name}_emailconfig', None)
    return {
        'email': email,
        'email_config': email_config,
    }
