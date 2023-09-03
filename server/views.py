from io import BytesIO
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from fastai.basic_train import load_learner
import requests
from fastai.vision import open_image
import openai
import os
from dotenv import load_dotenv
import base64


@csrf_exempt
def ResolveProductCategory(request):
    if request.method == "POST":
        if request.FILES.get("image"):
            image = request.FILES["image"]
            response_data = fetch_response_from_model(image)
            return JsonResponse(response_data, status=200)
        elif request.POST.get("search"):
            url = generate_image(request.POST["search"])
            response = requests.get(url)
            image = BytesIO(response.content)
            image.seek(0)
            image_data = image.read()
            base64_data = base64.b64encode(image_data).decode("utf-8")
            response_data = fetch_response_from_model(image)
            response_data.update(base64_data=base64_data)
            return JsonResponse(response_data, status=200)

    else:
        response_data = {"status": "error", "message": "Invalid request method"}
        return JsonResponse(response_data, status=400)


def generate_image(text):
    load_dotenv()
    API_KEY = os.getenv("API_KEY") or os.environ.get("API_KEY")
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
