# ============================================================
# comment_views.py
#
# 질문과 답변에 작성하는 댓글 기능을 담당한다.
#
# 질문 댓글:
# 1. comment_create_question : 질문 댓글 등록
# 2. comment_modify_question : 질문 댓글 수정
# 3. comment_delete_question : 질문 댓글 삭제
#
# 답변 댓글:
# 4. comment_create_answer   : 답변 댓글 등록
# 5. comment_modify_answer   : 답변 댓글 수정
# 6. comment_delete_answer   : 답변 댓글 삭제
# ============================================================


# render:
# HTML 템플릿에 데이터를 전달하고 화면을 만든다.
#
# get_object_or_404:
# 요청한 질문, 답변, 댓글이 존재하지 않으면
# 자동으로 404 응답을 반환한다.
#
# redirect:
# 댓글 처리가 끝난 후 질문 상세 화면으로 이동시킨다.
from django.shortcuts import render, get_object_or_404, redirect


# 댓글 작성일과 수정일에 현재 시간을 저장하기 위해 사용한다.
from django.utils import timezone


# 로그인한 사용자만 댓글 등록·수정·삭제 기능을
# 사용할 수 있도록 제한한다.
from django.contrib.auth.decorators import login_required


# 댓글 삭제를 POST 요청으로만 실행되게 제한한다.
#
# 주소창에 삭제 URL을 직접 입력하는 GET 요청으로
# 데이터가 삭제되는 것을 방지한다.
from django.views.decorators.http import require_POST


# 댓글 수정·삭제 권한이 없을 때
# 사용자에게 오류 메시지를 전달하기 위해 사용한다.
from django.contrib import messages


# 현재 파일 위치:
# pybo/views/comment_views.py
#
# 점 두 개(..)는 상위 패키지인 pybo를 의미한다.
#
# Comment는 모델이므로 반드시 models에서 가져와야 한다.
from ..models import Question, Answer, Comment


# 댓글 입력값을 검사하고 Comment 객체를 만드는 폼이다.
from ..forms import CommentForm


# ============================================================
# 1. 질문 댓글 등록
#
# URL 예:
# /pybo/comment/create/question/102/
#
# question_id:
# 댓글이 등록될 질문의 번호이다.
#
# GET 요청:
# 빈 댓글 등록 폼을 보여 준다.
#
# POST 요청:
# 입력한 댓글을 질문에 연결하여 DB에 저장한다.
# ============================================================
@login_required
def comment_create_question(request, question_id):
    # 댓글을 등록할 질문을 조회한다.
    #
    # 해당 질문이 존재하지 않으면 404 응답을 반환한다.
    question = get_object_or_404(
        Question,
        pk=question_id,
    )

    # 댓글 등록 버튼을 누르면 POST 요청이 들어온다.
    if request.method == 'POST':
        # 사용자가 입력한 댓글 내용을 CommentForm에 전달한다.
        form = CommentForm(request.POST)

        # 댓글 내용이 폼 유효성 검사를 통과했는지 확인한다.
        if form.is_valid():
            # 아직 작성자, 질문, 작성일을 넣어야 하므로
            # DB 저장을 잠시 보류한다.
            comment = form.save(commit=False)

            # 현재 로그인한 사용자를 댓글 작성자로 지정한다.
            comment.author = request.user

            # 이 댓글이 어느 질문에 속하는지 지정한다.
            comment.question = question

            # 질문 댓글이므로 answer는 지정하지 않는다.
            #
            # Comment 모델에서 answer 필드가
            # null=True, blank=True로 설정되어 있어야 한다.
            comment.answer = None

            # 현재 시간을 댓글 작성일시로 지정한다.
            comment.create_date = timezone.now()

            # 모든 필수값이 준비되었으므로 DB에 저장한다.
            comment.save()

            # 댓글 등록 후 원래 질문의 상세 화면으로 이동한다.
            return redirect(
                'pybo:detail',
                question_id=question.id,
            )

    else:
        # GET 요청으로 댓글 등록 화면을 처음 열었을 때
        # 사용자에게 보여 줄 빈 폼을 생성한다.
        form = CommentForm()

    # 중요:
    # context는 if/else 바깥에 있어야 한다.
    #
    # 그래야 다음 두 경우 모두 실행할 수 있다.
    # 1. GET 요청으로 등록 화면을 처음 열었을 때
    # 2. POST 요청의 폼 검증에 실패했을 때
    context = {
        'form': form,
        'question_id': question.id,
        'form_title': '질문 댓글 등록',
    }

    # 질문 댓글 등록 폼을 화면에 출력한다.
    return render(
        request,
        'pybo/comment_form.html',
        context,
    )


# ============================================================
# 2. 답변 댓글 등록
#
# URL 예:
# /pybo/comment/create/answer/15/
#
# answer_id:
# 댓글이 등록될 답변의 번호이다.
#
# GET 요청:
# 빈 댓글 등록 폼을 보여 준다.
#
# POST 요청:
# 댓글을 해당 답변에 연결하여 DB에 저장한다.
# ============================================================
@login_required
def comment_create_answer(request, answer_id):
    # 댓글을 등록할 답변을 조회한다.
    answer = get_object_or_404(
        Answer,
        pk=answer_id,
    )

    # 댓글 등록 버튼을 누르면 POST 요청이 들어온다.
    if request.method == 'POST':
        # 사용자가 입력한 댓글 내용을 폼에 전달한다.
        form = CommentForm(request.POST)

        # 입력값이 유효한지 검사한다.
        if form.is_valid():
            # 작성자, 답변, 작성일을 추가하기 위해
            # DB 저장을 잠시 보류한다.
            comment = form.save(commit=False)

            # 현재 로그인 사용자를 댓글 작성자로 지정한다.
            comment.author = request.user

            # 이 댓글이 어느 답변에 속하는지 지정한다.
            comment.answer = answer

            # 답변 댓글이므로 question은 지정하지 않는다.
            comment.question = None

            # 댓글 작성일시를 현재 시간으로 지정한다.
            comment.create_date = timezone.now()

            # 답변 댓글을 DB에 저장한다.
            comment.save()

            # 답변은 질문 상세 화면에 표시되므로
            # 답변이 속한 질문 상세 화면으로 이동한다.
            return redirect(
                'pybo:detail',
                question_id=answer.question.id,
            )

    else:
        # GET 요청이면 빈 댓글 폼을 생성한다.
        form = CommentForm()

    # GET 요청 또는 폼 검증 실패 시
    # 댓글 폼 템플릿에 전달할 데이터를 구성한다.
    context = {
        'form': form,

        # 목록으로 또는 취소 기능에서 사용할 수 있도록
        # 답변이 속한 질문 번호를 전달한다.
        'question_id': answer.question.id,

        # 등록 폼의 제목을 구분하기 위해 전달한다.
        'form_title': '답변 댓글 등록',
    }

    return render(
        request,
        'pybo/comment_form.html',
        context,
    )


# ============================================================
# 3. 질문 댓글 수정
#
# URL 예:
# /pybo/comment/modify/question/7/
#
# comment_id:
# 수정할 댓글의 번호이다.
#
# GET 요청:
# 기존 댓글 내용이 입력된 수정 폼을 보여 준다.
#
# POST 요청:
# 변경한 댓글 내용과 수정일시를 DB에 저장한다.
# ============================================================
@login_required
def comment_modify_question(request, comment_id):
    # 질문에 연결된 댓글만 조회한다.
    #
    # question__isnull=False:
    # question 필드에 질문이 연결되어 있는 댓글만 찾는다.
    #
    # 이 조건이 있으므로 답변 댓글을 질문 댓글 수정 기능으로
    # 잘못 수정하는 것을 방지할 수 있다.
    comment = get_object_or_404(
        Comment,
        pk=comment_id,
        question__isnull=False,
    )

    # 현재 로그인한 사용자와 댓글 작성자가 같은지 확인한다.
    if request.user != comment.author:
        messages.error(
            request,
            '댓글 수정 권한이 없습니다.',
        )

        # 권한이 없으면 댓글이 속한 질문 상세 화면으로 돌아간다.
        return redirect(
            'pybo:detail',
            question_id=comment.question.id,
        )

    # 댓글 수정 내용을 저장하기 위한 POST 요청이다.
    if request.method == 'POST':
        # instance=comment:
        # 새로운 댓글을 생성하지 않고 기존 댓글을 수정한다.
        form = CommentForm(
            request.POST,
            instance=comment,
        )

        if form.is_valid():
            # modify_date를 추가해야 하므로
            # DB 저장을 잠시 보류한다.
            comment = form.save(commit=False)

            # 댓글을 수정한 현재 시간을 기록한다.
            comment.modify_date = timezone.now()

            # 변경된 댓글을 DB에 저장한다.
            comment.save()

            # 수정 완료 후 질문 상세 화면으로 이동한다.
            return redirect(
                'pybo:detail',
                question_id=comment.question.id,
            )

    else:
        # GET 요청으로 수정 화면을 처음 열었을 때
        # 기존 댓글 내용을 폼에 채운다.
        form = CommentForm(instance=comment)

    # 수정 폼에 전달할 데이터를 구성한다.
    context = {
        'form': form,
        'question_id': comment.question.id,
        'form_title': '질문 댓글 수정',
    }

    return render(
        request,
        'pybo/comment_form.html',
        context,
    )


# ============================================================
# 4. 답변 댓글 수정
#
# URL 예:
# /pybo/comment/modify/answer/8/
#
# comment_id:
# 수정할 답변 댓글의 번호이다.
# ============================================================
@login_required
def comment_modify_answer(request, comment_id):
    # 답변에 연결된 댓글만 조회한다.
    #
    # answer__isnull=False:
    # answer 필드에 답변이 연결된 댓글만 찾는다.
    #
    # 따라서 질문 댓글이 이 기능에서 수정되는 것을 방지한다.
    comment = get_object_or_404(
        Comment,
        pk=comment_id,
        answer__isnull=False,
    )

    # 현재 로그인한 사용자가 댓글 작성자인지 확인한다.
    if request.user != comment.author:
        messages.error(
            request,
            '댓글 수정 권한이 없습니다.',
        )

        # 답변 댓글은 답변이 속한 질문의 상세 화면에 표시된다.
        return redirect(
            'pybo:detail',
            question_id=comment.answer.question.id,
        )

    # 댓글 수정 내용을 저장하는 POST 요청이다.
    if request.method == 'POST':
        # 기존 댓글 객체와 수정된 내용을 폼에 전달한다.
        form = CommentForm(
            request.POST,
            instance=comment,
        )

        if form.is_valid():
            # 수정일시를 추가해야 하므로 바로 저장하지 않는다.
            comment = form.save(commit=False)

            # 현재 시간을 댓글 수정일시로 지정한다.
            comment.modify_date = timezone.now()

            # 수정된 댓글을 DB에 저장한다.
            comment.save()

            # 댓글이 달린 답변의 질문 상세 화면으로 돌아간다.
            return redirect(
                'pybo:detail',
                question_id=comment.answer.question.id,
            )

    else:
        # 수정 화면을 처음 열었을 때
        # 기존 댓글 내용을 입력 폼에 표시한다.
        form = CommentForm(instance=comment)

    context = {
        'form': form,
        'question_id': comment.answer.question.id,
        'form_title': '답변 댓글 수정',
    }

    return render(
        request,
        'pybo/comment_form.html',
        context,
    )


# ============================================================
# 5. 질문 댓글 삭제
#
# URL 예:
# /pybo/comment/delete/question/7/
#
# 댓글 삭제는 POST 방식으로만 처리한다.
# ============================================================
@login_required
@require_POST
def comment_delete_question(request, comment_id):
    # 질문에 연결된 댓글만 조회한다.
    comment = get_object_or_404(
        Comment,
        pk=comment_id,
        question__isnull=False,
    )

    # 현재 로그인 사용자가 댓글 작성자인지 확인한다.
    if request.user != comment.author:
        messages.error(
            request,
            '댓글 삭제 권한이 없습니다.',
        )

        return redirect(
            'pybo:detail',
            question_id=comment.question.id,
        )

    # 댓글을 삭제한 후 돌아갈 질문 번호를 먼저 보관한다.
    #
    # 삭제 후에는 comment.question 관계를 사용하는 것이
    # 안전하지 않을 수 있기 때문이다.
    question_id = comment.question.id

    # 선택한 질문 댓글 한 건을 DB에서 삭제한다.
    comment.delete()

    # 댓글이 있던 질문의 상세 화면으로 이동한다.
    return redirect(
        'pybo:detail',
        question_id=question_id,
    )


# ============================================================
# 6. 답변 댓글 삭제
#
# URL 예:
# /pybo/comment/delete/answer/8/
#
# 댓글 삭제는 POST 방식으로만 처리한다.
# ============================================================
@login_required
@require_POST
def comment_delete_answer(request, comment_id):
    # 답변에 연결된 댓글만 조회한다.
    comment = get_object_or_404(
        Comment,
        pk=comment_id,
        answer__isnull=False,
    )

    # 현재 로그인한 사용자와 댓글 작성자를 비교한다.
    if request.user != comment.author:
        messages.error(
            request,
            '댓글 삭제 권한이 없습니다.',
        )

        return redirect(
            'pybo:detail',
            question_id=comment.answer.question.id,
        )

    # 댓글을 삭제하기 전에 답변이 속한 질문 번호를 저장한다.
    question_id = comment.answer.question.id

    # 선택한 답변 댓글 한 건을 DB에서 삭제한다.
    comment.delete()

    # 원래 질문의 상세 화면으로 이동한다.
    return redirect(
        'pybo:detail',
        question_id=question_id,
    )