from django import forms

class PublicLinkForm(forms.Form):
    public_key = forms.CharField(label='Публичная ссылка', max_length=255)
    file_type = forms.ChoiceField(
        label='Тип файла',
        choices=[
            ('all', 'Все'),
            ('documents', 'Документы'),
            ('images', 'Изображения'),
        ],
        required=False
    )
