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

class LoginUserForm(forms.Form):
    id = forms.CharField(label="会員ID", max_length=128)
    password = forms.CharField(label="パスワード", max_length=256, widget=forms.PasswordInput(render_value=False))

class RegistUserForm(forms.Form):
    id = forms.CharField(label="会員ID", max_length=128)
    password = forms.CharField(label="パスワード", max_length=256, widget=forms.PasswordInput(render_value=False))
    password_confirm = forms.CharField(label="パスワード(確認)", max_length=256, widget=forms.PasswordInput(render_value=False))
    name = forms.CharField(label="お名前", max_length=128)
    address = forms.CharField(label="ご住所", max_length=256)

    def clean(self):
        cleaned_data = super().clean()

        password = self.cleaned_data['password']
        password_confirm = self.cleaned_data['password_confirm']
        if password != password_confirm:
            raise forms.ValidationError("パスワードが異なります")
        cleaned_data.pop('password_confirm', None)
        
        return cleaned_data

class UpdateUserForm(forms.Form):
    password = forms.CharField(label="パスワード", widget=forms.PasswordInput(render_value=False))
    password_confirm = forms.CharField(label="パスワード(確認)", max_length=256, widget=forms.PasswordInput(render_value=False))
    name = forms.CharField(label="お名前")
    address = forms.CharField(label="ご住所")

    def clean(self):
        cleaned_data = super().clean()

        password = self.cleaned_data['password']
        password_confirm = self.cleaned_data['password_confirm']
        if password != password_confirm:
            raise forms.ValidationError("パスワードが異なります")
        cleaned_data.pop('password_confirm', None)
        
        return cleaned_data
