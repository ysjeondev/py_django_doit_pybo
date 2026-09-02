from django.shortcuts import render, get_object_or_404, redirect
from .models import Question
from django.utils import timezone
from .forms import QuestionForm, AnswerForm
from django.core.paginator import Paginator


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

def answer_create(request, question_id):
    # URL로 전달받은 질문 번호로 질문을 조회한다.
    question = get_object_or_404(
        Question,
        pk=question_id
    )

    if request.method == 'POST':
        # 전송된 답변 내용을 폼에 담는다.
        form = AnswerForm(request.POST)

        # 입력값이 정상적인 경우
        if form.is_valid():
            # 데이터베이스 저장을 잠시 보류한다.
            answer = form.save(commit=False)

            # 답변과 질문을 연결한다.
            answer.question = question

            # 답변 작성 시각을 저장한다.
            answer.create_date = timezone.now()

            # 데이터베이스에 최종 저장한다.
            answer.save()

            # 질문 상세 화면으로 이동한다.
            return redirect(
                'pybo:detail',
                question_id=question.id
            )
    else:
        # GET 요청일 때 빈 답변 폼을 만든다.
        form = AnswerForm()

    # 입력 오류가 있거나 GET 요청이면 상세 화면을 출력한다.
    context = {
        'question': question,
        'form': form
    }

    return render(
        request,
        'pybo/question_detail.html',
        context
    )

def question_create(request):
    #pybo 질문 등록
    
    if request.method == 'POST':
        form = QuestionForm(request.POST)
    
        if form.is_valid():
            question = form.save(commit=False)
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')
    else:
        form =QuestionForm()
    context ={'form':form}
    return render(request, 'pybo/question_form.html', context)


