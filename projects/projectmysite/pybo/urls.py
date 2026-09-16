from django.urls import path
from . import views

app_name ='pybo'

urlpatterns=urlpatterns = [
    # 질문 목록
    path(
        '',
        views.index,
        name='index'
    ),
    # 질문 등록
    path(
        'question/create/',
        views.question_create,
        name='question_create'
    ),
    # 질문 수정
    # question_id를 이용해 수정할 질문을 찾는다.
    path(
        'question/modify/<int:question_id>/',
        views.question_modify,
        name='question_modify'
    ),
    # 질문 삭제
    # 삭제는 views.py에서 POST 요청만 허용할 예정이다.
    path(
        'question/delete/<int:question_id>/',
        views.question_delete,
        name='question_delete'
    ),
    # 답변 등록
    path(
        'answer/create/<int:question_id>/',
        views.answer_create,
        name='answer_create'
    ),
    # 답변 수정
    # answer_id를 이용해 수정할 답변을 찾는다.
    path(
        'answer/modify/<int:answer_id>/',
        views.answer_modify,
        name='answer_modify'
    ),
    # 답변 삭제
    path(
        'answer/delete/<int:answer_id>/',
        views.answer_delete,
        name='answer_delete'
    ),
    # 질문 상세
    # 숫자로 된 주소는 마지막에 배치하면 URL 구조를 읽기 편하다.
    path(
        '<int:question_id>/',
        views.detail,
        name='detail'
    ),
    # 질문 댓글 등록
    path(
    'comment/create/question/<int:question_id>/',
    views.comment_create_question,
    name='comment_create_question'
    ),
    # 질문 댓글 수정
    path(
    'comment/modify/question/<int:comment_id>/',
    views.comment_modify_question,
    name='comment_modify_question'
    ),
    # 질문 댓글 삭제
    path(
    'comment/delete/question/<int:comment_id>/',
    views.comment_delete_question,
    name='comment_delete_question'
    ),
    # 답변 댓글 등록
    path(
    'comment/create/answer/<int:answer_id>/',
    views.comment_create_answer,
    name='comment_create_answer'
    ),
    # 답변 댓글 수정
    path(
    'comment/modify/answer/<int:comment_id>/',
    views.comment_modify_answer,
    name='comment_modify_answer'
    ),
    # 답변 댓글 삭제
    path(
    'comment/delete/answer/<int:comment_id>/',
    views.comment_delete_answer,
    name='comment_delete_answer'
    ),
]