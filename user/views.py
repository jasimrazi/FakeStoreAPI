from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializers import RegisterSerializer, LoginSerializer, MerchantRegisterSerializer
from .models import Register, Login, MerchantRegister
from rest_framework.response import Response
from rest_framework import status




# Create your views here.
class AddUserView(GenericAPIView):
    def get_serializer_class(self):
        return RegisterSerializer

    def post(self, request):
        name = request.data.get("name")
        email = request.data.get("email")
        number = request.data.get("number")
        password = request.data.get("password")
        role = "user"  # Hardcoded to "user"

        # Step 1: Validate registration fields first
        if not name or not email or not number or not password:
            return Response(
                {"Message": "All fields (name, email, number, password) are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Step 2: Check for duplicate email and number
        if Register.objects.filter(email=email).exists():
            return Response(
                {"Message": "Duplicate email found"}, status=status.HTTP_400_BAD_REQUEST
            )

        elif Register.objects.filter(number=number).exists():
            return Response(
                {"Message": "Duplicate number found"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Step 3: Create the Login entry
        login_serializer = LoginSerializer(data={"email": email, "password": password, "role": role})
        
        if login_serializer.is_valid():
            login_instance = login_serializer.save()
            loginid = login_instance.loginid  # Save the UUID as loginid__loginid for Register
        else:
            return Response(
                {"Message": "Login failed", "Errors": login_serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Step 4: Create Register with login instance
        register_serializer = RegisterSerializer(
            data={
                "email": email,
                "password": password,
                "role": role,
                "name": name,
                "number": number,
                "loginid": login_instance.id,  # Pass the actual login instance
            }
        )

        if register_serializer.is_valid():
            register_instance = register_serializer.save()
            return Response(
                {
                    "Message": "User account registered successfully",
                    "data": {
                        "name": register_instance.name,
                        "loginid": str(login_instance.loginid),  # Convert loginid__loginid to string
                    },
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "Message": "Registration failed",
                    "Errors": register_serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )



class AddMerchantView(GenericAPIView):
    def get_serializer_class(self):
        # Return the MerchantRegisterSerializer for merchant registration
        return MerchantRegisterSerializer

    def post(self, request):
        # Retrieve the input fields from the request
        loginid = ""
        name = request.data.get("name")
        email = request.data.get("email")
        number = request.data.get("number")
        password = request.data.get("password")
        store_name = request.data.get("store_name")
        business_license = request.data.get("business_license")
        role = "merchant"  # Hardcoded to "merchant"

        # Step 1: Validate registration fields first
        if not name or not email or not number or not password or not store_name or not business_license:
            return Response(
                {"Message": "All fields (name, email, number, password, store_name, business_license) are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Step 2: Check for duplicate email and number
        if MerchantRegister.objects.filter(email=email).exists():
            return Response(
                {"Message": "Duplicate email found"}, status=status.HTTP_400_BAD_REQUEST
            )

        elif MerchantRegister.objects.filter(number=number).exists():
            return Response(
                {"Message": "Duplicate number found"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Step 3: Validate and create login
        login_serializer = LoginSerializer(
            data={"email": email, "password": password, "role": role}
        )

        if login_serializer.is_valid():
            l = login_serializer.save()
            loginid = l.id  # Store the login ID for merchant registration
        else:
            return Response(
                {"Message": "Login failed", "Errors": login_serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Step 4: Handle merchant registration with the validated login id
        merchant_serializer = MerchantRegisterSerializer(
            data={
                "email": email,
                "password": password,
                "role": role,  # Hardcoded to "merchant"
                "name": name,
                "number": number,
                "store_name": store_name,
                "business_license": business_license,
                "loginid": loginid,
            }
        )

        if merchant_serializer.is_valid():
            merchant_serializer.save()
            return Response(
                {"Message": "Merchant account registered successfully"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "Message": "Registration failed",
                    "Errors": merchant_serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

            
class LoginUserView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        email = request.data.get("email", "").strip()
        password = request.data.get("password", "").strip()

        # Check if email or password is empty
        if not email or not password:
            return Response(
                {"Message": "Email and password fields cannot be empty."},
                status=status.HTTP_400_BAD_REQUEST,
            )


        # Check for the user in the Login model
        user = Login.objects.filter(email=email, password=password).first()

        if user is None:
            return Response(
                {"Message": "Incorrect email or password."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # If user is found, get the loginid and role
        loginid = user.loginid  # Get the loginid from the Login model
        role = user.role  # Get the role from the Login model
        name = user.register.name

        print(f"Login successful for email: {email}, loginid: {loginid}, role: {role}")  # Debugging line

        # Return a successful response with user details
        return Response(
            {
                "data": {
                    "loginid": str(loginid),  # Ensure loginid is serialized as a string
                    "role": role,
                    "email": email,
                    "name": name,
                }
            },
            status=status.HTTP_200_OK,
        )




        
class GetAllUserView(GenericAPIView):
    serializer_class = RegisterSerializer

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
            users = Register.objects.all().order_by('-id')  # Sort by descending order if 'desc'
        else:
            users = Register.objects.all().order_by('id')  # Default to ascending order if not 'desc'

        # Apply limit to the queryset
        users = users[:limit]

        # Check if there are any users
        if users.exists():
            # Serialize the users queryset
            serializer = RegisterSerializer(users, many=True)
            return Response(
                {"data": serializer.data, "Message": "Fetch successful"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response({"Message": "No data"}, status=status.HTTP_400_BAD_REQUEST)


class UserIDView(GenericAPIView):
    serializer_class = RegisterSerializer

    def get(self, request, id):
        a = Register.objects.filter(id=id)

        if a.exists():
            b = RegisterSerializer(a, many=True)
            return Response(
                {"data": b.data, "Message": "Fetch successful"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"Message": "No user found"}, status=status.HTTP_404_NOT_FOUND
            )
            
class UpdateUserView(GenericAPIView):
    serializer_class = RegisterSerializer

    def put(self, request, id):
        name = request.data.get("name")
        email = request.data.get("email")
        number = request.data.get("number")
        password = request.data.get("password")
        loginid = request.data.get("loginid")

        # Fetch the Register object based on loginid
        user = Register.objects.filter(id=id).first()

        # Check if user exists
        if user:
            # Create a dictionary of the new data
            updated_data = {
                "name": name,
                "email": email,
                "number": number,
                "password": password,
                # "loginid": loginid,
            }

            # Pass the existing instance and updated data to the serializer
            serializer = RegisterSerializer(user, data=updated_data, partial=True)

            # Validate and update the user data
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"Message": "Update successful"}, status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"Message": "Invalid data", "Errors": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        # Return error if user doesn't exist
        return Response({"Message": "No user found"}, status=status.HTTP_404_NOT_FOUND)
    
class DeleteUserView(GenericAPIView):
    serializer_class = RegisterSerializer

    def delete(self, request,id):

        user = Register.objects.filter(id=id).first()

        if user:
            user.delete()
            return Response({"Message": "Delete succesful"}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"Message": "No user"}, status=status.HTTP_400_BAD_REQUEST
            )


            
