import glob
import fitz


# in_path = '../../backend/data/'
# out_path = '../../backend/data/Image-Output/'


def pdf_2_image(input_path, output_path):
    # To get better resolution
    zoom_x = 2.0  # horizontal zoom
    zoom_y = 2.0  # vertical zoom
    mat = fitz.Matrix(zoom_x, zoom_y)  # zoom factor 2 in each dimension
    all_files = glob.glob(input_path + "*.pdf")
    for filename in all_files:
        doc = fitz.open(filename)  # open document
        for page in doc:  # iterate through the pages
            pix = page.get_pixmap(matrix=mat)  # render page to an image
            pix.save(output_path + "page-%i.png" % page.number)   # store image as a PNG