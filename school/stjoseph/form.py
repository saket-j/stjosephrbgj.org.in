from django import forms

class RegisterForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'eg: Abc Xyz',}), max_length=100)
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder':'eg: name@domain.com',}), max_length=300)
    pas = forms.CharField(widget=forms.PasswordInput(), min_length=6, max_length=100)
    cpas = forms.CharField(widget=forms.PasswordInput(), min_length=6, max_length=100)
    tit = forms.ChoiceField(widget=forms.Select(attrs={'onChange':'ValueChange()',}),
                                choices=(("1","Alumni (Past Student)"),("2", "Student (Current)"),("3", "Staff"),("4", "Alumni & Staff (Past Student and now Teacher)"),))
    cla = forms.ChoiceField(widget=forms.Select(),choices=(("1","LKG"),("2", "UKG"),("3", "I"),
                                                         ("4","II"),("5", "III"),("6", "IV"),
                                                         ("7","V"),("8", "VI"),("9", "VII"),
                                                         ("10","VIII"),("11", "IX"),("12", "X"),
                                                         ))
    yop = forms.IntegerField(min_value=1950, max_value=2020)
    yj = forms.IntegerField(min_value=1950, max_value=2020)
    subj = forms.CharField(widget=forms.Textarea(attrs={'rows': 2,'class': 'xlarge'}))
    cw = forms.CharField(widget=forms.Textarea(attrs={'rows': 3,'class': 'xxlarge',}))
    lf = forms.URLField(widget=forms.TextInput(attrs={'class': 'xxlarge','placeholder':'http://www.facebook.com/profile.php?id=100001575135427',}),required=False)
    con = forms.CharField(required=False, max_length=20)
    cap = forms.IntegerField()
    capq = forms.CharField(widget=forms.HiddenInput())

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(), max_length=300)
    pas = forms.CharField(widget=forms.PasswordInput(), min_length=6, max_length=100)
    cap = forms.IntegerField()
    capq = forms.CharField(widget=forms.HiddenInput())
    
class CPForm(forms.Form):
    pas = forms.CharField(widget=forms.PasswordInput(), min_length=6, max_length=100)
    cpas = forms.CharField(widget=forms.PasswordInput(), min_length=6, max_length=100)  

class FPForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(), max_length=300)
    cap = forms.IntegerField()
    capq = forms.CharField(widget=forms.HiddenInput())
