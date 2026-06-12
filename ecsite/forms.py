from django import forms

class ItemSearchForm(forms.Form):
    # formのフィールドの設定
    category = forms.CharField(label="カテゴリー", max_length=16)
    keyword = forms.CharField(label="キーワード", max_length=256)
    
    # フィールド独自のバリデーションの設定
    def clean_keyword(self):
        keyword = self.cleaned_data['keyword']
        if len(keyword) < 1:
            raise forms.ValidationError("キーワードを入力してください")
        return keyword
    
