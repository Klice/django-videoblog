# -*- coding: utf-8 -*-
from django.forms import ModelForm, Textarea, HiddenInput
from videoblog.models import Feedback


class FeedbackForm(ModelForm):
    class Meta:
        model = Feedback
        fields = ['ip', 'name', 'email', 'text']
        widgets = {
            'ip': HiddenInput(),
            'text': Textarea(attrs={'cols': 30, 'rows': 10}),
        }
