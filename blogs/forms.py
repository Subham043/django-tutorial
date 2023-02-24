from django import forms
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _ #for post type
from django.core.exceptions import ValidationError
from .models import Article

BIRTH_YEAR_CHOICES = ['1980', '1981', '1982']
FAVORITE_COLORS_CHOICES = [
    ('blue', 'Blue'),
    ('green', 'Green'),
    ('black', 'Black'),
    
]

class NameForm(forms.Form):

    your_name = forms.CharField(label='Your name', max_length=100)
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)
    birth_year = forms.DateField(widget=forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES))
    single_color = forms.ChoiceField(required=False, choices=FAVORITE_COLORS_CHOICES)
    favorite_colors = forms.MultipleChoiceField(
        required=False,
        widget=forms.RadioSelect,
        choices=FAVORITE_COLORS_CHOICES,
    )
    comment = forms.CharField(widget=forms.TextInput(attrs={'size': '40'}))

    your_name.widget.attrs.update({'class': 'special'})

    template_name = "form_template.html"

    def validate(self, value):
        """Check if value consists only of valid emails."""
        # Use the parent's handling of required fields, etc.
        super().validate(value)
        for sender in value:
            validate_email(sender)

    def clean(self):
        cleaned_data = super().clean()
        cc_myself = cleaned_data.get("cc_myself")
        subject = cleaned_data.get("subject")

        if cc_myself and subject:
            # Only do something if both fields are valid so far.
            if "help" not in subject:
                raise ValidationError(
                    "Did not send for 'help' in the subject despite "
                    "CC'ing yourself."
                )
            
    def send_email(self):
        # send email using the self.cleaned_data dictionary
        pass

class ArticleForm(forms.ModelForm):
    # title = forms.CharField(label='Your name', max_length=100)
    class Meta:
        model = Article
        # fields = ['title','author']
        fields = '__all__'
        localized_fields = ('publish_on',)
        widgets = {
            'description': forms.Textarea(attrs={'cols': 80, 'rows': 20}),
        }
        labels = {
            'title': _('Your name'),
        }
        help_texts = {
            'title': _('Some useful help text.'),
        }
        error_messages = {
            'title': {
                'max_length': _("This writer's name is too long."),
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'special'})

    def clean_title(self):
        # custom validation for the title field
        pass


