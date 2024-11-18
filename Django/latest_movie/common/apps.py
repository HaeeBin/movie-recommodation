from django.apps import AppConfig

# Common 애플리케이션의 설정을 관리
class CommonConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'common'
