# Django 데이터베이스 모델 기능을 가져온다.
from django.db import models

# Django가 기본으로 제공하는 사용자 모델이다.
#
# 질문 작성자, 답변 작성자, 댓글 작성자뿐 아니라
# 질문과 답변을 추천한 사용자도 이 모델과 연결한다.
from django.contrib.auth.models import User


# ============================================================
# 질문 모델
#
# 게시판에 등록되는 질문 한 건을 나타낸다.
# ============================================================
class Question(models.Model):

    # 질문을 작성한 사용자이다.
    #
    # 한 사용자는 여러 질문을 작성할 수 있으므로
    # User와 Question은 일대다 관계이다.
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author_question',
    )

    # 질문 제목
    subject = models.CharField(
        max_length=200,
    )

    # 질문 내용
    content = models.TextField()

    # 질문 작성일시
    create_date = models.DateTimeField()

    # 질문 수정일시
    #
    # 수정하지 않은 질문은 값이 없을 수 있으므로
    # null=True와 blank=True를 지정한다.
    modify_date = models.DateTimeField(
        null=True,
        blank=True,
    )

    # ========================================================
    # 질문 추천인
    #
    # 하나의 질문을 여러 사용자가 추천할 수 있고,
    # 한 사용자도 여러 질문을 추천할 수 있으므로
    # 다대다 관계인 ManyToManyField를 사용한다.
    #
    # related_name='voter_question':
    # User 객체에서 사용자가 추천한 질문을 역방향으로
    # 조회할 때 사용할 이름이다.
    #
    # 예:
    # user.voter_question.all()
    #
    # blank=True:
    # 추천자가 한 명도 없는 질문도 저장할 수 있게 한다.
    # ========================================================
    voter = models.ManyToManyField(
        User,
        related_name='voter_question',
        blank=True,
    )

    def __str__(self):
        # 관리자 화면과 Django shell에서
        # Question 객체 대신 질문 제목을 보여 준다.
        return self.subject



# ============================================================
# 답변 모델
#
# 특정 질문에 등록되는 답변 한 건을 나타낸다.
# ============================================================
class Answer(models.Model):

    # 답변을 작성한 사용자
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author_answer',
    )

    # 답변이 등록된 질문
    #
    # 질문이 삭제되면 연결된 답변도 함께 삭제된다.
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
    )

    # 답변 내용
    content = models.TextField()

    # 답변 작성일시
    create_date = models.DateTimeField()

    # 답변 수정일시
    modify_date = models.DateTimeField(
        null=True,
        blank=True,
    )
    # ========================================================
    # 답변 추천인
    #
    # 답변과 사용자도 다대다 관계이다.
    #
    # related_name을 질문 추천인과 다르게 지정해야 한다.
    #
    # 예:
    # user.voter_answer.all()
    # ========================================================
    voter = models.ManyToManyField(
        User,
        related_name='voter_answer',
        blank=True,
    )

    def __str__(self):
        # 관리자 화면이나 shell에서 답변 내용을 표시한다.
        return self.content

class Comment(models.Model):
    # 댓글을 작성한 사용자를 저장한다.
    #
    # Django의 User 모델과 다대일 관계를 만든다.
    # 사용자 한 명은 여러 댓글을 작성할 수 있다.
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    # 질문에 작성된 댓글일 때 해당 질문을 저장한다.
    #
    # 답변에 달린 댓글은 question 값이 없으므로
    # null=True와 blank=True를 사용한다.
    question = models.ForeignKey(
        Question,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    # 답변에 작성된 댓글일 때 해당 답변을 저장한다.
    #
    # 질문에 달린 댓글은 answer 값이 없으므로
    # null=True와 blank=True를 사용한다.
    answer = models.ForeignKey(
        Answer,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    # 댓글 내용을 저장한다.
    content = models.TextField()

    # 댓글이 최초로 작성된 시간을 저장한다.
    create_date = models.DateTimeField()

    # 댓글 수정 시간을 저장한다.
    #
    # 한 번도 수정하지 않은 댓글에는 수정 시간이 없으므로
    # null과 빈 값을 허용한다.
    modify_date = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        # 관리자 화면이나 Django Shell에서 Comment 객체를 출력할 때
        # 알아보기 쉽도록 댓글 내용을 반환한다.
        return self.content