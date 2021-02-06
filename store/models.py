import decimal

from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from .validations import *
from django.db import models


class Category(MPTTModel):
    name = models.CharField('Name', max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    image = models.ImageField(null=True, blank=True, upload_to='images', default='images/placeholder.png')

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    """def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' / '.join(full_path[::-1])
    """
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = 'images/placeholder.png'
        return url

    def get_absolute_url(self):
        return reverse('product_list_by_category',
                       args=[self.slug])


class Company(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    country = models.CharField('Country', max_length=15)
    image = models.ImageField(null=True, blank=True, upload_to='images', default='images/placeholder.png')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = 'images/placeholder.png'
        return url

    def get_absolute_url(self):
        return reverse('product_list_by_company',
                       args=[self.slug])

    @property
    def popular(self):
        products = Product.objects.filter(company=self).aggregate(sales=Sum('sales'))
        sales = 0
        if products["sales"] is not None:
            sales = int(products["sales"])
        return sales


class Product(models.Model):
    name = models.CharField('Name', max_length=200, db_index=True)
    category = models.ForeignKey(Category, verbose_name="Category", on_delete=models.CASCADE)
    company = models.ForeignKey(Company, verbose_name="Company", on_delete=models.CASCADE)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    image = models.ImageField(null=True, blank=True, upload_to='images', default='images/placeholder.jpg')

    description = models.TextField('Description', max_length=3000, blank=True, null=True)
    shortSpecifications = models.TextField('Short specifications', max_length=500, null=True)
    specifications = models.TextField('Specifications', max_length=3000, null=True)

    price = models.PositiveIntegerField('Price', validators=[validate_price])
    discount = models.PositiveSmallIntegerField('Discount', default=0, null=True, validators=[validate_discount])
    year = models.PositiveSmallIntegerField('Year', default=datetime.datetime.now().year, validators=[validate_product_year])

    stock = models.PositiveIntegerField('Stock')
    sales = models.PositiveIntegerField('Sales', default=0)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def discount_price(self):
        return round(self.price * decimal.Decimal(1 - self.discount / 100))

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = 'images/placeholder.jpg'
        return url

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.id, self.slug])


class ImageItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    image = models.ImageField(null=True, blank=True, upload_to='images', default='images/placeholder.jpg')

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = 'images/placeholder.jpg'
        return url

    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Product Gallery'


class Comment(models.Model):
    STATUS = (
        ('New', 'New'),
        ('True', 'True'),
        ('False', 'False'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    parent = models.ForeignKey('self', verbose_name="Parent", on_delete=models.CASCADE, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS, default='New')

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.product)