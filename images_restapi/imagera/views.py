from rest_framework.views import APIView
from rest_framework.response import Response
from imagera import keyManager, imageManager
from django.http import FileResponse
from random import choice
from string import ascii_letters, digits

import os
storage = '/image_storage/'

class accessManager(APIView):
    """ 
    Access manager 
    """
    def get(self, request, format = None):
        key = keyManager.generateKeyCreateFolder()
        return Response(data={"Access key":key}, status=200)
    
    def patch(self, request, inputKey, format = None):
        if(keyManager.validateKey(inputKey) is False):
            ans = "Access key does not exist, Please register\n" + inputKey
            return Response(data={"Message":ans}, status=403)

        else:
            keyObj = keyManager.reGenerateKey(inputKey)
            
            if(keyObj[0] == "Error"):
                ans = "Access key does not exist, Please register\n" + keyObj[1]
                return Response(data={"Message":ans}, status=403)
            
            elif(keyObj[0] == "Success"):
                ans = "Access key regeneration successful\n" + keyObj[1]
                return Response(data={"Message":ans}, status=200)

class imageListManager(APIView):
    """
    Images list manager
    """
    def get(self, request, inputKey, format = None):
        if(keyManager.validateKey(inputKey) is False):
            ans = "Access key does not exist, Please register\n" + inputKey
            return Response(data={"Message":ans}, status=403)
        
        else:
            images_list = imageManager.getImageList(inputKey)

            if(images_list[0] == "Error"):
                ans = "Access key does not exist, Please register\n" + inputKey
                return Response(data={"Message":ans}, status=403)
            
            else:
                ans = "\n".join(images_list[1])
                return Response(data={"Image List: ":ans}, status=200)
    
    def post(self, request, inputKey, format = None):
        if(keyManager.validateKey(inputKey) is False):
            ans = "Access key does not exist, Please register\n" + inputKey
            return Response(data={"Message":ans}, status=403)
        
        else:
            image_file = request.data.get("file")

            if (image_file is not None):
                if(imageManager.validateImage(image_file.content_type)):
                    if(imageManager.storeImage(inputKey, image_file)):
                        ans = "Image uploaded successful"
                        return Response(data={"Message":ans}, status=201)

                    else:
                        ans = "File name already exist"
                        return Response(data={"Message":ans}, status=403)

                else:
                    ans = "File type not supported"
                    return Response(data={"Message":ans}, status=403)
            
            else:
                ans = "No input file was found"
                return Response(data={"Message":ans}, status=403)

class imageDetailManager(APIView):
    """
    Image detail manager
    """
    def get(self, request, inputKey, inputName, format = None):
        if(keyManager.validateKey(inputKey) is False):
            ans = "Access key does not exist, Please register\n" + inputKey
            return Response(data={"Message":ans}, status=403)
        
        else:
            temp = imageManager.getImagePath(inputKey, inputName)

            if(temp is not False):
                response = FileResponse(open(temp, 'rb'))
                return response
            
            else:
                ans = "No image was found with given name\n"
                return Response(data={"Message":ans}, status=403)
    
    def patch(self, request, inputKey, inputName, format = None):
        if(keyManager.validateKey(inputKey) is False):
            ans = "Access key does not exist, Please register\n" + inputKey
            return Response(data={"Message":ans}, status=403)
        
        else:
            image_file = request.data.get("file")

            if(image_file is not None):
                if(imageManager.validateImage(image_file.content_type)):
                    if(imageManager.updateImage(inputKey, inputName, image_file)):
                        ans = "Image update successful"
                        return Response(data={"Message":ans}, status=201)

                    else:
                        ans = "No image found with given name"
                        return Response(data={"Message":ans}, status=403)
                else:
                    ans = "File type not supported"
                    return Response(data={"Message":ans}, status=403)
            else:
                ans = "No input file was found"
                return Response(data={"Message":ans}, status=403)
    
    def delete(self,request, inputKey, inputName, format = None):
        if(keyManager.validateKey(inputKey) is False):
            ans = "Access key does not exist, Please register\n" + inputKey
            return Response(data={"Message":ans}, status=403)
        
        else:
            if(imageManager.deleteImage(inputKey, inputName)):
                ans = "Image deletec successfully"
                return Response(data={"Message":ans}, status=201)
            
            else:
                ans = "No image found with given name"
                return Response(data={"Message":ans}, status=403)