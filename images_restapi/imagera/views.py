from django.http import HttpResponse
from imagera import key_manager, image_manager
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from random import choice
from string import ascii_letters, digits

storage = os.getcwd() + '/image_storage/'


def key_validator(fn):
    """
    Decorator function to handle access key validation
    """
    def wrapper(param1, request, format=None):
        if(request.method == "GET"):
            inputkey = request.GET['key']
        else:
            inputkey = request.POST['key']

        try:
            key_manager.validate_key(inputkey)
        except FileNotFoundError:
            ans = "Access key does not exist, Please register !"
            return Response(data={"Message": ans, "Key": inputkey},
                            status=403, content_type="application/json")
        else:
            return fn(param1, request, format=None)
    return wrapper


class GenerateKey(APIView):
    """
    Class to generate access key
    """
    def get(self, request, format=None):
        key = key_manager.generate_key_create_folder()
        ans = "Access key generation successful !"
        return Response(data={"Message": ans, "Key": key},
                        status=200, content_type="application/json")


class ChangeKey(APIView):
    """
    Class to regenerate access key
    """
    @key_validator
    def post(self, request, format=None):
        inputkey = request.POST['key']
        key = key_manager.regenerate_key(inputkey)
        ans = "Access key regeneration successful !"
        return Response(data={"Message": ans, "Key": key},
                        status=200, content_type="application/json")


class ImageListManager(APIView):
    """
    Images list manager
    """
    @key_validator
    def get(self, request, format=None):
        inputkey = request.GET['key']
        images_list = image_manager.get_image_list(inputkey)
        ans = ", ".join(images_list)
        return Response(data={"Images": ans}, status=200,
                        content_type="application/json")

    @key_validator
    def post(self, request, format=None):
        inputkey = request.POST['key']
        image_file = request.data.get("file")

        if (image_file is not None):
            try:
                image_manager.validate_image(image_file.content_type)
            except TypeError:
                ans = "File type not supported"
                return Response(data={"Message": ans}, status=403,
                                content_type="application/json")
            else:
                try:
                    image_manager.store_image(inputkey, image_file)
                except FileExistsError:
                    ans = "File name already exist"
                    return Response(data={"Message": ans}, status=403,
                                    content_type="application/json")
                else:
                    ans = "Image uploaded successfully"
                    return Response(data={"Message": ans}, status=201,
                                    content_type="application/json")
        else:
            ans = "No input file was uploaded"
            return Response(data={"Message": ans}, status=403,
                            content_type="application/json")


class ImageDetailManager(APIView):
    """
    Image detail manager
    """
    @key_validator
    def get(self, request, format=None):
        inputkey = request.GET['key']
        inputname = request.GET['name']

        try:
            temp = image_manager.get_image_path(inputkey, inputname)
        except FileNotFoundError:
            ans = "No image was found with given name"
            return Response(data={"Message": ans}, status=403,
                            content_type="application/json")
        else:
            with open(temp, 'rb') as f:
                return HttpResponse(f.read(), content_type="image/jpeg")

    @key_validator
    def patch(self, request, format=None):
        inputkey = request.POST['key']
        inputname = request.POST['name']
        image_file = request.data.get("file")

        if(image_file is not None):
            try:
                image_manager.validate_image(image_file.content_type)
            except TypeError:
                ans = "File type not supported"
                return Response(data={"Message": ans}, status=403,
                                content_type="application/json")
            else:
                try:
                    image_manager.update_image(
                            inputkey, inputname, image_file)
                except FileNotFoundError:
                    ans = "No image found with given name"
                    return Response(data={"Message": ans}, status=403,
                                    content_type="application/json")
                else:
                    ans = "Image updated successfully"
                    return Response(data={"Message": ans}, status=201,
                                    content_type="application/json")

        else:
            ans = "No input file was uploaded"
            return Response(data={"Message": ans}, status=403,
                            content_type="application/json")

    @key_validator
    def delete(self, request, format=None):
        inputkey = request.POST['key']
        inputname = request.POST['name']

        try:
            image_manager.delete_image(inputkey, inputname)
        except FileNotFoundError:
            ans = "No image found with given name"
            return Response(data={"Message": ans}, status=403,
                            content_type="application/json")
        else:
            ans = "Image deleted successfully"
            return Response(data={"Message": ans},
                            status=201, content_type="application/json")
