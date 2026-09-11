from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages

from .models import Question, Answer
from .forms import QuestionForm, AnswerForm

# Create your views here.
def index(request):
    # 주소에서 현재 페이지 번호를 가져온다.
    page = request.GET.get('page', '1')

    # 전체 질문을 최신순으로 조회한다.
    question_list = Question.objects.order_by('-create_date')

    # 한 페이지에 10개씩 나눈다.
    paginator = Paginator(question_list, 10)

    # 요청한 페이지의 데이터만 가져온다.
    page_obj = paginator.get_page(page)

    # QuerySet이 아니라 Page 객체를 전달한다.
    context = {
        'question_list': page_obj
    }

    return render(
        request,
        'pybo/question_list.html',
        context
    )

def detail(request,question_id):
    #pybo 내용 출력
    question = get_object_or_404(Question, id=question_id)
    context = { 'question':question}
    return render(request,'pybo/question_detail.html', context)

@login_required
def answer_create(request, question_id):
    question = get_object_or_404(
        Question,
        pk=question_id
    )

    if request.method == 'POST':
        form = AnswerForm(request.POST)

        if form.is_valid():
            answer = form.save(commit=False)

            # 현재 로그인 사용자를 작성자로 지정
            answer.author = request.user

            answer.question = question
            answer.create_date = timezone.now()
            answer.save()

            return redirect(
                'pybo:detail',
                question_id=question.id
            )

    else:
        form = AnswerForm()

    context = {
        'question': question,
        'form': form
    }

    return render(
        request,
        'pybo/question_detail.html',
        context
    )

@login_required
def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)

        if form.is_valid():
            question = form.save(commit=False)

            # 현재 로그인 사용자를 작성자로 지정
            question.author = request.user

            question.create_date = timezone.now()
            question.save()

            return redirect('pybo:index')

    else:
        form = QuestionForm()

    context = {
        'form': form
    }

    return render(
        request,
        'pybo/question_form.html',
        context
    )

@login_required
def question_modify(request, question_id):
    # URL에서 받은 question_id에 해당하는 질문을 조회한다.
    #
    # 질문이 존재하지 않으면 직접 예외를 발생시키는 대신
    # Django가 자동으로 404 응답을 반환한다.
    question = get_object_or_404(
        Question,
        pk=question_id
    )

    # 현재 로그인 사용자와 질문 작성자가 같은지 검사한다.
    #
    # 화면에서 수정 버튼을 숨겨도 사용자가 수정 URL을 직접
    # 입력할 수 있으므로 서버에서도 반드시 권한을 검사해야 한다.
    if request.user != question.author:
        # 일회성 오류 메시지를 저장한다.
        # redirect된 다음 화면에서 이 메시지를 출력할 수 있다.
        messages.error(
            request,
            '수정 권한이 없습니다.'
        )

        # 권한이 없으면 해당 질문의 상세 화면으로 돌려보낸다.
        return redirect(
            'pybo:detail',
            question_id=question.id
        )

    # 수정 폼에서 저장 버튼을 눌렀을 때 POST 요청이 들어온다.
    if request.method == 'POST':
        # request.POST에는 사용자가 수정한 제목과 내용이 들어 있다.
        #
        # instance=question을 반드시 지정해야 기존 질문이 수정된다.
        # instance를 생략하면 새로운 질문이 하나 더 생성될 수 있다.
        form = QuestionForm(
            request.POST,
            instance=question
        )

        # 제목과 내용이 폼의 유효성 검사를 통과했는지 확인한다.
        if form.is_valid():
            # commit=False는 바로 DB에 저장하지 않고
            # 수정할 Question 객체를 먼저 반환한다.
            question = form.save(commit=False)

            # 수정 시각 기능은 이후 절에서 모델에 modify_date를
            # 추가한 다음 저장할 예정이다.
            #
            # 현재는 제목과 내용만 수정해서 저장한다.
            question.save()

            # 수정 완료 후 수정된 질문 상세 화면으로 이동한다.
            return redirect(
                'pybo:detail',
                question_id=question.id
            )

    else:
        # GET 요청은 처음 수정 화면에 들어온 경우다.
        #
        # instance=question을 지정하면 기존 질문의 제목과 내용이
        # 입력 폼에 자동으로 채워진다.
        form = QuestionForm(instance=question)

    # 폼 검증 실패 또는 처음 수정 화면을 요청한 경우
    # 기존 질문 등록 템플릿을 재사용한다.
    context = {
        'form': form
    }

    return render(
        request,
        'pybo/question_form.html',
        context
    )

@login_required
@require_POST
def question_delete(request, question_id):
    # URL로 전달된 질문 번호를 이용해 삭제할 질문을 조회한다.
    #
    # 존재하지 않는 질문 번호라면 Django가 404를 반환한다.
    question = get_object_or_404(
        Question,
        pk=question_id
    )

    # 현재 로그인 사용자와 질문 작성자가 다르면
    # 삭제 작업을 수행하지 않는다.
    if request.user != question.author:
        messages.error(
            request,
            '삭제 권한이 없습니다.'
        )

        return redirect(
            'pybo:detail',
            question_id=question.id
        )

    # 작성자 본인인 경우 질문을 데이터베이스에서 삭제한다.
    #
    # Answer.question의 on_delete가 CASCADE이므로
    # 질문에 연결된 답변도 함께 삭제된다.
    question.delete()

    # 삭제된 질문의 상세 주소는 더 이상 존재하지 않으므로
    # 질문 목록 화면으로 이동한다.
    return redirect('pybo:index')

@login_required
def answer_modify(request, answer_id):
    # URL에서 받은 answer_id로 수정할 답변을 조회한다.
    answer = get_object_or_404(
        Answer,
        pk=answer_id
    )

    # 현재 로그인 사용자가 답변 작성자인지 검사한다.
    #
    # 다른 사용자가 URL을 직접 입력해 접근하는 경우도
    # 이 조건에서 차단된다.
    if request.user != answer.author:
        messages.error(
            request,
            '수정 권한이 없습니다.'
        )

        return redirect(
            'pybo:detail',
            question_id=answer.question.id
        )

    if request.method == 'POST':
        # 기존 answer 객체와 사용자가 수정한 내용을 함께 전달한다.
        #
        # instance=answer가 있으므로 새로운 답변이 만들어지지 않고
        # 기존 답변의 content가 변경된다.
        form = AnswerForm(
            request.POST,
            instance=answer
        )

        if form.is_valid():
            # 현재 AnswerForm은 content 필드만 처리하므로
            # 별도의 값 추가 없이 바로 저장할 수 있다.
            answer = form.save()

            # 수정 완료 후 답변이 속한 질문 상세 화면으로 이동한다.
            return redirect(
                'pybo:detail',
                question_id=answer.question.id
            )

    else:
        # 수정 화면을 처음 열 때 기존 답변 내용을 폼에 채운다.
        form = AnswerForm(instance=answer)

    context = {
        'form': form,
        'answer': answer
    }

    return render(
        request,
        'pybo/answer_form.html',
        context
    )

@login_required
@require_POST
def answer_delete(request, answer_id):
    # URL에서 전달받은 answer_id를 이용해
    # 데이터베이스에서 삭제할 답변을 조회한다.
    #
    # 해당 번호의 답변이 없으면 프로그램 오류를 발생시키는 대신
    # Django가 자동으로 404 응답을 반환한다.
    answer = get_object_or_404(
        Answer,
        pk=answer_id
    )

    # 현재 로그인한 사용자(request.user)와
    # 답변을 작성한 사용자(answer.author)가 같은지 확인한다.
    #
    # 템플릿에서 삭제 버튼을 숨겨도 사용자가 URL을 직접 호출할 수 있으므로
    # 서버의 View에서도 반드시 작성자 권한을 검사해야 한다.
    if request.user != answer.author:
        # 권한이 없는 사용자에게 보여줄 일회성 오류 메시지를 등록한다.
        messages.error(
            request,
            '삭제 권한이 없습니다.'
        )

        # 삭제하지 않고 답변이 속한 질문 상세 화면으로 돌아간다.
        return redirect(
            'pybo:detail',
            question_id=answer.question.id
        )

    # 답변을 삭제하면 answer.question 관계를 더 이상 안전하게
    # 사용할 수 없으므로, 삭제하기 전에 질문 번호를 보관한다.
    question_id = answer.question.id

    # 작성자 본인의 답변을 데이터베이스에서 삭제한다.
    answer.delete()

    # 삭제 완료 후 원래 질문의 상세 화면으로 이동한다.
    return redirect(
        'pybo:detail',
        question_id=question_id
    )