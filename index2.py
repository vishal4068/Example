import fitz

def is_table_like(rect, page):
    # Heuristic to identify if a rectangle is likely to represent a table
    # You may need to adjust these thresholds based on your specific documents
    width, height = rect.width, rect.height
    if width > 50 and height > 50 and width < 0.8 * height:
        # Check if the rectangle contains lines or grids (likely to be a table)
        x1, y1, x2, y2 = rect.x0, rect.y0, rect.x1, rect.y1
        for line in page.get_drawings():
            line_rect = fitz.Rect(line["rect"])
            if line_rect.intersects(rect):
                return True
    return False

def is_outer_rectangle(rect, all_rects):
    for other_rect in all_rects:
        if other_rect != rect and other_rect.contains(rect):
            return False
    return True

def mark_graphics_with_outer_red_rectangle(pdf_path, output_pdf_path):
    doc = fitz.open(pdf_path)
    
    for page in doc:
        all_rects = []
        images = page.get_images(full=True)
        for img_index, img in enumerate(images):
            xref = img[0]
            bbox = fitz.Rect(img[-1])
            all_rects.append(bbox)
        
        for drawing in page.get_drawings():
            bbox = fitz.Rect(drawing["rect"])
            if not is_table_like(bbox, page):
                all_rects.append(bbox)
        
        for rect in all_rects:
            if is_outer_rectangle(rect, all_rects):
                page.draw_rect(rect, color=(1, 0, 0), width=2)
    
    doc.save(output_pdf_path)
    doc.close()

# Input PDF path
pdf_path = 'vishal.pdf'
output_pdf_path = 'marked_vishal.pdf'

# Mark outer rectangles around images and vector graphics (excluding tables) with red rectangle in the PDF
mark_graphics_with_outer_red_rectangle(pdf_path, output_pdf_path)

print("Outer rectangles around images and vector graphics (excluding tables) marked with red rectangles successfully in the output PDF.")
