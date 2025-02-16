import io
from .serializers import UserSerializer
from .models import UserData
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import mimetypes
from rest_framework.parsers import MultiPartParser, FormParser
import csv

def csv_to_dict(line: list, header: dict):
    line = line.split(",")
    data = {
        "name": line[header["name"]],
        "email": line[header["email"]],
        "age": line[header["age"]],
    }
    return data


def validate_extention(file):
    extention = mimetypes.guess_extension(file.content_type)
    if extention != ".csv":
        return False
    return True


class UserView(APIView):

    def get(self, request):
        user_data = UserData.objects.all()
        serializer = UserSerializer(user_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request):
        """
        Parses the input 'csv' file and saves the valid data in database.
        """
        file = request.FILES.get("user_data")

        if not file:  # if file is missing return status code 400.
            return Response(
                {"message": "Input file missing!"}, status=status.HTTP_400_BAD_REQUEST
            )
        if not validate_extention(file):  # if file extention is not .csv, returns status code 400.
            return Response(
                {"message": "Invalid file format!"}, status=status.HTTP_400_BAD_REQUEST
            )

        file_data = file.read().decode('utf-8')
        csv_data = io.StringIO(file_data)  # convert string to file object.
        reader = csv.DictReader(csv_data)  # parses the csv data to dicts.
        user_data = [row for row in reader]  # converts the DictReader object to list of dicts.
        user_data_log = {
            "data": [],
            "rejected": 0,
            "success": 0,
            "total": len(user_data),  # total number of input data.
        }

        for data in user_data:
            serializer = UserSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                data["status"] = "created"
                user_data_log["success"] += 1
            else:
                error = serializer.errors
                data["status"] = {"errors": error}
                user_data_log["rejected"] += 1
            user_data_log["data"].append(data)
        return Response(user_data_log, status=status.HTTP_200_OK)
