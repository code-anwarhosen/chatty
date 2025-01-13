from django.contrib.auth.forms import PasswordChangeForm

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Adding Tailwind CSS classes to each form field
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'w-full p-2 bg-slate-600 rounded-lg mt-2',
                'placeholder': field.label,
            })