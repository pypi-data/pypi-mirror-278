import os
from PIL import Image
#========================================================================

class Thumbnail:

    def get01(flocation):
        image = Image.open(flocation)
        image = image if image.mode == "RGB" else image.convert("RGB")
        moonus = os.path.splitext(flocation)[0] + ".jpg"
        image.save(moonus, "JPEG")
        os.remove(flocation)
        return moonus

#========================================================================
