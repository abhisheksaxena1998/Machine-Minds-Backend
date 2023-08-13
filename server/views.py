from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from fastai.basic_train import load_learner
from fastai.vision import *


@csrf_exempt
def ResolveProductCategory(request):
    if request.method == "POST":
        image = request.FILES["image"]
        loaded_model = load_learner(
            path="server/", file="product_category_predictor.h5"
        )
        img = open_image(image)
        pred_class, _, _ = loaded_model.predict(img)
        response_data = {"status": "success", "category": str(pred_class)}
        return JsonResponse(response_data)
    else:
        response_data = {"status": "error", "message": "Invalid request method"}
        return JsonResponse(response_data, status=400)
