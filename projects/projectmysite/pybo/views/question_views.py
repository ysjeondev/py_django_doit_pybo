# 질문 등록·수정·삭제 기능을 담당하는 View 파일이다.

# render:
# 폼 화면을 브라우저에 출력한다.
#
# get_object_or_404:
# 지정한 질문이 없으면 404 응답을 반환한다.
#
# redirect:
# 처리가 끝난 후 다른 URL로 이동시킨다.
from django.shortcuts import render, get_object_or_404, redirect

# 현재 시간을 질문 작성일로 저장하기 위해 사용한다.
from django.utils import timezone

# 로그인한 사용자만 질문 등록·수정·삭제를
# 실행할 수 있도록 제한하는 장식자이다.
from django.contrib.auth.decorators import login_required

# 삭제 요청을 POST 방식으로만 허용한다.
from django.views.decorators.http import require_POST

# 권한이 없는 사용자에게 오류 메시지를 전달한다.
from django.contrib import messages

# 현재 파일의 상위 패키지인 pybo의 모델을 가져온다.
from ..models import Question

# 질문 입력값을 검사하고 Question 객체를 만들기 위한 폼이다.
from ..forms import QuestionForm


# ============================================================
# 질문 등록
# URL: /pybo/question/create/
# GET  요청: 빈 질문 등록 폼을 보여 준다.
# POST 요청: 사용자가 입력한 질문을 DB에 저장한다.
# ============================================================
@login_required
def question_create(request):
    # 등록 버튼을 누르면 POST 요청이 들어온다.
    if request.method == 'POST':
        # 사용자가 입력한 제목과 내용을 QuestionForm에 전달한다.
        form = QuestionForm(request.POST)

        # 제목과 내용이 폼의 검증 조건을 통과했는지 확인한다.
        if form.is_valid():
            # commit=False:
            # 아직 author와 create_date를 입력하지 않았으므로
            # DB 저장을 잠시 보류하고 Question 객체만 가져온다.
            question = form.save(commit=False)

            # 현재 로그인한 사용자를 질문 작성자로 지정한다.
            question.author = request.user

            # 현재 시간을 질문 작성일시로 지정한다.
            question.create_date = timezone.now()

            # 모든 필수값을 입력했으므로 DB에 저장한다.
            question.save()

            # 질문 등록이 끝나면 질문 목록으로 이동한다.
            return redirect('pybo:index')

    else:
        # GET 요청은 질문 등록 화면을 처음 열었을 때 발생한다.
        # 사용자에게 보여 줄 빈 폼을 만든다.
        form = QuestionForm()

    # GET 요청 또는 폼 검증 실패 시 실행된다.
    #
    # POST 검증 실패인 경우에는 오류 정보와 기존 입력값이
    # form 객체 안에 들어 있으므로 다시 화면에 표시할 수 있다.
    context = {
        'form': form,
    }

    return render(
        request,
        'pybo/question_form.html',
        context,
    )


# ============================================================
# 질문 수정
# URL 예: /pybo/question/modify/102/
# GET  요청: 기존 질문이 입력된 수정 폼을 보여 준다.
# POST 요청: 사용자가 변경한 내용을 DB에 저장한다.
# ============================================================
@login_required
def question_modify(request, question_id):
    # 수정할 질문을 질문 번호로 조회한다.
    question = get_object_or_404(
        Question,
        pk=question_id,
    )

    # 현재 로그인 사용자와 질문 작성자가 같은지 확인한다.
    #
    # 화면에서 수정 버튼을 숨겼더라도 사용자가 주소를 직접
    # 입력할 수 있으므로 서버에서도 반드시 검사해야 한다.
    if request.user != question.author:
        messages.error(
            request,
            '수정 권한이 없습니다.',
        )

        # 권한이 없으면 질문을 수정하지 않고 상세 화면으로 돌아간다.
        return redirect(
            'pybo:detail',
            question_id=question.id,
        )

    # 수정 내용을 저장하기 위해 POST 요청이 들어온 경우이다.
    if request.method == 'POST':
        # instance=question:
        # 새로운 질문을 생성하지 않고 기존 질문을 수정한다.
        form = QuestionForm(
            request.POST,
            instance=question,
        )

        if form.is_valid():
            # 현재 폼에는 제목과 내용이 들어 있고
            # 추가로 지정해야 할 값이 없으므로 바로 저장할 수 있다.
            question = form.save()

            # 수정이 끝나면 수정된 질문의 상세 화면으로 이동한다.
            return redirect(
                'pybo:detail',
                question_id=question.id,
            )

    else:
        # GET 요청으로 수정 화면을 처음 열었을 때 실행된다.
        #
        # instance=question을 지정하면 기존 제목과 내용이
        # 입력 폼에 자동으로 표시된다.
        form = QuestionForm(instance=question)

    # 처음 수정 화면을 열거나 폼 검증이 실패한 경우
    # 질문 폼 템플릿을 다시 출력한다.
    context = {
        'form': form,
    }

    return render(
        request,
        'pybo/question_form.html',
        context,
    )


# ============================================================
# 질문 삭제
# URL 예: /pybo/question/delete/102/
# POST 요청만 허용한다.
# ============================================================
@login_required
@require_POST
def question_delete(request, question_id):
    # URL로 전달받은 번호에 해당하는 질문을 조회한다.
    question = get_object_or_404(
        Question,
        pk=question_id,
    )

    # 질문 작성자만 삭제할 수 있도록 권한을 확인한다.
    if request.user != question.author:
        messages.error(
            request,
            '삭제 권한이 없습니다.',
        )

        return redirect(
            'pybo:detail',
            question_id=question.id,
        )

    # 질문을 DB에서 삭제한다.
    #
    # Answer 모델과 Comment 모델의 관계가 CASCADE라면
    # 이 질문에 연결된 답변과 댓글도 함께 삭제된다.
    question.delete()

    # 삭제된 질문의 상세 화면은 더 이상 존재하지 않으므로
    # 질문 목록 화면으로 이동한다.
    return redirect('pybo:index')