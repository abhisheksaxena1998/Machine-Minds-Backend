from io import BytesIO
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from fastai.basic_train import load_learner
import requests
from fastai.vision import open_image
import openai
import os
from dotenv import load_dotenv


@csrf_exempt
def ResolveProductCategory(request):
    if request.method == "POST":
        if bool(request.FILES):
            image = request.FILES["image"]
            response_data = fetch_response_from_model(image)
            return JsonResponse(response_data, status=200)
        else:
            url = generate_image(request.POST["text_description"])
            response = requests.get(url)
            image = BytesIO(response.content)
            response_data = fetch_response_from_model(image)
            return JsonResponse(response_data, status=200)

    else:
        response_data = {"status": "error", "message": "Invalid request method"}
        return JsonResponse(response_data, status=400)


def generate_image(text):
    load_dotenv()
    API_KEY = os.getenv("API_KEY")
    openai.api_key = API_KEY
    res = openai.Image.create(
        prompt=text,
        n=1,
        size="256x256",
    )
    return res["data"][0]["url"]


def fetch_response_from_model(image):
    loaded_model = load_learner(path="server/", file="product_category_predictor.h5")
    img = open_image(image)
    pred_class, _, _ = loaded_model.predict(img)
    response_data = {"status": "success", "category": str(pred_class)}
    return response_data
