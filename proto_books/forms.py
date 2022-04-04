from django import forms
from .models import BookmarkModel

class BookmarkForm(forms.ModelForm):
    class Meta():
        model = BookmarkModel
        exclude = ('site_title','site_keyword', 'site_memo')

class BookmarkEditForm(forms.ModelForm):
    class Meta():
        model = BookmarkModel
        fields = ('site_memo', 'site_color')

class TagForm(forms.Form):
    hashtag = forms.CharField(label='キーワード追加')