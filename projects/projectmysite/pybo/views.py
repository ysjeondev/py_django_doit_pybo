from django.shortcuts import render, get_object_or_404, redirect
from .models import Question
from django.utils import timezone
from .forms import QuestionForm, AnswerForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

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


