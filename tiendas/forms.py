from django import forms
from .models import Tienda, Producto, Review
from django_ckeditor_5.widgets import CKEditor5Widget

class TiendaForm(forms.ModelForm):
    class Meta:
        model = Tienda
        fields = ["name", "description", "content", "image", "web", "email", "phone", "address", "tags", "visible"]
    
    # def save(self, *args, **kwargs):
        # self.description = self.clean_description(self.description)
        # super(TiendaForm, self).save(*args, **kwargs)

    # def clean_description(self, description):
    #     # Remove unnecessary <p> tags at the beginning
    #     if description.startswith('<p></p>'):
    #         description = description[len('<p></p>'):]
    #     return description
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control form-textarea'})
        self.fields['content'].widget.attrs.update({'class': 'form-content'})
        self.fields['image'].widget.attrs.update({'class': 'form-control'})
        self.fields['web'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['phone'].widget.attrs.update({'class': 'form-control'})
        self.fields['address'].widget.attrs.update({'class': 'form-control form-textarea-2'})
        self.fields['tags'].widget.attrs.update({'class': 'form-control form-multipicklist'})
        self.fields['visible'].widget.attrs.update({'class': 'form-check-input'})

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ["name", "ref", "description", "content", "image", "price", "in_stock", "visible"]

    def clean_price(self):
        price = self.cleaned_data.get('price')
        min_price = 0.00
        try:
            price = float(price)
        except (TypeError, ValueError):
            raise forms.ValidationError('El precio no es un valor válido.')
        if price < min_price:
            raise forms.ValidationError(f'El precio debe ser al menos {min_price}.')
        return price

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['ref'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control form-textarea'})
        self.fields['content'].widget.attrs.update({'class': 'form-content'})
        self.fields['image'].widget.attrs.update({'class': 'form-control'})
        self.fields['price'].widget.attrs.update({'class': 'form-control form-number', 'min': '0' })
        self.fields['in_stock'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['visible'].widget.attrs.update({'class': 'form-check-input'})

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "review_content"]

    RATING_CHOICES = [(i, i) for i in range(1, 6)]
    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rating'].widget.attrs.update({'class': 'form-control'})
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['review_content'].widget.attrs.update({'class': 'form-textarea-3'})