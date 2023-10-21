import cv2

def resize_image(image, width=None, height=None):
    """
    Resize the input image to the specified width and height.

    Args:
        image (numpy.ndarray): The input image as a NumPy array.
        width (int, optional): The target width of the image.
        height (int, optional): The target height of the image.

    Returns:
        numpy.ndarray: The resized image.
    """
    if width is None and height is None:
        return image  # No resizing needed

    if width is None:
        aspect_ratio = height / float(image.shape[0])
        new_width = int(image.shape[1] * aspect_ratio)
        dim = (new_width, height)
    else:
        aspect_ratio = width / float(image.shape[1])
        new_height = int(image.shape[0] * aspect_ratio)
        dim = (width, new_height)

    # Resize the image using OpenCV
    resized_image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    return resized_image
