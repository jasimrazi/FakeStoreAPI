from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from urllib.parse import urljoin
from django.conf import settings
from products.models import Product
from products.serializers import ProductSerializer

class ProductSearchView(GenericAPIView):
    serializer_class = ProductSerializer

    
    def post(self, request):
        search_query = request.data.get('search_query', '')
        if search_query:
            products = Product.objects.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))
            if not products.exists():
                return Response({'message': 'No products found'}, status=status.HTTP_404_NOT_FOUND)
            
            serializer = self.serializer_class(products, many=True)
            return Response({'data': serializer.data, 'message': 'Products fetched successfully'}, status=status.HTTP_200_OK)
        
        return Response({'message': 'No query found'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        search_query = request.query_params.get('search_query', '')
        if search_query:
            products = Product.objects.filter(
                Q(title__icontains=search_query)
            ).values('title').distinct()[:10]
            
            if not products.exists():
                return Response({'Message': 'No suggestions found'}, status=status.HTTP_400_BAD_REQUEST)

            suggestion_list = [{'product_title': product['title']} for product in products]
            
            return Response({'suggestion': suggestion_list, 'message': 'Suggestions fetched successfully', 'success': True}, status=status.HTTP_200_OK)
        
        return Response({'error': 'No search query provided', 'success': False}, status=status.HTTP_400_BAD_REQUEST)
