from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
import random


@csrf_exempt
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
        response_data = {"status": "error", "message": "Invalid request method"}
        return JsonResponse(response_data, status=400)
