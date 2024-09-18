from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializers import ProductSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import Product


# Create your views here.


# Fetch all products on limit and sort
class GetProductsView(GenericAPIView):
    serializer_class = ProductSerializer

    def get(self, request):
        # Retrieve query parameters
        limit = request.GET.get('limit', '10')  # Default limit to '10' if not provided
        sort = request.GET.get('sort', None)    # Default sort to None if not provided

        # Validate and convert limit to integer
        try:
            limit = int(limit)
        except ValueError:
            limit = 10  # Default to 10 if conversion fails

        # Determine sorting order
        if sort == 'desc':
            products = Product.objects.all().order_by('-id')
        else:
            products = Product.objects.all().order_by('id')  # Default to ascending order if not 'desc'

        # Apply limit to the queryset
        products = products[:limit]

        if products.exists():
            # Serialize the products queryset
            serializer = ProductSerializer(products, many=True)
            return Response(
                {"data": serializer.data, "Message": "Fetch successful"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response({"Message": "No data"}, status=status.HTTP_400_BAD_REQUEST)



# Add a product
class AddProductView(GenericAPIView):
    serializer_class = ProductSerializer

    def post(self, request):
        title = request.data.get("title")
        description = request.data.get("description")
        price = request.data.get("price")
        category = request.data.get("category")
        image = request.data.get("image")

        product_data = {
            "title": title,
            "description": description,
            "price": price,
            "category": category,
            "image": image,
        }

        product_serializer = ProductSerializer(data=product_data)

        if product_serializer.is_valid():
            product_serializer.save()
            return Response(
                {"Message": "Product added successfully"}, status=status.HTTP_200_OK
            )

        else:
            return Response(
                {"Message": "Fields empty", "Errors": product_serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ProductIDView(GenericAPIView):
    serializer_class = ProductSerializer

    def get(self, request, productid,):
        a = Product.objects.filter(id=productid)

        if a.exists():
            b = ProductSerializer(a, many=True)
            return Response(
                {"data": b.data, "Message": "Fetch successful"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"Message": "No product found"}, status=status.HTTP_404_NOT_FOUND
            )


class AllCategoriesView(GenericAPIView):
    serializer_class = ProductSerializer

    def get(self, request):
        # Fetch distinct categories from the Product model
        categories = Product.objects.values_list('category', flat=True).distinct()

        # Check if categories exist
        if categories:
            return Response(
                {"data": list(categories), "Message": "Categories fetched successfully"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response({"Message": "No categories found"}, status=status.HTTP_404_NOT_FOUND)

class SpecificCategoryView(GenericAPIView):
    serializer_class = ProductSerializer

    def get(self, request, category):
        # Filter products by category
        products = Product.objects.filter(category=category)
        
        # Check if products exist
        if products.exists():
            serializer = ProductSerializer(products, many=True)
            return Response(
                {"data": serializer.data, "Message": f"Products under {category} fetched successfully"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"Message": f"No products found under category {category}"},
                status=status.HTTP_404_NOT_FOUND,
            )
            
class UpdateProductView(GenericAPIView):
    serializer_class = ProductSerializer
    def put(self, request, id):
        title = request.data.get("title")
        description = request.data.get("description")
        price = request.data.get("price")
        category = request.data.get("category")
        image = request.data.get("image")
        
        products = Product.objects.filter(id=id).first()
        
        if products:
            
            product_data = {
                "title": title,
                "description": description,
                "price": price,
                "category": category,
                "image": image,
            }

            product_serializer = ProductSerializer(products, data=product_data, partial=True)
            
            if product_serializer.is_valid():
                product_serializer.save()
                return Response(
                    {"Message": "Update successful"}, status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"Message": "Invalid data", "Errors": product_serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response({"Message": f"No product with product id: {id} found"}, status=status.HTTP_404_NOT_FOUND)     
        
class DeleteProductView(GenericAPIView):
    serializer_class = ProductSerializer

    def delete(self, request, id):

        product = Product.objects.filter(id=id).first()

        if product:
            product.delete()
            return Response({"Message": "Delete successful"}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"Message": "No product"}, status=status.HTTP_400_BAD_REQUEST
            )   
        
        
        
    
