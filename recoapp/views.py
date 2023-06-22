from rest_framework.response import Response
from rest_framework import status
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from .forms import MyForm
from django.shortcuts import render
from .data import get_popular_products, assign_flower_names


@csrf_exempt
def purchase(request):
    """
    returns 5 recommended flower types
    """
    try:
        if request.method=='POST':
            form = MyForm(request.POST)
            
            if form.is_valid():
                user_id = form.cleaned_data['user_id']

            products_to_recommend = get_popular_products(user_id)

            result = assign_flower_names(user_id,products_to_recommend)

            context = {
                "flowers":result,
                "form": form 
            }

            print(context)

            form = MyForm()

            return render(request, 'templates/recoapp/home.html', context)
        
        else:
            form = MyForm()
            context = {'form': form}
            return render(request, 'templates/recoapp/home.html', context)

    except Exception as e:
        print(e)
        return Response({
                            "Success": False, 
                            "Status": status.HTTP_501_NOT_IMPLEMENTED, \
                            "Message":"An error was encountered during execution"
                        })