from models.image import ImageModel
from services.moby_dick_docker import docker_client


def retrieve_images():
    images = []
    for image in docker_client.images.list():
        img = ImageModel()
        img.id = clean_id(image.id)
        img.tag = retrieve_tags(image.tags)
        img.date = extract_date(image.attrs)
        images.append(img.to_json())

    return images


def create_image(request):
    if (request['uri'] and request['tag']):
        new_image = docker_client.images.build(path=request['uri'], tag=request['tag'])
        return {"created": "OK", "new_image": str(new_image[0])}
    return {"error": "Server error", "details": "You need to send both dockerfile uri and tag"}


def delete_image(tags):
    docker_client.images.remove(retrieve_image_to_delete(tags))
    return {"created": "OK"}


### Helpers ###

def identify_status_code(image):
    if 'created' in image:
        return 200
    return 500


def retrieve_image_to_delete(tags):
    image_tags = tags.split(":")
    return image_tags[0]


# Method to return fist tag if more than one exist
def retrieve_tags(tags):
    return tags[0] if len(tags) > 1 else tags


# Method to simple remove "SHA:" before the image ids and return the second part.
def clean_id(id):
    final_id = id.split(":")
    return final_id[1]


# Method to remove milis from created date
def extract_date(attributes):
    date = attributes['Created'].split(".")
    return date[0]