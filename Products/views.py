from django.shortcuts import render,get_object_or_404,redirect
from . import models
from django.db.models import Count
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from . import forms
from django.contrib import messages

# Create your views here.
def home(request):
    products = models.Product.objects.all()
    categories = models.Category.objects.annotate(product_count = Count('products'))

    context = {
        'products': products,
        'categories': categories
    }

    return render(request, 'products/home.html', context)

def category_products(request, category_slug):
    category = get_object_or_404(models.Category, slug = category_slug)
    products = models.Product.objects.filter(category=category)
    paginator = Paginator(products, 6)
    context ={
        'products': paged_products,
        'category': category,
    }
    return render(request, 'products/category_products.html', context)

def product_detail(request, product_slug):
    product = get_object_or_404(models.Product, slug = product_slug)
    reviews = product.reviews.filter(status = True)

    rating_counts = {
        '5': product.reviews.filter(rating__gt = 4.4, rating__lte=5.1).count(),
        '4': product.reviews.filter(rating__gt = 3.4, rating__lte=4.1).count(),
        '3': product.reviews.filter(rating__gt = 2.4, rating__lte=3.1).count(),
        '2': product.reviews.filter(rating__gt = 1.4, rating__lte=2.1).count(),
        '1': product.reviews.filter(rating__gt = 0.4, rating__lte=1.1).count(),
    }

    total_reviews = sum(rating_counts.values())

    rating_percentages = {
        '5': (rating_counts['5'] / total_reviews * 100) if total_reviews else 0,
        '5': (rating_counts['4'] / total_reviews * 100) if total_reviews else 0,
        '5': (rating_counts['3'] / total_reviews * 100) if total_reviews else 0,
        '5': (rating_counts['2'] / total_reviews * 100) if total_reviews else 0,
        '5': (rating_counts['1'] / total_reviews * 100) if total_reviews else 0,
    }

    context = {
        'product': product,
        'rating_counts': rating_counts,
        'rating_percentages': rating_percentages,
        'reviews': reviews, 
    }

    return render(request, 'products/product-left-thumbline.html', context)

@login_required
def submit_review(request, product_slug):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = models.review.objects.get(user__id = request.user.id, product_slug = product_slug)
            form = forms.ReviewForm(request.POST, instance = reviews)
            form.save()
            messages.success(request, 'Thank you!')
            return redirect(url)
        except models.review.DoesNotExist:
            form = forms.ReviewForm(request.POST)
            if form.is_valid():
                data = models.review()
                data.product = models.Product.objects.get(slug = product_slug)
                data.user_id = request.user.id
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.save()
                messages.success(request, 'Thank you!')
                return redirect(url)