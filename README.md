# local-market

2º DAW (Web Development) Final Project with Django

1. Guest user (no login): 

See shops and productos

Search products and shops by category

Register / Login 

2. User (registered): 

Add reviews to productos. Edit and delete reviews.
    
    (Possible improvement: Don't allow more than one review per user and product and don't allow reviews in your own products.)

Edit profile info

Request to admins a change of profile to 'owner' (seller would have been a better name). 

3. Owner User: 

Create Shops in Profile

View my shops in profile

Create Products in Shop manually or with csv:

        ref;name;description;price;visible;in_stock
        11100;Producto Uno;Descubre [Nombre del Producto], creado para ofrecerte calidad y rendimiento excepcionales.;10;true;true
        2220;Producto Dos;Descubre [Nombre del Producto], creado para ofrecerte calidad y rendimiento excepcionales.;20;true;false

Use CKeditor5 to add content to shops and products with rich text editor, add images, position them, etc.

Content of shop is: 

    Header: main image, description, data
    Products: A list of paginated productos
    Content: The content created with CKeditor5 rich text editor

Content of product is:

    Header: main image, description, data
    Contet: Created with CKeditor5
    Reviews

4. Admin: superuser

Add a user to the group 'owner' so that it is allowed to create shops and products. Users and Groups use to default Django models.

Static pages can be created from django admin panel

Admin panel names has been customized

5. Project Structure -
3 apps:

mainApp -> Static folder for css and images - Main template: layout.html - Login and register 

paginas -> Generate static pages via admin panel 

tiendas -> Everythin related to shops and products 

Relevant sources:

    https://victorroblesweb.es/

    ckeditor5:
    https://ckeditor.com/ckeditor-5/

    Star icons:
    Shapes and symbols icons created by lakonicon - Flaticon

    Django documentation:
    https://docs.djangoproject.com/en/5.0/