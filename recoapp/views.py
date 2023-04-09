from rest_framework.response import Response
from rest_framework import viewsets, status

from .data import get_popular_products, assign_flower_names


class recommendViewset(viewsets.ViewSet):
    def get_new_user_recommendations(self, request):
        """
        returns number of all policies and their categories based on policy type
        """
        try:
            if request.method=='POST':
                user_id = request.data['user_id']
                products_to_recommend = get_popular_products(user_id)

                result = assign_flower_names(user_id,products_to_recommend)

                result = result.values()

            return Response({
                                "Success": True, 
                                "Status": status.HTTP_200_OK, 
                                "Message": "Successful", 
                                "Result": result
                            })

        except Exception as e:
            print(e)
            return Response({
                                "Success": False, 
                                "Status": status.HTTP_501_NOT_IMPLEMENTED, \
                                "Message":"An error was encountered during execution"
                            })
