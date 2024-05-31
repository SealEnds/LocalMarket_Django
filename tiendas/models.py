from django.db import models
from django.contrib.auth.models import User # importar modelo usuario por defecto de django
from django_ckeditor_5.fields import CKEditor5Field
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator, MaxLengthValidator # valores min y max para numeros

# Create your models here.
# tags
# tiendas
# discount
# user discount
# productos
# reviews

class Tag(models.Model):
    name = models.CharField(default='Tag', max_length=50,verbose_name='Nombre')
    description = models.CharField(max_length=255,verbose_name='Descripción', null=True, blank=True) # null is in database, blank is in form
    class Meta:
        verbose_name_plural = 'Tags'
    def __str__(self):
        return self.name
    
class Tienda(models.Model):
    name = models.CharField(default='Tienda', max_length=50,verbose_name='Nombre')
    description = models.TextField(max_length=300, null=True, blank=True, verbose_name='Descripción')
    content = CKEditor5Field(verbose_name='Contenido', null=True, blank = True, config_name='extends')
    image = models.ImageField(default='null', null=True, verbose_name='Imagen Principal', upload_to="tiendas")
    web = models.CharField(max_length=50,verbose_name='Web', null=True, blank=True)
    url = models.CharField(max_length=255, null=True, blank=True, verbose_name='Web URL')
    email = models.EmailField(max_length=50, verbose_name='Email', blank=True, null=True)
    phone = models.CharField(max_length=12, verbose_name='Teléfono', blank=True, null=True)
    address = models.TextField(max_length=255, null=True, blank=True, verbose_name='Dirección')
    visible = models.BooleanField(default=True, verbose_name='Visible')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha Creación", null=True)
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name="Última actualización", null=True)
    user = models.ForeignKey(User, editable=False, verbose_name='Usuario', on_delete=models.CASCADE, default=1) # guarda id usuario que crea la tienda. Con Cascade borra todo lo creado por el usuario. editable=False para no poder elegir el usuario
    tags = models.ManyToManyField(Tag, verbose_name='Tags', blank=True) # relación muchos a muchos con django. Crea junction table automáticamente. blank=True para que puedan no tener valor
    class Meta:
        verbose_name_plural = 'Tiendas'
        ordering = ['-created_at'] # ordenar de más reciente a más antiguo
    def __str__(self):
        return self.name

# class Discount(models.Model):
#     name = models.CharField(default='Descuento', max_length=50, verbose_name='Descuento'),
#     percentage = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
#     class Meta:
#         verbose_name_plural = 'Descuentos'
#         ordering = ['-percentage'] # ordenar de más bajo a más alto
#     def __str__(self):
#         return self.name

class Producto(models.Model):
    name = models.CharField(default='Producto', max_length=50, verbose_name='Producto')
    description = models.TextField(max_length=300, null=True, blank=True, verbose_name='Descripción')
    content = CKEditor5Field(verbose_name='Contenido', null=True, blank=True, config_name='extends')
    image = models.ImageField(default='null', null=True, verbose_name='Imagen principal', upload_to="productos")
    price = models.DecimalField(default=0, max_digits=5, decimal_places=2, validators=[MinValueValidator(0)], blank=True, null=True, verbose_name='Precio')
    ref = models.CharField(max_length=16, blank=True, null=True, verbose_name='Referencia') # no unique porque es único pero solo por tienda
    visible = models.BooleanField(default=True, verbose_name='Visible')
    in_stock = models.BooleanField(default=True, verbose_name='En Stock')
    stock = models.IntegerField(default=0, validators=[MinValueValidator(-1), MaxValueValidator(10000)])
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha creación", null=True)
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name="Última actualización", null=True)
    user = models.ForeignKey(User, editable=False, verbose_name='Usuario', on_delete=models.CASCADE, default=1) # guarda id usuario que crea el producto. Con Cascade borra todo lo creado por el usuario. editable=False para no poder elegir el usuario
    tienda = models.ForeignKey(Tienda, editable=False, verbose_name='Tienda', on_delete=models.CASCADE, default=1)
    tags = models.ManyToManyField(Tag, verbose_name='Tags', blank=True)
    # discount = models.ManyToManyField(Discount, editable=False, verbose_name='Descuentos', default=1, blank=True)
    class Meta:
        verbose_name_plural = 'Productos'
        ordering = ['-created_at'] # ordenar de más reciente a más antiguo
    def __str__(self):
        return self.name
    
# class UserProductDiscount(models.Model): # cada usuario tiene un descuento asociado a un producto específico
#     detail = models.CharField(default='Detail', max_length=255, verbose_name='Información Adicional', null=True, blank=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     product = models.ForeignKey(Producto, on_delete=models.CASCADE)
#     discount = models.ForeignKey(Discount, on_delete=models.CASCADE)

class Review(models.Model):
    detail = models.TextField(default='Detail', verbose_name='Detail', blank=True, null=True)
    review_content = models.TextField(verbose_name='Contenido', blank=True, null=True)
    rating = models.IntegerField(verbose_name='Valoración', validators=[MinValueValidator(1), MaxValueValidator(5)], blank=True, null=True)
    visible = models.BooleanField(default=True, verbose_name='Visible')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha Creación", null=True)
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name="Última actualización", null=True)
    user = models.ForeignKey(User, editable=False, verbose_name='Usuario', on_delete=models.CASCADE, default=1)
    producto = models.ForeignKey(Producto, editable=False, verbose_name='Producto', on_delete=models.CASCADE, default=1)
    class Meta:
        verbose_name_plural = 'Reviews'
        ordering = ['-created_at'] # ordenar de más reciente a más antiguo
    def __str__(self):
        detail_str = self.detail if self.detail else "No Detail"
        user_str = str(self.user) if self.user else "No User"
        producto_str = str(self.producto) if self.producto else "No Producto"
        return f"Review: {detail_str} by {user_str} for {producto_str}"
