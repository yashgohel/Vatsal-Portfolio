from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import BlogPost


class AdminLoginForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        if not user.is_staff:
            raise forms.ValidationError(
                "Please sign in with an admin account.",
                code="not_staff",
            )


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ("title", "cover_image", "content")
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "placeholder": "Enter blog title",
                    "class": "admin-input",
                }
            ),
            "cover_image": forms.ClearableFileInput(attrs={"class": "admin-file"}),
            "content": forms.Textarea(
                attrs={
                    "placeholder": "Write the blog content...",
                    "class": "admin-textarea",
                    "rows": 12,
                }
            ),
        }
