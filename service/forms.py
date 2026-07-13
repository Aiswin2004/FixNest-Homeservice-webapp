from django import forms
from .models import Provider,Booking
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class ProviderForm(forms.ModelForm):
    work_title = forms.CharField(
        max_length=200,
        label="Recent Work Title"
    )

    work_image = forms.ImageField(
        label="Recent Work Image"
    )
    customer_name = forms.CharField(
        max_length=150,
        label="Customer Name"
    )
    completed_date = forms.DateField(
    label="Completed Work Date",
    widget=forms.DateInput(
        attrs={
            "class": "form-control",
            "type": "date",
        }
    )
)
    customer_phone = forms.CharField(
        max_length=15,
        label="Customer Phone"
    )

    work_address = forms.CharField(
        widget=forms.Textarea(attrs={"rows":3}),
        label="Completed Work Address"
    )
    username = forms.CharField(
    max_length=150,
    widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Username"
    })
)

    email = forms.EmailField(
    widget=forms.EmailInput(attrs={
        "class": "form-control",
        "placeholder": "Email Address"
    })
)

    password = forms.CharField(
    widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Password"
    })
)

    confirm_password = forms.CharField(
    widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Confirm Password"
    })
    )
    class Meta:
        model = Provider

        fields = [
            "name",
            "category",
            "description",
            "price",
            "phone",
            "adhaar_no",
            "provider_address",
            "original_price",
            "availability",
            "rating",
            "image",
            "is_featured",
            "is_bestworker",
        ]
        widgets = {

            "name": forms.TextInput(attrs={
                "class":"form-control",
                "placeholder":"Provider Name"
            }),

            "phone": forms.TextInput(attrs={
                "class":"form-control",
                "placeholder":"Mobile No"
            }),
            "adhaar_no":forms.TextInput(attrs={
                "class":"form-control",
                "placeholder":"Adhaar No"
            }),
            "provider_address":forms.TextInput(attrs={
                "class":"form-control",
                "placeholder":"Address"
            }),

            "description": forms.Textarea(attrs={
                "class":"form-control",
                "rows":4,
                "placeholder":"Describe your service"
            }),

            "price": forms.NumberInput(attrs={
                "class":"form-control"
            }),

            "original_price": forms.NumberInput(attrs={
                "class":"form-control"
            }),

            "category": forms.Select(attrs={
                "class":"form-control"
            }),

            "availability": forms.Select(attrs={
                "class":"form-control"
            }),

            "rating": forms.NumberInput(attrs={
                "class":"form-control",
                "step":"0.1"
            }),

            "image": forms.ClearableFileInput(attrs={
                "class":"form-control"
            }),

            "is_featured": forms.CheckboxInput(attrs={
                "class":"form-check-input"
            }),

            "is_bestworker": forms.CheckboxInput(attrs={
                "class":"form-check-input"
            }),

        }

    
# ─── REGISTRATION FORM ────────────────────────────────────────────────────────
class RegisterForm(UserCreationForm):
    """
    Extends Django's built-in UserCreationForm.
    Adds email and name fields.
    """
    first_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First Name'
        })
    )
    last_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last Name'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email Address'
        })
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username'
        })
    )
    phone_no = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Phone Number'
        })
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm Password'
        })
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email','phone_no', 'password1', 'password2']


# ─── LOGIN FORM ───────────────────────────────────────────────────────────────
class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )
#provider_id,start_date,end_date,unavailable_date,reason
class provider_blocked_date():
    provider_id = forms .IntegerField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder':'ID'
        })
    )
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class':'form-control',
            'placeholder':'Start Date',
            'type':'date'
        })
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class':'form-control',
            'placeholder':'End Date',
            'type':'date'
        })
    )
    unavailable_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class':'form-control',
            'placeholder':'unavailable Date',
            'type':'date'
        })
    )
    reason=forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'Reason For Leave'
        })
    )
    class Meta:
        model = User
        fields = ['provider_id', 'start_date', 'end_date', 'unavailable_date','reason']


class BookingForm(forms.ModelForm):

    class Meta:
        model = Booking

        fields = [
            "customer_name",
            "customer_phone",
            "service_address",
            "booking_date",
            "booking_time",
            "problem_description",
        ]

        widgets = {

            "customer_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Your Name"
            }),

            "customer_phone": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Mobile Number"
            }),

            "service_address": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Enter Service Address"
            }),

            "booking_date": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),

            "booking_time": forms.TimeInput(attrs={
                "class": "form-control",
                "type": "time"
            }),

            "problem_description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Describe your problem"
            }),

        }