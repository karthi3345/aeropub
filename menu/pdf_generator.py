import os
import fitz  # PyMuPDF
from menu.models import MenuItem, RestaurantSettings

PDF_SOURCE = r'C:\Users\Karthik_Raja\Downloads\Menu card - Final version.pdf'
OUTPUT_DIR = r'd:\skybliss_menu\static\menu_pages'
NIRMALA_FONT = r'C:\Windows\Fonts\Nirmala.ttc'
CALIBRI_BOLD = r'C:\Windows\Fonts\calibrib.ttf'

def render_dynamic_pdf_pages():
    """
    Renders the exact 12-page PDF menu.
    Preserves 100% of the authentic background photography and design without any dark boxes.
    - Page 10 (Starters): The original Rupee symbol (₹) is completely preserved untouched,
      and updated prices use the authentic Calibri-Bold font matching the PDF design perfectly.
    - Page 8 & 9 (Spirits & Whisky): Text-only redaction with crisp pure white typography (#FFFFFF)
      and original baseline alignment.
    """
    if not os.path.exists(PDF_SOURCE):
        return

    items = {item.code: item for item in MenuItem.objects.all() if item.code}
    name_items = {item.name.lower().strip(): item for item in MenuItem.objects.all()}

    doc = fitz.open(PDF_SOURCE)

    for pno in range(len(doc)):
        page = doc[pno]

        # Page 8: Spirits (Brandy, Gin, Liqueur, Rum, Tequila, Vodka)
        if pno == 7:
            for block in page.get_text('dict')['blocks']:
                if 'lines' in block:
                    for line in block['lines']:
                        for span in line['spans']:
                            if span['bbox'][0] > 290 and any(c.isdigit() for c in span['text']):
                                pad = 1.0
                                rect = fitz.Rect(span['bbox'][0] - pad, span['bbox'][1] - pad, span['bbox'][2] + pad + 15, span['bbox'][3] + pad)
                                page.add_redact_annot(rect)
            
            page.apply_redactions(images=0)

            words = page.get_text('words')
            for code, item in items.items():
                if code.startswith(('B', 'G', 'L', 'R', 'T', 'V')) and not code.startswith(('BE', 'TC', 'VC', 'RC')):
                    code_matches = [w for w in words if w[4] == code and w[0] < 140]
                    if code_matches:
                        cw = code_matches[0]
                        price_num = int(item.price) if item.price % 1 == 0 else item.price
                        has_space = code.startswith('B')
                        new_text = f"\u20b9 {price_num}" if has_space else f"\u20b9{price_num}"
                        origin_x = 307.9 if has_space else 309.5
                        origin_y = cw[3] - 2.5
                        page.insert_text(
                            (origin_x, origin_y), 
                            new_text, 
                            fontname='nirmala_bold', 
                            fontfile=NIRMALA_FONT, 
                            fontsize=12.0, 
                            color=(1, 1, 1)
                        )

        # Page 9: Whisky Collections
        elif pno == 8:
            for block in page.get_text('dict')['blocks']:
                if 'lines' in block:
                    for line in block['lines']:
                        for span in line['spans']:
                            if span['bbox'][0] > 350 and any(c.isdigit() for c in span['text']):
                                pad = 1.0
                                rect = fitz.Rect(span['bbox'][0] - pad, span['bbox'][1] - pad, span['bbox'][2] + pad + 20, span['bbox'][3] + pad)
                                page.add_redact_annot(rect)

            page.apply_redactions(images=0)

            words = page.get_text('words')
            for code, item in items.items():
                if code.startswith('W') and not code.startswith(('WI', 'WN')):
                    code_matches = [w for w in words if w[4] == code and w[0] < 200]
                    if code_matches:
                        cw = code_matches[0]
                        price_num = int(item.price) if item.price % 1 == 0 else item.price
                        new_text = f"\u20b9{price_num}"
                        origin_x = 367.66
                        origin_y = cw[3] - 2.5
                        page.insert_text(
                            (origin_x, origin_y), 
                            new_text, 
                            fontname='nirmala_bold', 
                            fontfile=NIRMALA_FONT, 
                            fontsize=12.0, 
                            color=(1, 1, 1)
                        )

        # Page 10: First Class Starters
        elif pno == 9:
            # Redact ONLY the number digits, leaving the original Rupee symbol (₹) 100% UNTOUCHED!
            for block in page.get_text('dict')['blocks']:
                if 'lines' in block:
                    for line in block['lines']:
                        for span in line['spans']:
                            # Only numbers on the right side (x > 465)
                            if span['bbox'][0] > 465 and any(c.isdigit() for c in span['text']):
                                pad = 0.5
                                rect = fitz.Rect(span['bbox'][0] - pad, span['bbox'][1] - pad, span['bbox'][2] + pad + 15, span['bbox'][3] + pad)
                                page.add_redact_annot(rect)

            page.apply_redactions(images=0)

            # Insert updated prices using original Calibri-Bold font matching the exact starter positions
            starter_items_map = [
                ("flight deck fries", 469.0, 103.7),
                ("jet -fuel garlic breads", 469.0, 149.8),
                ("twin jet eggs", 469.0, 201.2),
                ("sky crunch", 469.0, 250.0),
                ("wingman lollipops", 467.3, 302.8),
                ("full throttle bowls", 467.1, 352.2),
                ("glider wings", 467.1, 412.8),
                ("vortex balls", 469.0, 475.7),
                ("payload prawns", 469.0, 522.7),
                ("gyro basil fry", 468.2, 579.5),
                ("black box pepper", 470.2, 629.6),
                ("jetfire dragon fry", 470.2, 678.3),
                ("sea food basket", 470.5, 724.4),
            ]
            for sname, origin_x, baseline_y in starter_items_map:
                matched_item = None
                for n, it in name_items.items():
                    if n in sname or sname in n:
                        matched_item = it
                        break
                if matched_item:
                    price_num = int(matched_item.price) if matched_item.price % 1 == 0 else matched_item.price
                    new_text = str(price_num)
                    page.insert_text(
                        (origin_x, baseline_y),
                        new_text,
                        fontname='calibri_bold',
                        fontfile=CALIBRI_BOLD,
                        fontsize=18.0,
                        color=(0, 0, 0)
                    )

        # Render page into static JPG with high resolution (dpi=150)
        pix = page.get_pixmap(dpi=150)
        out_file = os.path.join(OUTPUT_DIR, f"page_{pno + 1}.jpg")
        pix.save(out_file)

    # Save active PDF file
    updated_pdf_path = r'd:\skybliss_menu\media\menu_pdfs\active_live_menu.pdf'
    os.makedirs(os.path.dirname(updated_pdf_path), exist_ok=True)
    doc.save(updated_pdf_path)
    doc.close()

    settings = RestaurantSettings.objects.first()
    if settings:
        settings.menu_pdf.name = 'menu_pdfs/active_live_menu.pdf'
        settings.save(update_fields=['menu_pdf'])
