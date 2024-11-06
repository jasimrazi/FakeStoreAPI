from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializers import ProductSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import Product, ProductImage, Size
from django.conf import settings
import cloudinary   
import cloudinary.uploader
import cloudinary.api


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
        brand = request.data.get("brand")
        category = request.data.get("category")
        sizes = request.data.getlist("sizes")  # Expecting sizes as a list
        images = request.FILES.getlist("images")  # Expecting images as a list of files

        # Initial product data without images and sizes
        product_data = {
            "title": title,
            "description": description,
            "price": price,
            "brand": brand,
            "category": category,
        }
        
        print("Received Product Data:")
        print(f"Title: {title}")
        print(f"Description: {description}")
        print(f"Price: {price}")
        print(f"Brand: {brand}")
        print(f"Category: {category}")
        print(f"Sizes: {sizes}")
        print(f"Images: {images}")

        # Create product instance
        serializer = self.serializer_class(data=product_data)
        if serializer.is_valid():
            product = serializer.save()
            print("Product instance created:", product.title)

            # Handle sizes
            size_instances = []
            for size_name in sizes:
                print("Processing size:", size_name)
                size_instance, _ = Size.objects.get_or_create(size=size_name)
                size_instances.append(size_instance)

            # Assign sizes to product
            product.sizes.set(size_instances)
            print("Sizes set for product:", [size.size for size in size_instances])

            # Handle images
            image_urls = []
            for image in images:
                print("Processing image:", image)
                try:
                    upload_data = cloudinary.uploader.upload(image)
                    image_url = upload_data.get('url')
                    image_urls.append(image_url)
                    ProductImage.objects.create(product=product, image_url=image_url)
                    
                    # Log Cloudinary response for debugging
                    print("Cloudinary upload response:", upload_data)

                except Exception as e:
                    print("Cloudinary upload failed:", str(e))
                    return Response({'message': 'Cloudinary upload failed', 'success': 0}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            response_serializer = self.serializer_class(product)
            return Response({
                'data': response_serializer.data,
                'message': 'Product added successfully',
                'images': image_urls,
                'success': 1
            }, status=status.HTTP_201_CREATED)

        else:
            print("Validation failed:", serializer.errors)
            return Response({
                'data': serializer.errors,
                'message': 'Validation failed',
                'success': 0
            }, status=status.HTTP_400_BAD_REQUEST)


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
        
        
        
    
