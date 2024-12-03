from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
from PIL import Image, ImageDraw

# Set up your Azure credentials and endpoint
subscription_key = "F9n0lQA5sPQKOUNk9yj89Mej20jteMXZNgiz7KuL2mYXZQpfI2cNJQQJ99ALACYeBjFXJ3w3AAAFACOGXK6R"
endpoint = "https://maxcomcomputervisionservice.cognitiveservices.azure.com/"

# Authenticate the client
computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))


def analyze_image(image_path):
    """
    Analyze an image and return a detailed description and additional data.
    """
    with open(image_path, "rb") as image_stream:
        analysis = computervision_client.analyze_image_in_stream(
            image_stream,
            visual_features=[
                VisualFeatureTypes.description,
                VisualFeatureTypes.tags,
                VisualFeatureTypes.objects,
                VisualFeatureTypes.color,
                VisualFeatureTypes.categories,
                VisualFeatureTypes.adult,
                VisualFeatureTypes.faces
            ]
        )

    description = (
        analysis.description.captions[0].text
        if analysis.description.captions
        else "No description available"
    )

    tags = [tag.name for tag in analysis.tags]

    objects = [
        {"name": obj.object_property, "confidence": obj.confidence, "rectangle": obj.rectangle}
        for obj in analysis.objects
    ]

    dominant_colors = analysis.color.dominant_colors

    categories = [{"name": cat.name, "score": cat.score} for cat in analysis.categories]

    adult_content = {
        "is_adult_content": analysis.adult.is_adult_content,
        "is_racy_content": analysis.adult.is_racy_content,
        "is_gory_content": analysis.adult.is_gory_content,
    }

    faces = [
        {
            "age": face.age,
            "gender": face.gender
        }
        for face in analysis.faces
    ]

    # Print results
    print("Description:", description)
    print("Tags:", tags)
    print("Objects:", objects)
    print("Dominant Colors:", dominant_colors)
    print("Categories:", categories)
    print("Adult Content:", adult_content)
    print("Faces:", faces)

    return {
        "description": description,
        "tags": tags,
        "objects": objects,
        "dominant_colors": dominant_colors,
        "categories": categories,
        "adult_content": adult_content,
        "faces": faces,
    }


image_path = "i.jpg"
results = analyze_image(image_path)


def draw_objects(image_path, objects):
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    for obj in objects:
        rect = obj["rectangle"]
        draw.rectangle(
            [(rect.x, rect.y), (rect.x + rect.w, rect.y + rect.h)],
            outline="red",
            width=2
        )
        draw.text((rect.x, rect.y - 10), f'{obj["name"]} ({obj["confidence"]:.2f})', fill="red")

    image.show()


if results["objects"]:
    draw_objects(image_path, results["objects"])
