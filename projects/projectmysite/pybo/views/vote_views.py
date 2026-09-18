# ============================================================
# vote_views.py
#
# 질문과 답변의 추천 기능을 담당한다.
#
# 처리 기능:
# 1. vote_question : 질문 추천
# 2. vote_answer   : 답변 추천
# ============================================================


# get_object_or_404:
# 추천할 질문 또는 답변을 조회한다.
# 데이터가 존재하지 않으면 자동으로 404 응답을 반환한다.
#
# redirect:
# 추천 처리가 끝나면 질문 상세 화면으로 이동한다.
from django.shortcuts import get_object_or_404, redirect


# 로그인한 사용자만 추천 기능을 사용할 수 있게 한다.
#
# 로그인하지 않은 사용자가 추천 URL을 요청하면
# 로그인 화면으로 이동한다.
from django.contrib.auth.decorators import login_required


# 추천은 DB 내용을 변경하는 작업이므로
# POST 요청만 허용한다.
#
# 주소창에 URL을 입력하는 GET 요청으로
# 추천 데이터가 변경되는 것을 방지한다.
from django.views.decorators.http import require_POST


# 자신의 질문이나 답변을 추천할 때
# 사용자에게 오류 메시지를 전달한다.
from django.contrib import messages


# 현재 파일은 pybo/views/vote_views.py에 있으므로
# 점 두 개(..)를 사용해 상위 pybo 패키지의
# models.py에서 Question과 Answer를 가져온다.
from ..models import Question, Answer


# ============================================================
# 1. 질문 추천
#
# URL 예:
# /pybo/vote/question/102/
#
# question_id:
# 추천할 질문의 번호이다.
#
# 처리 흐름:
# 1. 로그인 여부 확인
# 2. POST 요청 여부 확인
# 3. 추천할 질문 조회
# 4. 자기 질문인지 확인
# 5. 추천인 목록에 현재 사용자 추가
# 6. 질문 상세 화면으로 이동
# ============================================================
@login_required
@require_POST
def vote_question(request, question_id):
    # URL로 전달받은 question_id에 해당하는 질문을 조회한다.
    #
    # 질문이 존재하지 않으면 서버 오류 대신
    # Django가 자동으로 404 응답을 반환한다.
    question = get_object_or_404(
        Question,
        pk=question_id,
    )

    # 현재 로그인한 사용자가 질문 작성자인지 확인한다.
    #
    # 커뮤니티에서는 일반적으로 자신이 작성한 글을
    # 자신이 추천하지 못하도록 제한한다.
    if request.user == question.author:
        # 추천은 처리하지 않고 오류 메시지만 등록한다.
        messages.error(
            request,
            '본인이 작성한 질문은 추천할 수 없습니다.',
        )

    else:
        # 현재 로그인한 사용자를 질문의 추천인 목록에 추가한다.
        #
        # voter는 ManyToManyField이므로 add()를 사용한다.
        question.voter.add(request.user)

        # 같은 사용자가 추천 버튼을 여러 번 눌러도
        # 동일한 사용자-질문 관계가 중복 저장되지는 않는다.
        messages.success(
            request,
            '질문을 추천했습니다.',
        )

    # 추천 처리 후 현재 질문의 상세 화면으로 이동한다.
    return redirect(
        'pybo:detail',
        question_id=question.id,
    )


# ============================================================
# 2. 답변 추천
#
# URL 예:
# /pybo/vote/answer/15/
#
# answer_id:
# 추천할 답변의 번호이다.
#
# 처리 흐름:
# 1. 로그인 여부 확인
# 2. POST 요청 여부 확인
# 3. 추천할 답변 조회
# 4. 자기 답변인지 확인
# 5. 추천인 목록에 현재 사용자 추가
# 6. 답변이 등록된 질문 상세 화면으로 이동
# ============================================================
@login_required
@require_POST
def vote_answer(request, answer_id):
    # URL로 전달받은 answer_id에 해당하는 답변을 조회한다.
    answer = get_object_or_404(
        Answer,
        pk=answer_id,
    )

    # 현재 로그인 사용자가 답변 작성자인지 확인한다.
    if request.user == answer.author:
        # 자기 답변이면 추천하지 않고 오류 메시지를 전달한다.
        messages.error(
            request,
            '본인이 작성한 답변은 추천할 수 없습니다.',
        )

    else:
        # 현재 로그인 사용자를 답변의 추천인 목록에 추가한다.
        answer.voter.add(request.user)

        messages.success(
            request,
            '답변을 추천했습니다.',
        )

    # 답변은 독립된 상세 화면이 없고
    # 질문 상세 화면 안에 표시된다.
    #
    # 따라서 답변이 속한 질문 상세 화면으로 이동한다.
    return redirect(
        'pybo:detail',
        question_id=answer.question.id,
    )