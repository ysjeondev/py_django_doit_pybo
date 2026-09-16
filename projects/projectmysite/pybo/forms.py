from django import forms
from pybo.models import Question, Answer, Comment

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['subject','content']
        labels = { 'subject':'제목', 'content':'내용'}
        
class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields =['content']
        labels = {
            'content':'답변내용',
        }

class CommentForm(forms.ModelForm):
    class Meta:
        # 이 폼으로 Comment 모델의 데이터를 입력받는다.
        model = Comment
        # 작성자, 질문, 답변, 작성일시는 사용자가 선택하면 안 된다.
        # 서버에서 자동으로 지정하고 사용자는 댓글 내용만 입력한다.
        fields = ['content']
        labels = {
            'content': '댓글내용',
        }

