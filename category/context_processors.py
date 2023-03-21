from .models import Category

def categoryMenu(request):
    categories = Category.objects.all()
    return dict(categories=categories)
