# 관리자 페이지의 설정에 대한 부분입니다.

from django.contrib import admin
from .models import *

# 관리자 페이지 choice를 세로로 출력하는 메서드
# class choiceInline(admin.TabularInline):
#     model = choice

# 관리자 페이지 Question 들어가면 나오는 항목의 레이아웃, 구성에 대한 부분
# class QuestionAdmin(admin.ModelAdmin):
#     search_fields = ['subject']
#     fieldsets = [
#         ('영화', {'fields': ['subject']}),
#         ('영화시간', {'fields': ['game_date'], 'classes': ['collapse']}),        
#     ]
#     # 관리자 페이지 Question 내부 리스트의 열구성
#     # 열이름은 model에서 verbose_name으로 정함
#     list_display=('subject','game_date','was_published_recently')
#     # game_date는 읽기 전용으로 만듦
#     #readonly_fields = ['game_date']
#     inlines = [choiceInline]
#     # 관리자 페이지 Question 내부 필터구성
#     list_filter = ['game_date']
#     # 관리자 페이지 Question 내부 검색창
#     search_fields = ['subject']


#관리자만 질문,답변을 등록할수 있게함, 제목검색기능
# admin.site.register(Question,QuestionAdmin)