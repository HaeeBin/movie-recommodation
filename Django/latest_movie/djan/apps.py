from django.apps import AppConfig

class djanConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    # 다른 프로젝트와 헷갈리지 않게 이름 지정
    name = 'djan'

