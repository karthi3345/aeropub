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
    Preserves 100% of authentic background photography and design without any dark boxes.
    - Page 6 (Beer & Wine): Full crisp rendering of beers and wines.
    - Page 8 (Spirits - Brandy, Gin, Liqueur, Rum, Tequila, Vodka): All 40 spirit prices
      are accurately mapped and rendered with the official Rupee symbol (₹).
    - Page 9 (Whisky Collections): All 30 whisky prices rendered with Rupee symbol (₹).
    - Page 10 (Starters): Original Rupee symbol (₹) preserved with matching Calibri-Bold digits.
    """
    if not os.path.exists(PDF_SOURCE):
        return

    items = {item.code: item for item in MenuItem.objects.all() if item.code}
    name_items = {item.name.lower().strip(): item for item in MenuItem.objects.all()}

    doc = fitz.open(PDF_SOURCE)

    # 1. Page 6: Beers & Wines (Index 5)
    p6 = doc[5]
    # Check if beer or wine price changed in database
    sample_beer = items.get('BE1') or items.get('BE2')
    sample_wine = items.get('YN1') or items.get('YN2')
    beer_price = int(sample_beer.price) if sample_beer and sample_beer.price % 1 == 0 else (int(sample_beer.price) if sample_beer else 350)
    wine_price = int(sample_wine.price) if sample_wine and sample_wine.price % 1 == 0 else (int(sample_wine.price) if sample_wine else 500)

    # Redact and re-stamp only if price changed from default 350 or 500
    if beer_price != 350:
        p6.add_redact_annot(fitz.Rect(217, 61, 268, 91))
    if wine_price != 500:
        p6.add_redact_annot(fitz.Rect(221, 395, 272, 425))
    p6.apply_redactions(images=0)

    if beer_price != 350:
        p6.insert_text((218.0, 83.0), str(beer_price), fontname='calibri_bold', fontfile=CALIBRI_BOLD, fontsize=27.96, color=(0, 0, 0))
    if wine_price != 500:
        p6.insert_text((222.2, 417.1), str(wine_price), fontname='calibri_bold', fontfile=CALIBRI_BOLD, fontsize=27.96, color=(0, 0, 0))

    # 2. Page 8: Spirits (Index 7) - All 40 items mapped by exact baseline coordinates
    p8 = doc[7]
    # Map of all 40 spirit codes to: (origin_x, origin_y, has_space)
    spirit_coords = {
        'B1': (307.9, 59.0, True),
        'B2': (307.9, 74.6, True),
        'B3': (307.9, 90.3, True),
        'B4': (307.9, 106.0, True),
        'B5': (307.9, 121.7, True),
        'G1': (309.5, 153.0, False),
        'G2': (309.5, 168.7, False),
        'G3': (309.5, 184.3, False),
        'G4': (309.5, 200.0, False),
        'G5': (309.5, 215.7, False),
        'G6': (309.5, 231.4, False),
        'G7': (309.5, 247.0, False),
        'L1': (309.5, 278.4, False),
        'L2': (309.5, 294.0, False),
        'L3': (309.5, 309.7, False),
        'L4': (309.5, 325.4, False),
        'R1': (309.5, 356.7, False),
        'R2': (309.5, 372.4, False),
        'R3': (309.5, 388.1, False),
        'R4': (309.5, 403.8, False),
        'R5': (309.5, 419.4, False),
        'R6': (309.5, 435.1, False),
        'R7': (309.5, 450.8, False),
        'R8': (309.5, 466.4, False),
        'R9': (309.5, 482.1, False),
        'R10': (309.5, 497.8, False),
        'R11': (309.5, 513.5, False),
        'R12': (309.5, 529.1, False),
        'T1': (309.5, 560.9, False),
        'T2': (309.5, 576.6, False),
        'T3': (309.5, 592.2, False),
        'T4': (309.5, 607.9, False),
        'V1': (309.5, 639.3, False),
        'V2': (309.5, 654.9, False),
        'V3': (309.5, 670.6, False),
        'V4': (309.5, 686.3, False),
        'V5': (309.5, 702.0, False),
        'V6': (309.5, 717.6, False),
        'V7': (309.5, 733.3, False),
        'V8': (309.5, 748.9, False),
    }

    # Redact existing price spans on Page 8
    for block in p8.get_text('dict')['blocks']:
        if 'lines' in block:
            for line in block['lines']:
                for span in line['spans']:
                    if span['bbox'][0] > 290 and any(c.isdigit() for c in span['text']):
                        rect = fitz.Rect(span['bbox'][0] - 0.5, span['bbox'][1] - 0.5, span['bbox'][2] + 25, span['bbox'][3] + 0.5)
                        p8.add_redact_annot(rect)

    p8.apply_redactions(images=0)

    # Insert all 40 spirit prices with Rupee symbol and crisp white typography
    for code, (ox, oy, has_sp) in spirit_coords.items():
        item = items.get(code)
        if item:
            price_val = int(item.price) if item.price % 1 == 0 else item.price
            text_to_draw = f"\u20b9 {price_val}" if has_sp else f"\u20b9{price_val}"
            p8.insert_text(
                (ox, oy),
                text_to_draw,
                fontname='nirmala_bold',
                fontfile=NIRMALA_FONT,
                fontsize=12.0,
                color=(1, 1, 1)
            )

    # 3. Page 9: Whisky Collections (Index 8)
    p9 = doc[8]
    whisky_coords = {
        'W1': (367.66, 81.1),
        'W2': (367.66, 97.1),
        'W3': (367.66, 113.0),
        'W4': (367.66, 129.0),
        'W5': (367.66, 145.0),
        'W6': (367.66, 160.9),
        'W7': (367.66, 176.9),
        'W8': (367.66, 229.2),
        'W9': (367.66, 245.2),
        'W10': (367.66, 261.1),
        'W11': (367.66, 277.1),
        'W12': (367.66, 293.1),
        'W13': (367.66, 309.0),
        'W14': (367.66, 325.0),
        'W15': (367.66, 377.1),
        'W16': (367.66, 393.0),
        'W17': (367.66, 409.0),
        'W18': (367.66, 424.9),
        'W19': (367.66, 440.9),
        'W20': (367.66, 456.8),
        'W21': (367.66, 472.8),
        'W22': (367.66, 488.7),
        'W23': (367.66, 504.7),
        'W24': (367.66, 556.8),
        'W25': (367.66, 572.9),
        'W26': (367.66, 588.8),
        'W27': (367.66, 604.8),
        'W28': (367.66, 620.8),
        'W29': (367.66, 636.7),
        'W30': (367.66, 652.7),
    }

    for block in p9.get_text('dict')['blocks']:
        if 'lines' in block:
            for line in block['lines']:
                for span in line['spans']:
                    if span['bbox'][0] > 350 and any(c.isdigit() for c in span['text']):
                        rect = fitz.Rect(span['bbox'][0] - 0.5, span['bbox'][1] - 0.5, span['bbox'][2] + 25, span['bbox'][3] + 0.5)
                        p9.add_redact_annot(rect)

    p9.apply_redactions(images=0)

    for code, (ox, oy) in whisky_coords.items():
        item = items.get(code)
        if item:
            price_val = int(item.price) if item.price % 1 == 0 else item.price
            p9.insert_text(
                (ox, oy),
                f"\u20b9{price_val}",
                fontname='nirmala_bold',
                fontfile=NIRMALA_FONT,
                fontsize=12.0,
                color=(1, 1, 1)
            )

    # 4. Page 10: First Class Starters (Index 9)
    p10 = doc[9]
    for block in p10.get_text('dict')['blocks']:
        if 'lines' in block:
            for line in block['lines']:
                for span in line['spans']:
                    if span['bbox'][0] > 465 and any(c.isdigit() for c in span['text']):
                        rect = fitz.Rect(span['bbox'][0] - 0.5, span['bbox'][1] - 0.5, span['bbox'][2] + 20, span['bbox'][3] + 0.5)
                        p10.add_redact_annot(rect)

    p10.apply_redactions(images=0)

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
            price_val = int(matched_item.price) if matched_item.price % 1 == 0 else matched_item.price
            p10.insert_text(
                (origin_x, baseline_y),
                str(price_val),
                fontname='calibri_bold',
                fontfile=CALIBRI_BOLD,
                fontsize=18.0,
                color=(0, 0, 0)
            )

    # Render all 12 pages into static JPGs at high quality (150 DPI)
    for i in range(len(doc)):
        pix = doc[i].get_pixmap(dpi=150)
        pix.save(os.path.join(OUTPUT_DIR, f"page_{i + 1}.jpg"))

    # Save active PDF
    updated_pdf_path = r'd:\skybliss_menu\media\menu_pdfs\active_live_menu.pdf'
    os.makedirs(os.path.dirname(updated_pdf_path), exist_ok=True)
    doc.save(updated_pdf_path)
    doc.close()

    settings = RestaurantSettings.objects.first()
    if settings:
        settings.menu_pdf.name = 'menu_pdfs/active_live_menu.pdf'
        settings.save(update_fields=['menu_pdf'])
