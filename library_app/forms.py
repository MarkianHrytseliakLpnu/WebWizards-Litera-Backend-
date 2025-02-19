from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Підтвердіть пароль")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            self.add_error('email', "Користувач з таким email вже існує")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Паролі не співпадають")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if email and password:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                self.add_error(None, "Невірний email або пароль")
                return cleaned_data

            if not user.check_password(password):
                self.add_error(None, "Невірний email або пароль")
            else:
                cleaned_data['user'] = user

        return cleaned_data


class UserSettingsForm(forms.ModelForm):
    """
    Оновлює поля username, first_name, last_name, email, phone_number.
    Також дозволяє змінити пароль за умови введення старого.
    """
    old_password = forms.CharField(
        label="Старий пароль",
        widget=forms.PasswordInput,
        required=False
    )
    new_password1 = forms.CharField(
        label="Новий пароль",
        widget=forms.PasswordInput,
        required=False
    )
    new_password2 = forms.CharField(
        label="Підтвердження нового пароля",
        widget=forms.PasswordInput,
        required=False
    )

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "phone_number"]

    def __init__(self, user=None, *args, **kwargs):
        """
        Зберігаємо request.user, щоб звірити старий пароль при зміні.
        Якщо instance не передано, то підставимо user як instance.
        """
        self.user = user  # це actual користувач із сесії
        if "instance" not in kwargs and user is not None:
            kwargs["instance"] = user
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get("old_password")
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")

        # Перевірка зміни пароля лише якщо принаймні одне з нових полів заповнено
        if new_password1 or new_password2:
            # Користувач повинен ввести старий пароль
            if not old_password:
                self.add_error("old_password", "Потрібно ввести старий пароль.")
            else:
                # Перевіряємо, чи старий пароль дійсний
                if not self.user.check_password(old_password):
                    self.add_error("old_password", "Старий пароль невірний.")

            # Перевірка співпадіння нового пароля
            if new_password1 and new_password2 and new_password1 != new_password2:
                self.add_error("new_password2", "Паролі не співпадають.")
        return cleaned_data

    def save(self, commit=True):
        """
        Зберігає основні дані користувача (username, first_name, last_name, email, phone_number).
        Якщо нові поля для пароля заповнено, змінює пароль.
        """
        user = super().save(commit=False)

        # Якщо користувач ввів новий пароль (і перевірки успішні), оновлюємо його
        new_password1 = self.cleaned_data.get("new_password1")
        new_password2 = self.cleaned_data.get("new_password2")
        if new_password1 and new_password2 and new_password1 == new_password2:
            user.set_password(new_password1)

        if commit:
            user.save()
        return user
