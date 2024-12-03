import requests
from PIL import Image, ImageDraw, ImageFont

url = "https://maxcomazureaiservicestest.cognitiveservices.azure.com/customvision/v3.0/Prediction/5c23ffe5-d661-4fa4-be71-6dfbf4c04aac/detect/iterations/Iteration1/image"
prediction_key = "EWlQowRIBJZSAqg4Ayd3C5cX8c92s7gYeVpyUXjBdeQ1AkZUAnnmJQQJ99ALACYeBjFXJ3w3AAAEACOGajUF"
image_path = "a.jpg"

with open(image_path, "rb") as image_file:
    image_data = image_file.read()

headers = {
    "Prediction-Key": prediction_key,
    "Content-Type": "application/octet-stream"
}

response = requests.post(url, headers=headers, data=image_data)

if response.status_code == 200:
    predictions = response.json()["predictions"]
    print("Prediction result:")
    print(predictions)

    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    for prediction in predictions:
        probability = prediction["probability"]
        tag_name = prediction["tagName"]
        bounding_box = prediction["boundingBox"]
        tagId = prediction["tagId"]

        if probability > 0.95:
            left = bounding_box["left"] * image.width
            top = bounding_box["top"] * image.height
            width = bounding_box["width"] * image.width
            height = bounding_box["height"] * image.height
            right = left + width
            bottom = top + height

            draw.rectangle([left, top, right, bottom], outline="red", width=3)

            label = f"{tag_name}: {probability:.2%} ({tagId})"
            draw.text((left, top - 10), label, fill="red")

    image.show()

else:
    print(f"Error: {response.status_code}")
    print(response.text)
