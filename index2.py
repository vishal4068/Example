import fitz  # PyMuPDF
import cv2
import numpy as np

def draw_red_borders_around_images_in_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)  # Use load_page for better performance
        image_list = page.get_images(full=True)
        
        for img_index, img_info in enumerate(image_list):
            # img_info format: [xref, smask, width, height, bpc, colorspace, alt. colorspace, name]
            # The image's rectangle can be obtained with page.get_image_rects(xref)
            img_rects = page.get_image_rects(img_info[0])
            for rect in img_rects:
                # Draw a red border around the image rect
                # Note: The border width is set to 3. Adjust as needed.
                page.draw_rect(rect, color=(1, 0, 0), width=3, overlay=True)
    
    # Save the modified PDF
    new_pdf_path = pdf_path.replace('.pdf', '_with_red_borders.pdf')
    doc.save(new_pdf_path)
    doc.close()
    return new_pdf_path

if __name__ == "__main__":
    pdf_path = "output.pdf"  # Change this to your PDF file path
    new_pdf_path = draw_red_borders_around_images_in_pdf(pdf_path)
    print(f"Modified PDF saved as: {new_pdf_path}")

# import fitz  # PyMuPDF
# import cv2
# import numpy as np

# def convert_pdf_page_to_image(pdf_path, page_number, zoom=2):
#     doc = fitz.open(pdf_path)
#     page = doc.load_page(page_number)
#     pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
#     img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n)
#     doc.close()
#     return img

# def detect_charts_in_image(image):
#     # This is a placeholder for the actual chart detection logic.
#     # You might use edge detection, contour finding, and shape analysis
#     # to attempt to identify charts. This will vary greatly depending on
#     # the types of charts and their complexity.
#     # For demonstration, let's apply a simple edge detection:
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     edges = cv2.Canny(gray, 50, 150, apertureSize=3)
#     return edges

# if __name__ == "__main__":
#     pdf_path = "graphics.pdf"
#     page_number = 0  # Example: looking at the first page

#     # Convert a PDF page to an image
#     img = convert_pdf_page_to_image(pdf_path, page_number)

#     # Attempt to detect charts in the converted image
#     detected_charts = detect_charts_in_image(img)

#     # Display the result
#     cv2.imshow("Detected Charts", detected_charts)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

