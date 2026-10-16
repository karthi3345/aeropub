import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skybliss_core.settings')
django.setup()

from django.contrib.auth.models import User
from menu.models import Category, MenuItem, TableQR

def seed_database():
    print("Creating admin user...")
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@skybliss.com', 'admin123')
        print("Superuser created: admin / admin123")
    else:
        print("Superuser already exists.")

    print("Populating Sky Bliss Categories & Items from the Menu Booklet...")

    # Data from PDF
    menu_structure = [
        {
            "name": "Departure Collections (Signature)",
            "slug": "departure-collections",
            "icon": "fa-martini-glass-citrus",
            "order": 1,
            "items": [
                ("SC1", "Runway Rum", None, 600.00, True),
                ("SC2", "Jetlag Tequila", None, 600.00, True),
                ("SC3", "Cloud Nine Vodka", None, 600.00, True),
                ("SC4", "Sky High Gin", None, 600.00, True),
                ("SC5", "First Class Whisky", None, 600.00, True),
            ]
        },
        {
            "name": "Landing Collections (Super Strong)",
            "slug": "landing-collections",
            "icon": "fa-bolt",
            "order": 2,
            "items": [
                ("MC1", "Tower Control", "Super Strong Cocktails", 800.00, True),
                ("MC2", "Island In The Clouds", "Super Strong Cocktails", 800.00, True),
            ]
        },
        {
            "name": "Vodka Collections",
            "slug": "vodka-collections",
            "icon": "fa-glass-water",
            "order": 3,
            "items": [
                # ₹300 tier
                ("VC1", "Green Runway", "Orange", 300.00, False),
                ("VC2", "Golden First Class", "Lime", 300.00, False),
                ("VC3", "Blue Skies Lemonade", "Blueberry", 300.00, False),
                ("VC4", "Midnight Altitude", "Huckleberry", 300.00, False),
                ("VC5", "Pacific Skies", "Pineapple", 300.00, False),
                ("VC6", "Blueberry Airlift", "Blueberry", 300.00, False),
                # ₹400 tier
                ("VC7", "Midnight Flight", "Black Grape", 400.00, False),
                ("VC8", "Scarlet Takeoff", "Strawberry", 400.00, False),
                ("VC9", "Mango Jetstream", "Mango", 400.00, False),
                ("VC10", "Polar Flight", "Cranberry", 400.00, False),
                ("VC11", "Grape Runway", "Grape", 400.00, False),
                ("VC12", "Orange Takeoff", "Orange", 400.00, False),
                ("VC13", "Pink Cloud Landing", "Cranberry", 400.00, False),
                ("VC14", "Crimson Sunrise", "Orange", 400.00, False),
                ("VC15", "Azure Lounge", "Lemonade", 400.00, False),
                ("VC16", "Cucumber Cloud", "Cucumber", 400.00, False),
                # ₹500 tier
                ("VC17", "Black Grape Altitude", "Black Grape", 500.00, False),
                ("VC18", "Autumn Altitude", "Apple", 500.00, False),
                ("VC19", "Coconut Cloud Nine", "Coconut", 500.00, False),
                ("VC20", "Scarlet Skyline", "Lemon", 500.00, False),
                ("VC21", "Chocolate First Class", "Chocolate", 500.00, False),
                ("VC22", "Parisian Airways", "Pineapple", 500.00, False),
                ("VC23", "Tropical Layover", "Peach", 500.00, False),
                ("VC24", "Emerald Departure", "Orange", 500.00, False),
                ("VC25", "Bubblegum Boarding", "Bubble Gum", 500.00, False),
            ]
        },
        {
            "name": "Rum Collections",
            "slug": "rum-collections",
            "icon": "fa-wine-bottle",
            "order": 4,
            "items": [
                # ₹400 tier
                ("RC1", "Runway Mojito", "Soda", 400.00, False),
                ("RC2", "Orchard Airways", "Apple", 400.00, False),
                ("RC3", "Caribbean Cruise", "Pineapple", 400.00, False),
                ("RC4", "Blue Jetstream", "Pineapple", 400.00, False),
                ("RC5", "Tropical Airspace", "Pineapple", 400.00, False),
                ("RC6", "Mango First Class", "Mango", 400.00, False),
                ("RC7", "Malibu Skyway", "Pineapple", 400.00, False),
                ("RC8", "Blueberry Coastline", "Blueberry", 400.00, False),
                ("RC9", "Tropical Flight Punch", "Watermelon", 400.00, False),
                ("RC10", "Rainbow Clouds", "Pineapple", 400.00, False),
                # ₹500 tier
                ("RC11", "Lunar Flight", "Pineapple", 500.00, False),
                ("RC12", "Banana Cloud Nine", "Banana", 500.00, False),
                ("RC13", "Raspberry Runway", "Raspberry", 500.00, False),
            ]
        },
        {
            "name": "Tequila Collections",
            "slug": "tequila-collections",
            "icon": "fa-champagne-glasses",
            "order": 5,
            "items": [
                ("TC1", "Tangerine Takeoff", "Orange", 400.00, False),
                ("TC2", "Autumn Airways", "Lime", 400.00, False),
                ("TC3", "Sunrise Departure", "Orange", 400.00, False),
                ("TC4", "Rose Gold Airways", "Rose", 400.00, False),
                ("TC5", "Crimson Altitude", "Berry", 400.00, False),
            ]
        },
        {
            "name": "Beers & Wines",
            "slug": "beer-and-wine",
            "icon": "fa-beer-mug-empty",
            "order": 6,
            "items": [
                ("BE1", "Budweiser", "Chilled Premium Beer", 350.00, False),
                ("BE2", "Carlsberg", "Danish Lager", 350.00, False),
                ("BE3", "Corona", "Mexican Cerveza with Lime", 350.00, True),
                ("BE4", "Heineken", "Pure Malt Lager", 350.00, False),
                ("BE5", "Hoegaarden", "Belgian Wheat Beer", 350.00, True),
                ("BE6", "Kingfisher", "Ultra Witbier", 350.00, False),
                ("YN1", "Red Wine", "House Reserve", 500.00, False),
                ("YN2", "White Wine", "Crisp & Refreshing", 500.00, False),
                ("YN3", "Grover", "Art Collection", 500.00, False),
                ("YN4", "Jacob’s Creek", "Australian Shiraz / Chardonnay", 500.00, False),
                ("YN5", "Le Grand Merlot", "French Classic", 500.00, False),
                ("YN6", "JC Pinot Noir", "Delicate Red", 500.00, False),
            ]
        },
        {
            "name": "Spirits (Brandy, Gin, Rum, Vodka)",
            "slug": "spirits",
            "icon": "fa-whiskey-glass",
            "order": 7,
            "items": [
                ("B1", "Morpheus Blue", "Brandy", 200.00, False),
                ("B2", "Monarch Brandy", "Brandy", 250.00, False),
                ("B3", "Morpheus XO", "Brandy", 250.00, False),
                ("B4", "Hobsons", "Brandy", 300.00, False),
                ("B5", "Hennessy", "Cognac", 350.00, True),
                ("G1", "Great Indian", "Gin", 150.00, False),
                ("G2", "Samsara Pink", "Gin", 150.00, False),
                ("G3", "Samsara White", "Gin", 150.00, False),
                ("G4", "Tanqueray", "London Dry Gin", 250.00, False),
                ("G5", "Jaisalmer", "Indian Craft Gin", 250.00, False),
                ("G6", "Cherrapunji", "Eastern Botanical Gin", 250.00, False),
                ("G7", "Bombay Sapphire", "Vapour Infused Gin", 250.00, True),
                ("L1", "Baileys", "Irish Cream Liqueur", 300.00, False),
                ("L2", "Kahlua", "Coffee Liqueur", 300.00, False),
                ("L3", "Jägermeister", "Herbal Liqueur", 350.00, True),
                ("L4", "Cointreau", "Orange Liqueur", 400.00, False),
                ("R1", "Bacardi Ginger", "Rum", 150.00, False),
                ("R2", "Bacardi Guava", "Rum", 150.00, False),
                ("R3", "Bacardi Limon", "Rum", 150.00, False),
                ("R4", "Bacardi Mango Chilli", "Rum", 150.00, False),
                ("R5", "Bacardi Orange", "Rum", 150.00, False),
                ("R6", "Bacardi White", "Rum", 150.00, False),
                ("R7", "Old Monk", "Dark Rum", 180.00, False),
                ("R8", "Old Monk Coffee", "Dark Rum", 200.00, False),
                ("R9", "Bacardi Gold", "Rum", 200.00, False),
                ("R10", "Bacardi Dark", "Rum", 200.00, False),
                ("R11", "Havana Club", "Rum", 250.00, False),
                ("R12", "Bacardi Reserva Ocho", "Aged Rum", 350.00, False),
                ("T1", "Camino", "Tequila", 200.00, False),
                ("T2", "Don Angel", "Tequila", 200.00, False),
                ("T3", "Patrón Silver", "Ultra-Premium Tequila", 400.00, True),
                ("T4", "Warehouse", "Tequila", 400.00, False),
                ("V1", "Smirnoff", "Vodka", 200.00, False),
                ("V2", "Absolut", "Vodka", 240.00, False),
                ("V3", "Absolut Raspberry", "Flavored Vodka", 250.00, False),
                ("V4", "Absolut Grapefruit", "Flavored Vodka", 250.00, False),
                ("V5", "Absolut Lemon", "Flavored Vodka", 250.00, False),
                ("V6", "Absolut Mandarin", "Flavored Vodka", 250.00, False),
                ("V7", "Absolut Citron", "Flavored Vodka", 250.00, False),
                ("V8", "Grey Goose", "French Premium Vodka", 350.00, True),
            ]
        },
        {
            "name": "Whisky Collection",
            "slug": "whisky-collection",
            "icon": "fa-whiskey-glass",
            "order": 8,
            "items": [
                # Regular
                ("W1", "100 Pipers", "Regular Scotch", 180.00, False),
                ("W2", "Ballantine's", "Blended Scotch", 180.00, False),
                ("W3", "Fireball Cinnamon", "Cinnamon Flavored Whisky", 180.00, False),
                ("W4", "Jim Beam", "Kentucky Straight Bourbon", 180.00, False),
                ("W5", "J&B Rare", "Blended Scotch", 180.00, False),
                ("W6", "JW Blonde", "Blended Scotch", 180.00, False),
                ("W7", "Jameson", "Triple Distilled Irish Whiskey", 220.00, False),
                # Single Malt
                ("W8", "Indri", "Trini Single Malt Indian", 250.00, True),
                ("W9", "Godawan", "Single Malt Artisanal", 250.00, False),
                ("W10", "Glenmorangie", "Highland Single Malt", 250.00, False),
                ("W11", "Paul John Nirvana", "Goan Single Malt", 250.00, False),
                ("W12", "Singleton", "12 Years Single Malt", 350.00, False),
                ("W13", "Talisker", "10 Years Isle of Skye Malt", 450.00, True),
                ("W14", "Glenlivet 12 Years", "Speyside Single Malt", 450.00, True),
                # Premium
                ("W15", "Dewar's 12 Years", "Blended Scotch", 250.00, False),
                ("W16", "Seven Island", "Craft Whisky", 280.00, False),
                ("W17", "Chivas Regal", "12 Years Blended Scotch", 280.00, False),
                ("W18", "JW Black Label", "12 Years Blended Scotch", 280.00, False),
                ("W19", "JW Double Black", "Deep Smoky Scotch", 320.00, False),
                ("W20", "JW Gold Label", "Reserve Scotch", 320.00, False),
                ("W21", "Jack Daniel's", "Tennessee Whiskey Old No. 7", 380.00, True),
                ("W22", "Jack Daniel's Honey", "Honey Tennessee Whiskey", 380.00, False),
                ("W23", "Gentleman Jack", "Double Mellowed Tennessee", 450.00, False),
                # Millionaire
                ("W24", "JW Blue Label", "The Masterpiece Blend", 900.00, True),
                ("W25", "Royal Salute", "21 Years Signature Blend", 900.00, True),
                ("W26", "Dalmore", "Highland Single Malt", 900.00, True),
                ("W27", "Chivas 18 Years", "Gold Signature", 900.00, False),
                ("W28", "Dalwhinnie 15 Years", "Highland Single Malt", 900.00, False),
                ("W29", "Dewar's 21 Years", "Double Double Aged", 900.00, False),
                ("W30", "Royal Brackla 21 Years", "The King's Own Whisky", 900.00, True),
            ]
        },
        {
            "name": "First Class Starters",
            "slug": "first-class-starters",
            "icon": "fa-plate-wheat",
            "order": 9,
            "items": [
                ("ST1", "Flight Deck Fries", "Classic / Peri Peri / Cheesy", 180.00, False),
                ("ST2", "Jet-Fuel Garlic Breads", "Classic / Cheesy / Spicy Chicken", 200.00, False),
                ("ST3", "Twin Jet Eggs", "Fry / Pan / Boil", 100.00, False),
                ("ST4", "Sky Crunch", "Chicken Bites / Prawn / Mushroom / Calamari Rings", 300.00, True),
                ("ST5", "Wingman Lollipops", "Chicken / Crab", 300.00, False),
                ("ST6", "Full Throttle Bowls", "Tandoori Chicken / Chicken Sausage / Crispy Prawn / Crumb Fried Mushroom", 300.00, False),
                ("ST7", "Glider Wings", "Korean BBQ / Crispy Cajun / Spicy Honey Hot Baked / Schezwan", 300.00, True),
                ("ST8", "Vortex Balls", "Chicken / Beef / Jalapeno", 350.00, False),
                ("ST9", "Payload Prawns", "Bang Bang / Dynamite", 350.00, True),
                ("ST10", "Gyro Basil Fry", "Mushroom, Paneer, Chicken, Prawn, Mutton", 350.00, False),
                ("ST11", "Black Box Pepper", "Mushroom, Paneer, Chicken, Prawn, Mutton", 350.00, False),
                ("ST12", "Jetfire Dragon Fry", "Mushroom, Paneer, Chicken, Prawn, Mutton", 350.00, False),
                ("ST13", "Sea Food Basket", "Fries, Fish, Prawn, Calamari Rings", 900.00, True),
            ]
        },
        {
            "name": "Lounge Main Course & Fast Lane",
            "slug": "main-course",
            "icon": "fa-bowl-rice",
            "order": 10,
            "items": [
                ("MC01", "Grilled Chicken Steak", "Served with Potatoes, Sauce, Salad & Herb Rice", 500.00, True),
                ("MC02", "Grilled Spicy Fish", "Served with Potatoes, Sauce, Salad & Herb Rice", 500.00, False),
                ("MC03", "Chicken Scaloppine", "Served with Potatoes, Sauce, Salad & Herb Rice", 500.00, False),
                ("MC04", "Beer-Battered Fish & Chips", "Served with Tartar & Fries", 500.00, True),
                ("MC05", "Tequila Chicken Steak", "Infused with Mexican agave and herb glaze", 500.00, True),
                ("MC06", "Chicken Escalope", "Crisp crumbed cutlet with gourmet sauce", 500.00, False),
                ("MC07", "Fish Escalope", "Fresh catch escalope served with herb rice", 500.00, False),
                ("MC08", "Cajun Cottage Cheese Steak", "Paneer steak seasoned with Cajun rub & grilled veg", 500.00, False),
                ("FL01", "Rice / Noodles", "Veg, Egg, Chicken, Schezwan style", 350.00, False),
                ("FL02", "Pastas / Spaghetti", "Pesto, Alfredo, Bolognese sauce options", 350.00, False),
                ("FL03", "Tandoor Breads + Curry", "Veg, Egg, Chicken rich gravies", 350.00, False),
                ("FL04", "Altitude Soft Drinks", "Aerated refreshments & tonics", 40.00, False),
            ]
        }
    ]

    total_items = 0
    for cat_data in menu_structure:
        cat, _ = Category.objects.get_or_create(
            slug=cat_data["slug"],
            defaults={
                "name": cat_data["name"],
                "icon": cat_data["icon"],
                "display_order": cat_data["order"],
            }
        )
        for code, name, flavor, price, is_featured in cat_data["items"]:
            MenuItem.objects.update_or_create(
                category=cat,
                name=name,
                defaults={
                    "code": code,
                    "flavor_or_subtext": flavor,
                    "price": price,
                    "is_featured": is_featured,
                    "is_available": True
                }
            )
            total_items += 1

    print(f"Successfully seeded {total_items} menu items into PostgreSQL database!")

    # Generate Tables and QR Codes
    tables_list = [
        "Rooftop Deck 1",
        "Rooftop Deck 2",
        "Runway VIP Lounge 1",
        "Bar Counter A",
        "Sky Balcony 4",
        "First Class Table 7"
    ]
    for table_name in tables_list:
        table_obj, created = TableQR.objects.get_or_create(table_number=table_name)
        if created or not table_obj.qr_image:
            table_obj.generate_qr(domain="http://127.0.0.1:8000")
            table_obj.save()
            print(f"Generated QR Code for: {table_name}")

    print("Database initialization complete!")

if __name__ == '__main__':
    seed_database()
