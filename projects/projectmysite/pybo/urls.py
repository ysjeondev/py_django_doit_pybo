# ============================================================
# pybo/urls.py
#
# pybo 앱에서 사용하는 URL과 View 함수를 연결한다.
#
# 기존에는 모든 함수가 pybo/views.py에 있었지만,
# 현재는 기능별로 다음 네 파일로 분리했다.
#
# base_views.py     : 질문 목록·상세
# question_views.py : 질문 등록·수정·삭제
# answer_views.py   : 답변 등록·수정·삭제
# comment_views.py  : 질문·답변 댓글 등록·수정·삭제
# ============================================================


# path:
# URL 주소와 실행할 View 함수를 연결한다.
from django.urls import path


# pybo/views 폴더에 분리한 View 모듈들을 가져온다.
#
# 다음 import 문은 각각 아래 파일을 의미한다.
#
# base_views     → pybo/views/base_views.py
# question_views → pybo/views/question_views.py
# answer_views   → pybo/views/answer_views.py
# comment_views  → pybo/views/comment_views.py
from .views import (
    base_views,
    question_views,
    answer_views,
    comment_views,
)


# URL 이름 앞에 pybo라는 네임스페이스를 사용한다.
#
# 템플릿이나 View에서는 다음처럼 URL을 사용할 수 있다.
#
# {% url 'pybo:index' %}
# redirect('pybo:detail', question_id=question.id)
app_name = 'pybo'


urlpatterns = [
    # ========================================================
    # 1. 기본 조회 URL
    # 담당 파일: base_views.py
    # ========================================================

    # 질문 목록
    #
    # 최종 주소:
    # /pybo/
    #
    # 실행 함수:
    # pybo/views/base_views.py의 index()
    path(
        '',
        base_views.index,
        name='index',
    ),

    # 질문 상세
    #
    # 예:
    # /pybo/102/
    #
    # <int:question_id>는 URL의 숫자를 question_id라는
    # 이름으로 detail 함수에 전달한다.
    path(
        '<int:question_id>/',
        base_views.detail,
        name='detail',
    ),


    # ========================================================
    # 2. 질문 등록·수정·삭제 URL
    # 담당 파일: question_views.py
    # ========================================================

    # 질문 등록
    #
    # 주소:
    # /pybo/question/create/
    path(
        'question/create/',
        question_views.question_create,
        name='question_create',
    ),

    # 질문 수정
    #
    # 예:
    # /pybo/question/modify/102/
    path(
        'question/modify/<int:question_id>/',
        question_views.question_modify,
        name='question_modify',
    ),

    # 질문 삭제
    #
    # 예:
    # /pybo/question/delete/102/
    path(
        'question/delete/<int:question_id>/',
        question_views.question_delete,
        name='question_delete',
    ),


    # ========================================================
    # 3. 답변 등록·수정·삭제 URL
    # 담당 파일: answer_views.py
    # ========================================================

    # 답변 등록
    #
    # question_id:
    # 답변이 등록될 질문 번호이다.
    #
    # 예:
    # /pybo/answer/create/102/
    path(
        'answer/create/<int:question_id>/',
        answer_views.answer_create,
        name='answer_create',
    ),

    # 답변 수정
    #
    # answer_id:
    # 수정할 답변 번호이다.
    #
    # 예:
    # /pybo/answer/modify/15/
    path(
        'answer/modify/<int:answer_id>/',
        answer_views.answer_modify,
        name='answer_modify',
    ),

    # 답변 삭제
    #
    # answer_id:
    # 삭제할 답변 번호이다.
    #
    # 예:
    # /pybo/answer/delete/15/
    path(
        'answer/delete/<int:answer_id>/',
        answer_views.answer_delete,
        name='answer_delete',
    ),


    # ========================================================
    # 4. 질문 댓글 URL
    # 담당 파일: comment_views.py
    # ========================================================

    # 질문 댓글 등록
    #
    # question_id:
    # 댓글이 등록될 질문 번호이다.
    path(
        'comment/create/question/<int:question_id>/',
        comment_views.comment_create_question,
        name='comment_create_question',
    ),

    # 질문 댓글 수정
    #
    # comment_id:
    # 수정할 댓글 번호이다.
    path(
        'comment/modify/question/<int:comment_id>/',
        comment_views.comment_modify_question,
        name='comment_modify_question',
    ),

    # 질문 댓글 삭제
    #
    # comment_id:
    # 삭제할 댓글 번호이다.
    path(
        'comment/delete/question/<int:comment_id>/',
        comment_views.comment_delete_question,
        name='comment_delete_question',
    ),


    # ========================================================
    # 5. 답변 댓글 URL
    # 담당 파일: comment_views.py
    # ========================================================

    # 답변 댓글 등록
    #
    # answer_id:
    # 댓글이 등록될 답변 번호이다.
    path(
        'comment/create/answer/<int:answer_id>/',
        comment_views.comment_create_answer,
        name='comment_create_answer',
    ),

    # 답변 댓글 수정
    path(
        'comment/modify/answer/<int:comment_id>/',
        comment_views.comment_modify_answer,
        name='comment_modify_answer',
    ),

    # 답변 댓글 삭제
    path(
        'comment/delete/answer/<int:comment_id>/',
        comment_views.comment_delete_answer,
        name='comment_delete_answer',
    ),
]