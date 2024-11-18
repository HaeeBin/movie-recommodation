from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, redirect,render
from django.utils import timezone
from datetime import datetime as dt
from django.conf import settings
from urllib.parse import quote
from .models import *
import boto3
import io
#페이징으로 페이지에 보이는 영화 갯수를 제한
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.urls import reverse
from PIL import Image
from django.db.models import F,Q
# from django.http import HttpResponseNotAllowed
from .forms import *
from django.contrib.auth.decorators import login_required

# 메인 영화페이지
def main(request,movie_code=None):
    movie_list = movie_all.objects.order_by('rank')
    # S3 이미지 URL 설정
    trend_url1 = f'https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/naver/naver_trend/trends_group_1.png'
    trend_url2 = f'https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/naver/naver_trend/trends_group_2.png'
    
    # 템플릿에 URL 전달
    context = {'movie_list': movie_list,'movie_code':movie_code,'trend_url1': trend_url1,'trend_url2': trend_url2}
    return render(request, 'djan/main.html', context)

def ranking(request):
    # 감독별 랭킹 데이터 쿼리
    director_ranking = movie_all.objects.order_by('rank')

    # 배우별 랭킹 데이터 쿼리
    actor_ranking = movie_all.objects.order_by('rank')
    trusted_directors=trusted_director.objects.order_by('-average_audience')
    trusted_actors=trusted_actor.objects.order_by('-avg_audience')
    # 템플릿에 데이터 전달
    context = {
        'director_ranking': director_ranking,
        'actor_ranking': actor_ranking,
        'trusted_directors' : trusted_directors,
        'trusted_actors' : trusted_actors
    }
    return render(request, 'djan/ranking.html', context)

# 모든영화페이지
# 뷰가 호출될 때 URL 매개변수로 movie_code가 제공되지 않으면 movie_code가 None으로 설정됩
def search(request, movie_code=None):
    # 페이지
    # GET 요청의 매개변수 중 'page'라는 이름의 값을 가져옵니다. 
    # 만약 'page' 매개변수가 요청에 없다면 기본값으로 '1'을 사용
    page = request.GET.get('page', '1')
    # GET 요청의 매개변수 중 'kw'라는 이름의 값을 가져옵니다.
    # 만약 검색 요청시 get에 kw가 포함됨
    # 만약 'kw' 매개변수가 요청에 없다면 기본값으로 ''을 사용
    kw = request.GET.get('kw', '')

    # (변경) 전체 영화 모델로 대체해야함
    movie_list = movie_all.objects.all()
    if kw:
        movie_list = movie_list.filter(
            Q(korean_name__icontains=kw) # 제목 검색
        ).distinct()

    # 페이지당 10개씩 보여주기
    paginator = Paginator(movie_list, 10)
    # 현재 페이지의 movie_all 객체들을 page_obj 변수에 저장
    page_obj = paginator.get_page(page)
    # 현재 페이지에 해당하는 movie_all 객체들을 'movie_list'라는 변수로 
    # 템플릿에 전달
    context = {'movie_list': page_obj, 'page' : page, 'kw':kw, 'movie_code':movie_code}
    return render(request, 'djan/search.html', context)

# 상세 영화페이지
def detail(request, movie_code=None):
    # primary key 각 객체를 유일하게 식별하는 주요 식별자입니다.
    # movie_all 모델은 일반적으로 각 질문마다 고유한 pk를 가지고 있습니다. 
    # 사용자가 특정 질문에 접근(get)하려고 할 때, 해당 질문의 pk 값을 URL에서
    # 가져오게 됩니다.
    movie = get_object_or_404(movie_all, pk=movie_code)
    info = movie_info.objects.filter(movie=movie).first()
    rating = None
    average_rate = None
    current_date = timezone.now().date()

    image_url = s3_to_wordcloud(movie_code)
      
    if request.user.is_authenticated:
        rating = movie_rating.objects.filter(movie=movie, user=request.user).first()
        average_rate = average_rating(movie)
    
    #날짜 변환
    open_date = dt.strptime(movie.open_date, '%Y-%m-%d').date()

    allow_vote = open_date <= current_date

    context = {'movie': movie, 'info':info, 'rating': rating, 'movie_code':movie_code, 'average_rate': average_rate, 'allow_vote' : allow_vote, 'image_url': image_url}

    return render(request, 'djan/detail.html', context)

# 댓글 작성할때 로그인 필요
@login_required(login_url='common:login')
# 댓글 작성 (redirect해서 detail로 다시 이동)
# movie_code는 URL 매핑에 의해 그 값이 전달된다. create/2/ 라는 페이지를
# 요청하면 매개변수 movie_code에는 2라는 값이 전달된다.
def answer_create(request, movie_code):
    # 우선 어떤 질문에 달린 댓글인지 알아야함
    movie = get_object_or_404(movie_all, pk=movie_code)
    # 댓글 등록(post)시
    if request.method == "POST":
        # POST 메서드로 전송된 데이터를 이용하여 answerForm 인스턴스를 생성
        form = answerForm(request.POST)
        if form.is_valid():
            # 임시 저장하여 answer 객체를 리턴받는다.
            answer = form.save(commit=False)
            # 작성자(author) 속성에 로그인 계정 저장
            answer.author = request.user
            # 실제 저장을 위해 작성일시를 설정한다.
            answer.answer_date = timezone.now()
            # 해당 질문도 저장
            answer.movie = movie
            answer.save()
            # 데이터베이스 저장후 다시 상세 페이지로 돌아감
            return redirect('djan:detail', movie_code=movie_code)
    #  답변 등록은 POST 방식만 사용되기 때문에 다른방식(GET)은 안됨
    else:
        form = answerForm()
    context = {'movie': movie, 'form': form, 'movie_code':movie_code}
    return render(request, 'djan/detail.html', context)

# 투표(완료시 결과페이지(result)로 이동)

def vote(request, movie_code=None):

    # 로그인하지 않은 사용자는 로그인 페이지로 리다이렉트
    if not request.user.is_authenticated:
        return redirect('common:login')
    
    # 우선 어떤 질문에 달린 투표인지 알아야함
    movie = get_object_or_404(movie_all, pk=movie_code)
    info = movie_info.objects.filter(movie=movie).first()

    user_rating, created = movie_rating.objects.get_or_create(movie=movie, user=request.user)

    if not created:
        average_rate = average_rating(movie)
        return render(request, 'djan/detail.html', {'movie': movie, 'error_message': "이미 투표한 사용자입니다.", 'average_rate': average_rate})

    # 데이터베이스에서 사용자가 해당 질문에 이미 투표했는지 확인
    # 투표했으면 이미 투표했다는 문구 출력

    choice_id = request.POST.get('choice')

    if choice_id is None:
        return render(request, 'djan/detail.html', {'movie': movie, 'error_message': '선택이 없습니다.'})
    try:
        selected_choice = movie.choice_set.get(pk=choice_id)
    #선택 안한경우 처리
    except (KeyError, choice.DoesNotExist):
        return render(request, 'djan/detail.html', {'movie': movie, 'error_message': f"선택이 없습니다. id={request.POST['choice']}"})

    # F는 데이터베이스에서 현재 값을 가져와 필드 값을 업데이트하므로 다른 사용자가
    # 변경한 값을 덮어씌우지 않는다.
    selected_choice.votes = F('votes') + 1
    # 현재 로그인한 사용자를 저장
    selected_choice.user = request.user  
    selected_choice.save()
    
    # 사용자의 투표 항목 업데이트
    user_rating.choice = selected_choice
    user_rating.save()

    # user_info모델에도 투표 내용 저장
    user_info.objects.create(movie=movie, user=request.user, choice=selected_choice)
    average_rate = average_rating(movie)

    return render(request, 'djan/detail.html', {'movie': movie, 'error_message': "투표 완료", 'rating':user_rating, 'info':info, 'average_rate': average_rate})

def average_rating(movie):
    total_vote = 0
    total_rating = 0

    # movie의 choices에서 각 choice에 대한 정보를 가져옴
    for choice in movie.choice_set.all():
        # 각 choice의 투표수와 선택지 별점을 가져옴
        n = choice.votes
        rating = int(choice.choice_text)

        total_vote += n
        total_rating += n * rating

    if total_vote == 0:
        return 0
    
    average_rate = total_rating / total_vote
    return average_rate

    
def s3_to_wordcloud(movie_code=None):
    image_key = f'wordcloud/image/{movie_code}.png'
    image_url = f'https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{image_key}'
    image = None
    try:
        # S3 클라이언트 생성
        s3 = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )

        # 이미지 데이터 가져오기
        response = s3.get_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=image_key)
        image_data = response['Body'].read()

        # 이미지 열기
        image = Image.open(io.BytesIO(image_data))
        print("Image loaded successfully from S3")

    except Exception as e:
        print(f"Error loading image from S3: {e}")

    if image :
        return image_url
    else:
        return None

# def trend_image(request):
#     # S3 이미지 URL 설정
#     trend_url1 = f'https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/naver/naver_trend/trends_group_1.png'
#     trend_url2 = f'https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/naver/naver_trend/trends_group_2.png'
    
#     # 템플릿에 URL 전달
#     context = {'trend_url1': trend_url1,'trend_url2': trend_url2}
#     return render(request, 'main.html', context)

   
