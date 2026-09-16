# 질문 목록과 질문 상세 조회를 담당하는 View 파일이다.

# render:
# 템플릿에 데이터를 전달하고 HTML 응답을 만든다.
#
# get_object_or_404:
# 데이터가 존재하지 않으면 404 응답을 반환한다.
from django.shortcuts import render, get_object_or_404

# 전체 질문을 페이지 단위로 나누기 위해 사용한다.
from django.core.paginator import Paginator

# 현재 파일은 pybo/views/base_views.py에 있다.
# 점 두 개(..)는 상위 패키지인 pybo를 의미한다.
from ..models import Question


# ============================================================
# 질문 목록 조회
# URL: /pybo/
# 담당 템플릿: pybo/question_list.html
# ============================================================
def index(request):
    # URL에서 페이지 번호를 가져온다.
    #
    # 예:
    # /pybo/?page=3
    #
    # page 값이 없으면 첫 페이지인 1을 사용한다.
    page = request.GET.get('page', '1')

    # 모든 질문을 작성일 내림차순으로 조회한다.
    # 가장 최근에 등록된 질문이 목록의 맨 위에 나온다.
    question_list = Question.objects.order_by('-create_date')

    # 조회한 질문을 한 페이지당 10개씩 나눈다.
    paginator = Paginator(question_list, 10)

    # 사용자가 요청한 페이지의 질문 데이터만 가져온다.
    page_obj = paginator.get_page(page)

    # 템플릿으로 전달할 데이터를 딕셔너리로 구성한다.
    context = {
        'question_list': page_obj,
    }

    # 질문 목록 템플릿을 실행하고 브라우저에 반환한다.
    return render(
        request,
        'pybo/question_list.html',
        context,
    )


# ============================================================
# 질문 상세 조회
# URL 예: /pybo/102/
# 담당 템플릿: pybo/question_detail.html
# ============================================================
def detail(request, question_id):
    # URL에서 전달받은 question_id와 일치하는 질문을 조회한다.
    #
    # 질문이 없으면 서버 오류 대신 404 응답을 반환한다.
    question = get_object_or_404(
        Question,
        pk=question_id,
    )

    # 조회한 질문을 question이라는 이름으로 템플릿에 전달한다.
    context = {
        'question': question,
    }

    # 질문 상세 화면을 사용자에게 반환한다.
    return render(
        request,
        'pybo/question_detail.html',
        context,
    )