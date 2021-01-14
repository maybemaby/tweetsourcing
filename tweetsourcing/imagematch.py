def reverse_image_search(uri):
    from google.cloud import vision

    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = uri

    response = client.web_detection(image=image)
    annotations = response.web_detection

    if annotations.pages_with_matching_images:
        print(
            "\n{} Pages with matching images found:".format(
                len(annotations.pages_with_matching_images)
            )
        )

        for page in annotations.pages_with_matching_images:
            print("\n\tPage url   : {}".format(page.url))

            if page.full_matching_images:
                print(
                    "\t{} Full Matches found: ".format(len(page.full_matching_images))
                )

                for image in page.full_matching_images:
                    print("\t\tImage url  : {}".format(image.url))

            if page.partial_matching_images:
                print(
                    "\t{} Partial matches found: ".format(
                        len(page.partial_matching_images)
                    )
                )

                for image in page.partial_matching_images:
                    print("\t\tImage url  : {}".format(image.url))

    if annotations.web_entities:
        print("\n{} Web entities found: ".format(len(annotations.web_entities)))

        for entity in annotations.web_entities:
            print("\n\tScore    : {}".format(entity.score))
            print("\tDescription: {}".format(entity.description))

    if response.error.message:
        raise Exception(f"Error message: {response.error.message}")

if __name__ == '__main__':
    reverse_image_search('https://pbs.twimg.com/media/ErnlSMlXUAMSTsu?format=jpg&name=large')