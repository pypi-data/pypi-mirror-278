from django import forms


class AppointmentForm(forms.Form):
    name = forms.CharField(
        label='', max_length=20,
        widget=forms.TextInput(attrs={'placeholder': '성함', 'class': 'form-control'})
    )
    email = forms.CharField(
        label='', max_length=20,
        widget=forms.TextInput(attrs={'placeholder': '이메일', 'class': 'form-control'})
    )
    subject = forms.CharField(
        label='', max_length=20,
        widget=forms.TextInput(attrs={'placeholder': '제목', 'class': 'form-control'})
    )
    message = forms.CharField(
        label='',
        required=False,
        widget=forms.Textarea(attrs={'placeholder': '문의사항',
                                     'class': 'form-control',
                                     'rows': '4'}))

