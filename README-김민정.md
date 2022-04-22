# PJT08 (22/04/22)

* 13:00 ~ 14:00 김민정
* 14:00 ~ 15:00 김수빈
* 15:00 ~ 15:30 김민정
* 15:30 ~ README 작성



## [0] 기본 환경 설정

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



### 오류

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







## [1] Model 만들기

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





## [2] Admin

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



## [3] json 파일 load

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





## [4] url 분리

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

1. 학습한 내용: project와 application url 분리
2. 어려웠던 부분: 이 부분을 처음 setting 때 해줬어야 했는데, 순서가 뒤섞였다.
3. 새로 배운 것들 및 느낀점: 코드 작성을 빠뜨리는 일이 없도록 비슷한 코드들은 한 번에 작성하도록 주의해야겠다.



## [5] Serializer

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



***

## 14:00 - 15:00

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



***

## 15:00 - 16:00

* 데이터 받아오기

  ```
  $ git pull
  $ python manage.py loaddata movies/actors.json movies/movies.json movies/reviews.json
  ```



## create_view 기능

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



## git push

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







***

## 마무리

* 이번이 두 번째 페어프로그래밍 프로젝트였는데, 지난 번보다 훨씬 페어 프로그래밍에 익숙해진 것 같다.
* 페어님과 서로 토의하면서 프로젝트를 하니까 서로 빠뜨린 부분도 금방 찾고 헷갈리는 부분도 쉽게 해결할 수 있었다.
* 프로젝트 처음에 뭐부터 시작해야 할지 많이 헷갈렸고, 그래서 프로젝트 중간중간 빠뜨린 부분들을 추가해줬는데 좀 더 차분하게 순서를 정리하고 프로젝트를 하는 연습을 해야겠다.