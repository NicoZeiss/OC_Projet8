"""Here are all the views we use in the Comparator app"""


from django.shortcuts import render, reverse, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.models import User
from .forms import SearchForm
from .models import Food


def index(request):
    """Display index page"""

    form = SearchForm()
    return render(request, 'comparator/index.html', {'form': form})


def search(request):
    """Send search form request and return results"""

    query = request.GET.get('user_input')
    # We filter into tthe db items which name contains user input
    result_list = Food.objects.filter(name__icontains=query).order_by('code')
    # Adding paginator in order to have 9 results per page
    paginator = Paginator(result_list, 9)
    page = request.GET.get("page")

    try:
        food = paginator.page(page)
    except PageNotAnInteger:
        food = paginator.page(1)
    except EmptyPage:
        food = paginator.page(paginator.num_pages)

    context = {
        "user_input": query,
        "food": food,
        "paginate": True
    }

    return render(request, 'comparator/search.html', context)


def detail(request, bar_code):
    """Display detail page"""

    # If item does not exist, display 404 page
    food = get_object_or_404(Food, code=bar_code)

    context = {
        "food": food
    }

    return render(request, 'comparator/detail.html', context)


def substitute(request):
    """Display substitute page form user product choice"""

    query = request.GET.get('user_substitute')
    # If item does not exist, display 404 page
    user_choice = get_object_or_404(Food, code=query)
    choice_cat = user_choice.category_id
    # Ordering items by nutriscore, in order to find best ones
    full_list = Food.objects.filter(category_id=choice_cat).order_by('nutriscore')
    sub_dic = {}
    i = 0
    # Iterating to have 9 results
    while len(sub_dic) <= 8:
        food = full_list[i]
        user = request.user
        # Checking if items is already added as favourite for authenticated user
        if len(food.user.filter(username=user.username)) != 0:
            sub_dic[food] = True
        else:
            sub_dic[food] = False
        i += 1

    context = {
        "subdic": sub_dic,
        "query": user_choice,
    }

    return render(request, 'comparator/substitute.html', context)

def save_sub(request):
    """Saving substitutes as favourites"""

    if request.user.is_authenticated:
        query_code = request.GET.get('query_code')
        sub_code = request.GET.get('sub_code')
        sub = Food.objects.get(code=sub_code)
        request.user.food.add(sub)

        return HttpResponseRedirect('/comparator/substitute/?user_substitute={}'.format(query_code))

    else:
        return HttpResponseRedirect(reverse('user:connexion'))



def favourites(request):
    """User can see all his saved favourites"""

    if request.user.is_authenticated:
        user = request.user
        sub_list = user.food.all().order_by('nutriscore')
        paginator = Paginator(sub_list, 9)
        page = request.GET.get("page")

        try:
            sublist = paginator.page(page)
        except PageNotAnInteger:
            sublist = paginator.page(1)
        except EmptyPage:
            sublist = paginator.page(paginator.num_pages)


        context = {
            "sublist": sublist
        }

        return render(request, 'comparator/favourites.html', context)

    else:
        return HttpResponseRedirect(reverse('user:connexion'))


def terms(request):
    """The view display terms os use"""
    return render(request, 'comparator/terms.html')
