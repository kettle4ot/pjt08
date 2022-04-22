# 0422_pjt08_pair programming

## 1. project 생성 / git clone

- 팀장님: 프로젝트 생성 후
- 팀원: git clone
- <u>*50분 진행 / 10분 휴식 패턴*</u>

## 2. 환경 세팅

#### navigator: 김수빈 / driver: 김민정

- 1시 부터
- 평소 하던 프로젝트와 달라서 초반 진행에 혼란을 겪음. 

##### 1. 가상환경 및 패키지 설치

- ```bash
  $ python -m venv venv
  $ source venv/Scripts/activate
  $ pip install -r requirements.txt
  ```

- 가상환경과 패키지 설치 후 속도 저하. 원인이 디스코드인지 아닌지 팀원의 세팅에서도 비교해볼 예정

- README.md 생성: 둘 다 동시에 작성 중이므로 이것은 임시파일입니다.

##### 2. 프로젝트, 앱 생성

- ```bash
  $ django-admin startproject pjt08 .
  $ python manage.py startapp movies
  ```

- 앱 폴더에 압축된 JSON 파일들이 들어간 fixtures 폴더 넣기

- settings.py에서 앱 등록 (movies, django_extensions, rest_framwork)

##### ~~3. JSON 파일 로드~~

- ```bash
  $ python manage.py migrate
  $ python manage.py loaddata actors.json ....
  ```

- ~~이때는 어짜피 fixtures 폴더가 하나라서 namespace 분리를 하지 않았음~~

- ~~model 없이 마이그레이트 해서 에러남~~

##### 3. models.py

- ```python
  from django.db import models
  
  # Create your models here.
  class Actor(models.Model):
      name = models.CharField(max_length=100)
  
  
  class Movie(models.Model):
      actors = models.ManyToManyField(Actor, related_name='movies')
      title = models.CharField(max_length=100)
      overview = models.TextField()
      release_date = models.DateTimeField()
      poster_path = models.TextField()
  
  
  class Review(models.Model):
      movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
      title = models.CharField(max_length=100)
      content = models.TextField()
  ```

- ```bash
  $ python manage.py makemigration
  $ python manage.py migrate
  ```

##### 4. admin.py

- ```python
  from django.contrib import admin
  from .models import Actor, Movie, Review
  
  # Register your models here.
  admin.site.register(Actor)
  admin.site.register(Movie)
  admin.site.register(Review)
  ```

##### 5. JSON 파일 로드

- ```bash
  $ python manage.py loaddata movies/actors.json movies/movies.json movies/reviews.json
  ```

  - 명세서대로 fixtures/movies 폴더까지 생성했다.

##### 6. admin에서 뜨는 지 확인해보기

- ```bash
  $ python manage.py createsuperuser
  ```

- /admin/에서 로그인해서 확인

##### 7. url 분리 잊어버림..지금 합시다.

- pjt08/urls.py url 분리

  - ```python
    from django.contrib import admin
    from django.urls import path, include
    
    urlpatterns = [
        path('admin/', admin.site.urls),
        path('api/v1/', include('movies.urls')),
    ]
    ```

- movies/urls.py 생성 및 작성

  - ```python
    from django.urls import path
    from . import views
    
    
    urlpatterns = [
        
    ]
    ```

## 3. serializers 세팅 (중요! 어렵!)

- 처음엔 파일 분리 안하고 시도했으나 참조 역참조가 헷갈려서 팀장님이 분리를 제안.

##### 1. serializers 분리

- movies/serializers 폴더 생성 후 actor.py, movie.py, review.py 생성

##### 2. serializers/actor.py

- ```python
  from rest_framework import serializers
  from ..models import Actor, Movie
  
  
  class ActorListSerializer(serializers.ModelSerializer):
      class Meta:
          model = Actor
          fields = ('id', 'name',)
  
  
  class ActorSerializer(serializers.ModelSerializer):
      class MovieSerializer(serializers.ModelSerializer):
          class Meta:
              model = Movie
              fields = ('title',)
      movies = MovieSerializer(many=True, read_only=True)
  
      class Meta:
          model = Actor
          fields = '__all__'
  ```

##### 3. serializers/movie.py

- ```python
  from rest_framework import serializers
  from movies.serializeers.review import ReviewListSerializer
  from ..models import Movie, Actor
  
  
  class MovieListSerializer(serializers.ModelSerializer):
  
      class Meta:
          model = Movie
          fields = ('title', 'overview',)
  
  
  class MovieSerializer(serializers.ModelSerializer):
      class ActorSerializer(serializers.ModelSerializer):
          class Meta:
              model = Actor
              fields = ('name',)
  
      actors = ActorSerializer(many=True, read_only=True)
      review_set = ReviewListSerializer(many=True, read_only=True)
  
      class Meta:
          model = Movie
          fields = '__all__'
  ```

- serializers에서 고민하고 있던 부분을 교수님께서 깔꼼하게 설명해주셨다. 처음부터 폴더에 넣어서 파일을 분리하고 mtom, 1ton 관계를 정의.

- 어디가 혼란스러웠는가?: 전체적으로 다,,,, 교재와 실습했던 파일들 다 참고하면서 혼란이 가중되던 차에 내려온 천사같은 설명.

#### navigator: 김민정 / driver: 김수빈

- 2시 부터

- 속도 차이 나는지 비교: 느려졌다!

- 팀원도 환경 세팅

- ```bash
  $ python -m venv venv
  $ source venv/Scripts/activate
  $ pip install -r requirements.txt
  $ python manage.py migrate
  $ python manage.py loaddata movies/actors.json movies/movies.json movies/reviews.json
  ```

##### 4. serializers/review.py

- ```python
  from rest_framework import serializers
  from ..models import Review, Movie
  
  
  class ReviewListSerializer(serializers.ModelSerializer):
  
      class Meta:
          model = Review
          fields = ('title', 'content',)
  
  
  class ReviewSerializer(serializers.ModelSerializer):
      class MovieListSerializer(serializers.ModelSerializer):
  
          class Meta:
              model = Movie
              fields = ('title',)
      movie = MovieListSerializer(read_only=True)
  
      class Meta:
          model = Review
          fields = '__all__'
          # read_only_fields = ('title',)
  ```

  - 혹시나 쓸 일이 있을까 싶어 실습 파일에서 참고한 read_only_fields를 주석으로 남겨둠

## 4. urls, views

- urls.py, views.py 작성 후 Postman으로 점검
- serializers보다 훨씬 수월하게 진행됨. 반복되는 패턴이 있어서 그런 듯.

##### 1. `path('actors/', views.actor_list),`

- views.py

  - ```python
    # 어마무시한 import들
    from django.shortcuts import get_list_or_404, get_object_or_404
    from rest_framework import status
    from rest_framework.decorators import api_view
    from rest_framework.response import Response
    from .models import Actor, Movie, Review
    from .serializeers.actor import ActorListSerializer, ActorSerializer
    from .serializeers.movie import MovieListSerializer, MovieSerializer
    from .serializeers.review import ReviewListSerializer, ReviewSerializer
    
    # Create your views here.
    @api_view(['GET'])
    def actor_list(request):
        actors = get_list_or_404(Actor)
        serializer = ActorListSerializer(actors, many=True)
        return Response(serializer.data)
    ```

##### 2. ` path('actors/<int:actor_pk>/', views.actor_detail),`

- views.py

  - ```python
    @api_view(['GET'])
    def actor_detail(request, actor_pk):
        actor = get_object_or_404(Actor, pk=actor_pk)
        serializer = ActorSerializer(actor)
        return Response(serializer.data)
    ```

    - `get_object_or_404`의 두 번째 인자를 빼먹을 뻔 함

##### 3. `  path('movies/', views.movie_list),`

- views.py

  - ```python
    @api_view(['GET'])
    def movie_list(request):
        movies = get_list_or_404(Movie)
        serializer = MovieListSerializer(movies, many=True)
        return Response(serializer.data)
    ```

##### 4. `  path('movies/<int:movie_pk>/', views.movie_detail),`

- views.py

  - ```python
    @api_view(['GET'])
    def movie_detail(request, movie_pk):
        movie = get_object_or_404(Movie, pk=movie_pk)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)
    ```

##### 5. `  path('reviews/', views.review_list),`

- views.py

  - ```python
    @api_view(['GET'])
    def review_list(request):
        reviews = get_list_or_404(Review)
        serializer = ReviewListSerializer(reviews, many=True)
        return Response(serializer.data)
    ```

##### 6. `path('reviews/<int:review_pk>/', views.review_detail),`

- views.py

  - ```python
    @api_view(['GET', 'PUT', 'DELETE'])
    def review_detail(request, review_pk):
        review = get_object_or_404(Review, pk=review_pk)
    
        if request.method == 'GET':
            serializer = ReviewSerializer(review)
            return Response(serializer.data)
    
        if request.method == 'PUT':
            serializer = ReviewSerializer(review, request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
    
        if request.method == 'DELETE':
            review.delete()
            data = {
                'delete': f'review {review_pk} is deleted.'
            }
            return Response(data, status=status.HTTP_204_NO_CONTENT)
    ```

    - 교재와 같이 상태 코드도 지정

- MovieSerializer을 재정의 해주지 않고 read_only_fields를 써서 **id만 나옴**

  ```python
  class ReviewSerializer(serializers.ModelSerializer):
      
      class Meta:
          model = Review
          fields = '__all__'
          read_only_fields = ('title',)
  ```

  ```python
  class ReviewSerializer(serializers.ModelSerializer):
      class MovieListSerializer(serializers.ModelSerializer):
  
          class Meta:
              model = Movie
              fields = ('title',)
      movie = MovieListSerializer(read_only=True)
      
      class Meta:
          model = Review
          fields = ('id', 'title', 'content',)
          read_only_fields = ('title',)
  ```

  - 원하는 필드만 보이게 inner class로 재정의
  - 여기서는 fields를 전체가 아니게 정의 해버림

  ```python
  class ReviewSerializer(serializers.ModelSerializer):
      class MovieListSerializer(serializers.ModelSerializer):
  
          class Meta:
              model = Movie
              fields = ('title',)
      movie = MovieListSerializer(read_only=True)
  
      class Meta:
          model = Review
          fields = '__all__'
  ```

  시행착오 끝에 성공. `fields = '__all__'`로 변경 후 read_only_fields는 지워버렸다.

  재정의를 하지 않고 read_only_fields로 title만 가져오는 걸 시도해 보았으나 실패. 방법이 있다면? 너무 궁금합니다.

#### navigator: 김수빈 / driver: 김민정

- 3시 부터

##### 7. `path('movies/<int:movie_pk>/reviews/', views.create_review)`

- views.py

  - ```python
    @api_view(['POST'])
    def create_review(request, movie_pk):
        movie = get_object_or_404(Movie, pk=movie_pk)
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(movie=movie)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    ```

## 5. 처음부터 점검

- 페이지 하나씩 다시 띄워서 명세서와 비교

- 완료 후 커밋 메세지 수정 (project beta version -> project completed)

- 커밋 메세지 수정 후 레포지토리에 반영이 되지 않았다. (push 오류)

- merge 후 다시 push => 성공

- README 다 쓰고 원인 파악해보기!

  

- `git commit --amend`

  - **<u>커밋 수정 전 이미 해당 커밋을 push한 경우</u>** 수정 후에 error 발생한다고 한다.

  - `git push --force` or `git push -f` 옵션으로 푸시가 가능

    - > "Don't do it."  from stackoverflow

- `git push -f (이하 생략)`   는 위험할까봐 merge 후 재 push

- 그렇다면 `git reset --soft`를 사용했어야? 하나? 아마도,,

## 6. 소감

페어님 덕에 진행이 잘 된 것 같다. 혼자였으면 토요일까지 진행했을 것이다.

##### 긴급,,오타 발견

​	serializer 폴더명을 serializeer로 지정했었다. vscode에서 폴더명을 바꾸려는데 계속 에러 뜸 => 그냥 윈도우상에서 폴더명 변경도 시도했으나 어디서 파일이 열려있다고 거절당했다. *왜..? 어디서?*

​	그냥 폴더를 새로 만들어서 이동시킴

이번엔느 저번보다 훨씬 수월했으나 종종 찾아오는 위기와 이상한데 꽂힌 호기심으로 인해 시간을 좀 썼다. 저의 방향을 끌어주신 팀장님께 감사드린다.