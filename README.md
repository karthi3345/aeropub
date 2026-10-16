# Sky Bliss — The AeroPub | Dynamic QR Restaurant Menu

A Django & PostgreSQL-based dynamic restaurant menu application designed for rooftop lounges and restaurants.

## Features
- **Table QR Code Standee**: Customers scan the table QR code to open the menu instantly on mobile without login, app installation, or registration.
- **Dynamic PDF Menu Booklet**: Displays the official 12-page menu card in high resolution, preserving the authentic visual design.
- **Admin Management Portal (`/admin/`)**:
  - Add, edit, and delete food items, cocktails, spirits, beers, wines, and starters.
  - Quick availability toggle (**Available** vs. **Sold Out**).
  - Price updates immediately reflect with the official Indian Rupee (**₹**) symbol.
- **PostgreSQL Database**: Powered by Neon Cloud Serverless PostgreSQL.
- **Public Tunnel Support**: Fully accessible over the internet via Cloudflare Tunnels.

## Tech Stack
- **Backend**: Python 3.12, Django 5.1
- **Database**: PostgreSQL (Neon Cloud)
- **PDF Engine**: PyMuPDF (`fitz`)
- **QR Engine**: `qrcode`, Pillow
- **Frontend**: Tailwind CSS, FontAwesome

## Setup & Running
1. Clone the repository:
   ```bash
   git clone https://github.com/karthi3345/areropub.git
   cd areropub
   ```

2. Install dependencies:
   ```bash
   pip install django dj-database-url psycopg2 qrcode pillow pymupdf
   ```

3. Configure Database URL in environment or `.env`:
   ```bash
   DATABASE_URL=postgresql://neondb_owner:npg_s8euPTpOIyv0@ep-polished-king-b55e3ayh-pooler.c-7.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require
   ```

4. Run migrations and start server:
   ```bash
   python manage.py migrate
   python manage.py runserver 0.0.0.0:8008
   ```

5. Access:
   - **QR Standee**: `http://127.0.0.1:8008/`
   - **Customer Menu**: `http://127.0.0.1:8008/menu/`
   - **Admin Portal**: `http://127.0.0.1:8008/admin/`
