from pathlib import Path


def register_image(screen):
    # Register the GIF image
    images_name = [ "end-knot.gif", 
                "grid.gif", 
                "top-cord.gif", 
                "top-grid.gif", 
                "primary-cord.gif", 
                "pendant-cord.gif", 
                "long-knot-1.gif", 
                "long-knot-2.gif", 
                "long-knot-3.gif", 
                "long-knot-4.gif", 
                "long-knot-5.gif", 
                "long-knot-6.gif", 
                "long-knot-7.gif", 
                "long-knot-8.gif", 
                "long-knot-9.gif", 
                "overhand-knot-1.gif", 
                "overhand-knot-2.gif", 
                "overhand-knot-3.gif", 
                "overhand-knot-4.gif", 
                "overhand-knot-5.gif", 
                "overhand-knot-6.gif", 
                "overhand-knot-7.gif", 
                "overhand-knot-8.gif", 
                "overhand-knot-9.gif", 
                "top-long-knot-1.gif", 
                "top-long-knot-2.gif", 
                "top-long-knot-3.gif", 
                "top-long-knot-4.gif", 
                "top-long-knot-5.gif", 
                "top-long-knot-6.gif", 
                "top-long-knot-7.gif", 
                "top-long-knot-8.gif", 
                "top-long-knot-9.gif", 
                "top-overhand-knot-1.gif", 
                "top-overhand-knot-2.gif", 
                "top-overhand-knot-3.gif", 
                "top-overhand-knot-4.gif", 
                "top-overhand-knot-5.gif", 
                "top-overhand-knot-6.gif", 
                "top-overhand-knot-7.gif", 
                "top-overhand-knot-8.gif", 
                "top-overhand-knot-9.gif"]

    for image_name in images_name:
        path = get_image_path(image_name)
        screen.addshape(path)    


def get_image_path(image_name):
    base_path = Path(__file__).parent
    image_path = base_path /  "../assets" / image_name
    return str(image_path)
