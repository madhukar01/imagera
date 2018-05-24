from django.http import HttpResponse
from imagera import key_manager, image_manager
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from random import choice
from string import ascii_letters, digits

storage = os.getcwd() + '/image_storage/'


class GenerateKey(APIView):
    """
    Class to generate access key
    """
    def get(self, request, format=None):
        key = key_manager.generate_key_create_folder()
        ans = "Access key generation successful !"
        return Response(data={"Message": ans, "Access key": key}, status=200)


class ChangeKey(APIView):
    """
    Class to regenerate access key
    """
    def get(self, request, format=None):
        inputkey = request.GET['key']
        if(key_manager.validate_key(inputkey) is False):
            ans = "Access key does not exist, Please register !"
            return Response(data={"Message": ans, "Access key": inputkey},
                            status=403)

        else:
            keyObj = key_manager.regenerate_key(inputkey)

            if(keyObj[0] == "Error"):
                ans = "Access key does not exist, Please register !"
                return Response(data={"Message": ans, "Access key": inputkey},
                                status=403)

            elif(keyObj[0] == "Success"):
                ans = "Access key regeneration successful !"
                return Response(data={"Message": ans,
                                "New access key": keyObj[1]},
                                status=200, content_type="text/html")


class ImageListManager(APIView):
    """
    Images list manager
    """
    def get(self, request, format=None):
        inputkey = request.GET['key']
        if(key_manager.validate_key(inputkey) is False):
            ans = "Access key does not exist, Please register !"
            return Response(data={"Message": ans, "Access key": inputkey},
                            status=403)

        else:
            images_list = image_manager.get_image_list(inputkey)

            if(images_list[0] == "Error"):
                ans = "Access key does not exist, Please register !"
                return Response(data={"Message": ans, "Access key": inputkey},
                                status=403)

            else:
                ans = ", ".join(images_list[1])
                return Response(data={"Image List": ans}, status=200)

    def post(self, request, format=None):
        inputkey = request.GET['key']
        if(key_manager.validate_key(inputkey) is False):
            ans = "Access key does not exist, Please register !"
            return Response(data={"Message": ans, "Access key": inputkey},
                            status=403)

        else:
            image_file = request.data.get("file")

            if (image_file is not None):
                if(image_manager.validate_image(image_file.content_type)):
                    if(image_manager.store_image(inputkey, image_file)):
                        ans = "Image uploaded successful"
                        return Response(data={"Message": ans}, status=201)

                    else:
                        ans = "File name already exist"
                        return Response(data={"Message": ans}, status=403)

                else:
                    ans = "File type not supported"
                    return Response(data={"Message": ans}, status=403)

            else:
                ans = "No input file was found"
                return Response(data={"Message": ans}, status=403)


class ImageDetailManager(APIView):
    """
    Image detail manager
    """
    def get(self, request, format=None):
        inputkey = request.GET['key']
        inputname = request.GET['name']
        if(key_manager.validate_key(inputkey) is False):
            ans = "Access key does not exist, Please register !"
            return Response(data={"Message": ans, "Access key": inputkey},
                            status=403)

        else:
            temp = image_manager.get_image_path(inputkey, inputname)

            if(temp is not False):
                with open(temp, 'rb') as f:
                    return HttpResponse(f.read(), content_type="image/jpeg")

            else:
                ans = "No image was found with given name"
                return Response(data={"Message": ans}, status=403)

    def patch(self, request, format=None):
        inputkey = request.GET['key']
        inputname = request.GET['name']
        if(key_manager.validate_key(inputkey) is False):
            ans = "Access key does not exist, Please register !"
            return Response(data={"Message": ans, "Access key": inputkey},
                            status=403)

        else:
            image_file = request.data.get("file")

            if(image_file is not None):
                if(image_manager.validate_image(image_file.content_type)):
                    if(image_manager.update_image(
                            inputkey, inputname, image_file)):
                        ans = "Image update successful"
                        return Response(data={"Message": ans}, status=201)

                    else:
                        ans = "No image found with given name"
                        return Response(data={"Message": ans}, status=403)
                else:
                    ans = "File type not supported"
                    return Response(data={"Message": ans}, status=403)
            else:
                ans = "No input file was found"
                return Response(data={"Message": ans}, status=403)

    def delete(self, request, format=None):
        inputkey = request.GET['key']
        inputname = request.GET['name']
        if(key_manager.validate_key(inputkey) is False):
            ans = "Access key does not exist, Please register !"
            return Response(data={"Message": ans, "Access key": inputkey},
                            status=403)

        else:
            if(image_manager.delete_image(inputkey, inputname)):
                ans = "Image deleted successfully"
                return Response(data={"Message": ans}, status=201)

            else:
                ans = "No image found with given name"
                return Response(data={"Message": ans}, status=403)
