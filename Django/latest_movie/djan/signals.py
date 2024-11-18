# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from djan.models import Movie_Ranking, choice

# @receiver(post_save, sender=Movie_Ranking)
# def create_choices_for_movie(sender, instance, created, **kwargs):
#     if created:  # 인스턴스가 새로 생성된 경우
#         for i in range(1, 6):  # 1, 2, 3,4,5에 대한 choice 인스턴스 생성
#             choice.objects.create(movie=instance, choice_text=str(i))