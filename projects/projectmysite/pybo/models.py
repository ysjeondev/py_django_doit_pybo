from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()

    def __str__(self):
        return self.subject


class Answer(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )

    content = models.TextField()
    create_date = models.DateTimeField()

    def __str__(self):
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