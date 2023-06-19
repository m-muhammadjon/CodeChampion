from django import forms

from apps.problems.models import Attempt


class AttemptForm(forms.ModelForm):
    class Meta:
        model = Attempt
        fields = ["language", "source_code"]
