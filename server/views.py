from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
import random
import openai
import requests
from django.conf import settings
openai.api_key = settings.OPEN_AI_KEY
import matplotlib.pyplot as plt
from io import BytesIO
from django.http import HttpResponse, FileResponse

def generate(text):
    res = openai.Image.create(
    	prompt=text,
    	n=1,
    	size="256x256",
    )
    return res["data"][0]["url"]

def ResolveProductCategory(request):
    if request.method == "POST":
        image = request.FILES["image"]
        image = Image.open(image)
        #!TODO: Implement logic for fetching product category from model
        response_list = [
            "Water Bottle",
            "Home Furnishing",
            "Accessories",
        ]
        response_data = {"status": "success", "category": random.choice(response_list)}
        return JsonResponse(response_data)
    else:
        text = "batman with green arrow"
        url = generate(text)
        response = requests.get(url)
        raw_image = BytesIO(response.content)
        image = Image.open(BytesIO(response.content))
        return FileResponse(raw_image, as_attachment=True, filename='output.png')