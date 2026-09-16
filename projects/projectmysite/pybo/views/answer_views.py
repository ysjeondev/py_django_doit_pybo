# ============================================================
# answer_views.py
#
# 질문에 달리는 답변의 등록·수정·삭제 기능을 담당한다.
#
# 처리 기능:
# 1. answer_create : 답변 등록
# 2. answer_modify : 답변 수정
# 3. answer_delete : 답변 삭제
# ============================================================


# render:
# HTML 템플릿에 데이터를 전달해 화면을 만든다.
#
# get_object_or_404:
# 요청한 질문이나 답변이 존재하지 않으면
# 자동으로 404 응답을 반환한다.
#
# redirect:
# 처리가 완료된 후 다른 URL로 이동시킨다.
from django.shortcuts import render, get_object_or_404, redirect


# 현재 날짜와 시간을 가져오기 위해 사용한다.
#
# Python의 datetime.now() 대신 timezone.now()를 사용하면
# Django의 TIME_ZONE 및 USE_TZ 설정을 적용할 수 있다.
from django.utils import timezone


# 로그인한 사용자만 답변 등록·수정·삭제 기능을
# 실행할 수 있도록 제한한다.
from django.contrib.auth.decorators import login_required


# 답변 삭제 요청을 POST 방식으로만 허용한다.
#
# 사용자가 주소창에 삭제 URL을 직접 입력하는 GET 요청으로
# 데이터가 삭제되는 것을 방지한다.
from django.views.decorators.http import require_POST


# 답변 수정·삭제 권한이 없을 때
# 사용자에게 오류 메시지를 전달하기 위해 사용한다.
from django.contrib import messages


# 현재 파일 위치:
# pybo/views/answer_views.py
#
# 점 두 개(..)는 상위 패키지인 pybo를 의미한다.
# pybo/models.py에서 Question과 Answer 모델을 가져온다.
from ..models import Question, Answer


# pybo/forms.py에서 답변 입력 폼을 가져온다.
from ..forms import AnswerForm


# ============================================================
# 1. 답변 등록
#
# URL 예:
# /pybo/answer/create/102/
#
# question_id:
# 답변이 등록될 질문의 번호이다.
#
# GET 요청:
# 이 프로젝트에서는 일반적으로 직접 사용하지 않는다.
#
# POST 요청:
# 질문 상세 화면에서 입력한 답변 내용을 DB에 저장한다.
# ============================================================
@login_required
def answer_create(request, question_id):
    # URL에서 전달받은 question_id를 이용하여
    # 답변을 등록할 질문을 조회한다.
    #
    # 해당 질문이 존재하지 않으면 Django가
    # 자동으로 404 응답을 반환한다.
    question = get_object_or_404(
        Question,
        pk=question_id,
    )

    # 질문 상세 화면에서 답변 등록 버튼을 누르면
    # POST 방식으로 요청이 전달된다.
    if request.method == 'POST':
        # request.POST에는 사용자가 입력한 답변 내용이 들어 있다.
        #
        # 예:
        # request.POST['content']
        form = AnswerForm(request.POST)

        # 답변 내용이 폼의 유효성 검사를 통과했는지 확인한다.
        #
        # 예:
        # 필수 입력값인 content가 비어 있지 않은지 검사한다.
        if form.is_valid():
            # commit=False를 사용하면 DB에 즉시 저장하지 않고
            # Answer 객체만 먼저 반환한다.
            #
            # 아직 다음 값들이 지정되지 않았기 때문이다.
            # - 답변 작성자
            # - 답변이 속한 질문
            # - 답변 작성일시
            answer = form.save(commit=False)

            # 현재 로그인한 사용자를 답변 작성자로 지정한다.
            answer.author = request.user

            # 이 답변이 어떤 질문에 등록되는지 지정한다.
            answer.question = question

            # 현재 시간을 답변 작성일시로 지정한다.
            answer.create_date = timezone.now()

            # 모든 필수값이 준비되었으므로 DB에 저장한다.
            answer.save()

            # 답변 등록이 완료되면 답변이 등록된
            # 질문 상세 화면으로 다시 이동한다.
            return redirect(
                'pybo:detail',
                question_id=question.id,
            )

    else:
        # 주소를 직접 입력하는 등의 이유로 GET 요청이 들어온 경우
        # 빈 답변 폼을 만든다.
        form = AnswerForm()

    # GET 요청이거나 POST 폼 검증에 실패하면 실행된다.
    #
    # question:
    # 질문 상세 화면을 다시 출력하기 위해 전달한다.
    #
    # form:
    # 사용자가 입력한 값과 폼 오류 내용을 전달한다.
    context = {
        'question': question,
        'form': form,
    }

    # 답변 입력 중 오류가 발생하면
    # 질문 상세 화면을 다시 출력한다.
    return render(
        request,
        'pybo/question_detail.html',
        context,
    )


# ============================================================
# 2. 답변 수정
#
# URL 예:
# /pybo/answer/modify/15/
#
# answer_id:
# 수정할 답변의 번호이다.
#
# GET 요청:
# 기존 답변 내용이 입력된 수정 폼을 보여 준다.
#
# POST 요청:
# 사용자가 변경한 답변 내용을 DB에 저장한다.
# ============================================================
@login_required
def answer_modify(request, answer_id):
    # URL에서 전달받은 answer_id를 이용해
    # 수정할 답변을 조회한다.
    answer = get_object_or_404(
        Answer,
        pk=answer_id,
    )

    # 현재 로그인한 사용자와 답변 작성자가 같은지 검사한다.
    #
    # question_detail.html에서 수정 버튼을 숨겨도
    # 다른 사용자가 수정 URL을 직접 입력할 수 있으므로
    # 서버에서도 반드시 권한을 확인해야 한다.
    if request.user != answer.author:
        # 권한이 없다는 일회성 메시지를 등록한다.
        messages.error(
            request,
            '수정 권한이 없습니다.',
        )

        # 답변이 속한 질문의 상세 화면으로 돌아간다.
        return redirect(
            'pybo:detail',
            question_id=answer.question.id,
        )

    # 수정 폼에서 저장 버튼을 누르면 POST 요청이 들어온다.
    if request.method == 'POST':
        # 사용자가 입력한 수정 내용과 기존 답변 객체를
        # AnswerForm에 함께 전달한다.
        #
        # instance=answer를 지정하지 않으면 기존 답변이 수정되지 않고
        # 새로운 답변이 만들어질 수 있다.
        form = AnswerForm(
            request.POST,
            instance=answer,
        )

        # 입력한 답변 내용이 폼 검증을 통과했는지 확인한다.
        if form.is_valid():
            # 기존 answer 객체에 수정된 content를 반영하고
            # DB에 저장한다.
            answer = form.save()

            # 수정이 완료되면 답변이 속한 질문 상세 화면으로 이동한다.
            return redirect(
                'pybo:detail',
                question_id=answer.question.id,
            )

    else:
        # GET 요청으로 수정 화면을 처음 열었을 때 실행된다.
        #
        # instance=answer를 지정하면 기존 답변 내용이
        # 수정 입력창에 자동으로 표시된다.
        form = AnswerForm(instance=answer)

    # 수정 화면에 전달할 데이터를 구성한다.
    context = {
        # 답변 입력 폼
        'form': form,

        # 수정 중인 답변 객체
        'answer': answer,
    }

    # 답변 수정 전용 템플릿을 출력한다.
    return render(
        request,
        'pybo/answer_form.html',
        context,
    )


# ============================================================
# 3. 답변 삭제
#
# URL 예:
# /pybo/answer/delete/15/
#
# answer_id:
# 삭제할 답변의 번호이다.
#
# @require_POST:
# 삭제 기능은 반드시 POST 요청으로만 실행한다.
# ============================================================
@login_required
@require_POST
def answer_delete(request, answer_id):
    # URL에서 전달받은 answer_id에 해당하는
    # 답변을 데이터베이스에서 조회한다.
    answer = get_object_or_404(
        Answer,
        pk=answer_id,
    )

    # 현재 로그인한 사용자와 답변 작성자를 비교한다.
    #
    # 작성자가 아니라면 답변을 삭제할 수 없다.
    if request.user != answer.author:
        # 삭제 권한이 없다는 메시지를 등록한다.
        messages.error(
            request,
            '삭제 권한이 없습니다.',
        )

        # 답변을 삭제하지 않고 질문 상세 화면으로 돌아간다.
        return redirect(
            'pybo:detail',
            question_id=answer.question.id,
        )

    # 답변을 삭제하기 전에 질문 번호를 별도 변수에 저장한다.
    #
    # answer.delete()를 실행한 뒤에는 삭제된 answer 객체의
    # 관계 정보를 사용하는 것이 안전하지 않기 때문이다.
    question_id = answer.question.id

    # 작성자 본인의 답변을 DB에서 삭제한다.
    answer.delete()

    # 답변 삭제가 끝나면 원래 질문 상세 화면으로 이동한다.
    return redirect(
        'pybo:detail',
        question_id=question_id,
    )