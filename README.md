# PJT08 (04/22)

> DB 설계를 활용한 REST API 설계

[TOC]



## 역할 나누기

* 페어 프로그래밍
  * 역할 교체 :  <u>*50분 진행 / 10분 휴식 패턴*</u>


  * | 네비게이터 | 드라이버 | 시작 시각 | 끝난 시각 |
    | ---------- | -------- | --------- | --------- |
    | 김수빈     | 김민정   | 13:00     | 14:00     |
    | 김민정     | 김수빈   | 14:00     | 15:00     |
    | 김수빈     | 김민정   | 15:00     | 16:00     |
    | 김민정     | 김수빈   | 17:00     | 18:00     |



## [1] 13:00 - 14:00

> 네비게이터: 김수빈, 드라이버: 김민정

### [드라이버]

#### 기본 환경 설정

1. 가상환경 설정 및 라이브러리 설치

   ```
   $ python -m venv venv
   $ source venv/Scripts/activate
   $ pip install -r requirements.txt
   ```

2. fixtures zip 파일 압축 파일 풀기

3. README.md, README-김민정.md, README-김수빈.md 만들기

4. 프로젝트(pjt08), 앱(movies) 생성 및 등록

   ```
   $ django-admin startproject pjt08 .
   $ python manage.py startapp movie
   ```

   * pjt08/settings.py

   ```python
   INSTALLED_APPS = [
       # Local app
       'movies',
       # Third-party
       'rest_framework',
       # Django apps
       'django.contrib.admin',
       'django.contrib.auth',
       'django.contrib.contenttypes',
       'django.contrib.sessions',
       'django.contrib.messages',
       'django.contrib.staticfiles',
   ]
   ```

5. movies/fixtures 폴더 만들고 json 파일 3개 이동하기

6. git push

7. **오류**

   * json 파일 받아오기

     ```
     $ python manage.py migrate
     $ python manage.py loaddata actors.json movies.json reviews.json
     ```

   * 원인: 아직 model이 만들어지지 않아서 json 파일을 받아올 수 없었다.

   * 해결방법: model 먼저 만들고 json 파일 받아오기



1. 학습한 내용: 기본 환경 세팅
2. 어려웠던 부분: 
   1. 항상 프로젝트 처음에는 뭐부터 시작해야할지 헷갈린다.
   2. json 파일을 load했는데 에러가 나서 당황했고, 에러 코드를 읽어본 결과 모델을 먼저 만들어야 한다는 것을 알 수 있었다. 
3. 새로 배운 것들 및 느낀점: 프로젝트 시작 전 좀 더 차분하게 해야할 일들을 정리하는 연습이 필요할 것 같다.



#### Model 만들기

* movies/models.py

  ```python
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

* 확인

  ```
  $ python manage.py makemigrations
  $ python manage.py migrate
  ```

  db.sqlite3 보고 명세에 맞게 만들어졌는지 확인

1. 학습한 내용: 명세에 맞게 Actor, Movie, Review 모델 만들기
2. 어려웠던 부분: 1:N 관계 설정은 여러 번 연습해봐서 익숙했지만, M:N 관계는 아직 어려워서 수업 자료를 보면서 했다.
3. 새로 배운 것들 및 느낀점: models.py에서 1:N과 M:N 관계를 설정하는 것이 생각보다 어렵지 않았고 연습을 더 해서 자료를 보지 않고도 코드를 짤 수 있도록 해야겠다.



#### Admin

* movies/admin.py

```python
from django.contrib import admin
from .models import Actor, Movie, Review

# Register your models here.
admin.site.register(Actor)
admin.site.register(Movie)
admin.site.register(Review)
```



1. 학습한 내용: 정의한 모델 Actor, Model, Review를 Admin site에 등록
2. 어려웠던 부분: 어려운 부분은 없었다.
3. 새로 배운 것들 및 느낀점: 이제 admin 기능은 완전히 익힌 것 같다.



#### json 파일 load

```
$ python manage.py loaddata actors.json movies.json reviews.json
```

* db.sqlite3 확인하기
* admin 페이지에서도 확인해보기
  * `$ python manage.py createsuperuser`
  * 확인 완료

1. 학습한 내용: 데이터 조회는 JSON 데이터 타입을 따르고, fixtures 사용
2. 어려웠던 부분: 초반에 model을 설정하지 않고 load를 받아서 에러가 났었고, 모델 수정 이후 load하니까 문제 없이 잘 받아졌다.
3. 새로 배운 것들 및 느낀점: fixtures는 처음 다뤄봐서 사용방법이 조금 헷갈리는데, 잘 정리해 두어야겠다.





#### url 분리

1. pjt08/urls.py

   ```python
   from django.contrib import admin
   from django.urls import path, include
   
   urlpatterns = [
       path('admin/', admin.site.urls),
       path('api/v1/', include('movies.urls')),
   ]
   ```

2. movies/urls.py

   ```python
   from django.urls import path
   from . import views
   
   
   urlpatterns = [
       
   ]
   ```

3. 학습한 내용: project와 application url 분리

4. 어려웠던 부분: 이 부분을 처음 setting 때 해줬어야 했는데, 순서가 뒤섞였다.

5. 새로 배운 것들 및 느낀점: 코드 작성을 빠뜨리는 일이 없도록 비슷한 코드들은 한 번에 작성하도록 주의해야겠다.



#### Serializer

1. movies/serializer.py

   ```python
   from rest_framework import serializers
   from .models import Actor, Movie, Review
   
   
   class ActorListSerializer(serializers.ModelSerializer):
       class Meta:
           model = Actor
           fields = '__all__'
   
   
   class ActorSerializer(serializers.ModelSerializer):
   
       class Meta:
           model = Actor
           fields = '__all__'
   
   
   class MovieListSerializer(serializers.ModelSerializer):
   
       class Meta:
           model = Movie
           fields = '__all__'
   
   
   class MovieSerializer(serializers.ModelSerializer):
   
       class Meta:
           model = Movie
           fields = '__all__'
   
   
   class ReviewListSerializer(serializers.ModelSerializer):
   
       class Meta:
           model = Reiew
           fields = '__all__'
   
   
   class ReviewSerializer(serializers.ModelSerializer):
   
       class Meta:
           model = Review
           fields = '__all__'
   ```

2. serializers 폴더를 만들고 각 파일들 분리

   * `actor.py`, `movie.py`, `review.py`
   * ModelSerializer 재정의 필요

   1. movies/serializers/actor.py

      ```python
      from rest_framework import serializers
      from .movie import MovieSerializer
      from ..models import Actor, Movie
      
      
      class ActorListSerializer(serializers.ModelSerializer):
          class Meta:
              model = Actor
              fields = '__all__'
      
      
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

   2. movies/serializers/movie.py

      ```python
      from rest_framework import serializers
      from movies.serializeers.review import ReviewListSerializer
      from ..models import Movie, Actor
      
      
      class MovieListSerializer(serializers.ModelSerializer):
      
          class Meta:
              model = Movie
              fields = '__all__'
      
      
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



1. 학습한 내용: 명세에 나와있는 응답 예시를 참고해서 serializers 작성
2. 어려웠던 부분: 
   1. 참조, 역참조를 할 때 처음에는 ModelSerializer들의 순서를 바꿔가면서 하려고 했는데, 여러 번 겹치는 게 생길 것 같아서 파일을 새로 만들고 각각 분리해서 작성했다.
   2. 생성하는 serializer는 6개인데 응답 예시를 보면 출력 형태가 다양했고, 어떻게 해야할지 많이 고민했다. 교수님께서 ModelSerializer를 재정의하는 방법을 알려주셔서 해결할 수 있었다.
3. 새로 배운 것들 및 느낀점:
   1. 앞으로 할 프로젝트들에서도 이번처럼 많은 serializer 파일들이 생기고 관계도 다양할텐데 serializers 폴더를 만들고 분리하는 방법을 잘 익혀둬야겠다.
   2. ModelSerializer를 재정의하면 serializer를 여러 개 만들지 않고도 출력을 손쉽게 바꿀 수 있다.



### [네비게이터]

* 평소 하던 프로젝트와 달라서 초반 진행에 혼란을 겪음. 
* 가상환경 설치 시: 가상환경과 패키지 설치 후 속도 저하. 원인이 디스코드인지 아닌지 팀원의 세팅에서도 비교해볼 예정
* serializers 작성:
  * serializers에서 고민하고 있던 부분을 교수님께서 깔꼼하게 설명해주셨다. 처음부터 폴더에 넣어서 파일을 분리하고 mtom, 1ton 관계를 정의.
  * 어디가 혼란스러웠는가?: 전체적으로 다,,,, 교재와 실습했던 파일들 다 참고하면서 혼란이 가중되던 차에 내려온 천사같은 설명.

<br>

## [2] 14:00 - 15:00

> 네비게이터: 김민정, 드라이버: 김수빈

### [드라이버]

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

#### serializers/review.py

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



#### urls, views

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

##### 2. `path('actors/<int:actor_pk>/', views.actor_detail),`

- views.py

  - ```python
    @api_view(['GET'])
    def actor_detail(request, actor_pk):
        actor = get_object_or_404(Actor, pk=actor_pk)
        serializer = ActorSerializer(actor)
        return Response(serializer.data)
    ```

    - `get_object_or_404`의 두 번째 인자를 빼먹을 뻔 함

##### 3. `path('movies/', views.movie_list),`

- views.py

  - ```python
    @api_view(['GET'])
    def movie_list(request):
        movies = get_list_or_404(Movie)
        serializer = MovieListSerializer(movies, many=True)
        return Response(serializer.data)
    ```

##### 4. `path('movies/<int:movie_pk>/', views.movie_detail),`

- views.py

  - ```python
    @api_view(['GET'])
    def movie_detail(request, movie_pk):
        movie = get_object_or_404(Movie, pk=movie_pk)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)
    ```

##### 5. `path('reviews/', views.review_list),`

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

  

### [네비게이터]

1. 학습한 내용: status 설정, related_name, read_only_fields, data=request.data 부분 토의
2. 어려웠던 부분: serializers/review.py
   * 에러: 출력에 movie title이 나오지 않고 movie id가 나옴
   * 원인: read_only_fields --- 글 쓰고 나서 유효성 검사할 때 필요
   * 해결: ModelSerializer 재정의
3. 새로 배운 것들 및 느낀점: 
   1. 이번 시간에는 네비게이터로 활동을 했는데 중간중간 서로 헷갈리는 부분이 있었고, 토의를 통해서 해결할 수 있었다. 드라이버님과 대화를 하면서 프로젝트를 더 탄탄하게 짤 수 있어서 좋았다.
   2. `method=='GET'` 일 때는 status 설정 안해도 된다.
   3. `method=='POST'`일 때 instance를 쓰면 `data=request.data` 대신 `request.data`로 적어도 된다.
   4. M:N에서는 related_name('movies')를 설정해주고, 1:N에서는 설정하지 않는다('review_set').

<br>

## [3] 15:00 - 16:00

> 네비게이터: 김수빈, 드라이버: 김민정

### [드라이버]

* 데이터 받아오기

  ```
  $ git pull
  $ python manage.py loaddata movies/actors.json movies/movies.json movies/reviews.json
  ```



#### create_view 기능

* urls.py

  ```python
  urlpatterns = [
      ...
      path('movies/<int:movie_pk>/reviews/', views.create_review),
  ]
  ```

* views.py

  ```python
  @api_view(['POST'])
  def create_review(request, movie_pk):
      movie = get_object_or_404(Movie, pk=movie_pk)
      serializer = ReviewSerializer(data=request.data)
      if serializer.is_valid(raise_exception=True):
          serializer.save(movie=movie)
          return Response(serializer.data, status=status.HTTP_201_CREATED)
  ```

1. 학습한 내용: 리뷰 생성 기능 구현
2. 어려웠던 부분: POST와 PUT 코드 구현이 헷갈렸다.
3. 새로 배운 것들 및 느낀점: 
   1. **POST**: 지난 정보를 받아올 필요가 없기 때문에 `ReviewSerializer(data=request.data)`
   2. **PUT**: 지난 정보를 받아와야 하기 때문에 `ReviewSerializer(review, request.data)`



#### git push

* git push (commit name: `project beta version`)

* 동작 재확인

* 커밋 이름 수정 (commit name: `project completed`)

  * 수정 전

    ```bash
    $ git log --oneline
    68e8b73 (HEAD -> master, origin/master) project beta version
    184e3ce review delete completed
    1461b93 serializer separation & writing
    5d2be6d settings
    ```

  * `git commit --amend`

  * 수정 후

    ```bash
    $ git log --oneline
    f57e8f0 (HEAD -> master) project completed
    184e3ce review delete completed
    1461b93 serializer separation & writing
    5d2be6d settings
    ```

* git pull 해서 merge 하고 test 해보기

1. 학습한 내용: 프로젝트 완료 후 업로드(push), commit 이름 바꾸기
2. 어려웠던 부분: 
   1. 이름을 바꾸고 나서 push를 하면 원격저장소와 로컬저장소의 내용이 다르다고 에러가 나온다.
   2. git pull을 받으면 merge가 되고
   3. 새로운 작업을 하나 하고 git push를 하면 변경사항들이 모두 반영된다.
3. 새로 배운 것들 및 느낀점: `git push` 했던 내용들을 변경하고 싶을 때 어떻게 하면 되는지 연습할 수 있었다.



### [네비게이터]

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

<br>

***

## [마무리] 페어 프로그래밍 소감

* 김민정

  * 이번이 두 번째 페어프로그래밍 프로젝트였는데, 지난 번보다 훨씬 페어 프로그래밍에 익숙해진 것 같다.
  * 페어님과 서로 토의하면서 프로젝트를 하니까 서로 빠뜨린 부분도 금방 찾고 헷갈리는 부분도 쉽게 해결할 수 있었다.
  * 프로젝트 처음에 뭐부터 시작해야 할지 많이 헷갈렸고, 그래서 프로젝트 중간중간 빠뜨린 부분들을 추가해줬는데 좀 더 차분하게 순서를 정리하고 프로젝트를 하는 연습을 해야겠다.
  
  
  
* 김수빈

  - 페어님 덕에 진행이 잘 된 것 같다. 혼자였으면 토요일까지 진행했을 것이다.
  
  ##### 긴급,,오타 발견
  
  ​	serializer 폴더명을 serializeer로 지정했었다. vscode에서 폴더명을 바꾸려는데 계속 에러 뜸 => 그냥 윈도우상에서 폴더명 변경도 시도했으나 어디서 파일이 열려있다고 거절당했다. *왜..? 어디서?*
  
  ​	그냥 폴더를 새로 만들어서 이동시킴
  
  이번에는 저번보다 훨씬 수월했으나 종종 찾아오는 위기와 이상한데 꽂힌 호기심으로 인해 시간을 좀 썼다. 저의 방향을 끌어주신 팀장님께 감사드린다.
  
  
  
  