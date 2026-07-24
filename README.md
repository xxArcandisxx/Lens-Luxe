# Lens&Luxe

Website: https://lens-luxe.vercel.app/

Lens&Luxe is a fashion and photography blog platform built with Flask. It combines style inspiration, blog posts, daily scoops, tips, and account features in one clean space for people who enjoy fashion content and visual storytelling.

## Run Locally

1. Clone the repository.
   ```bash
   git clone https://github.com/xxArcandisxx/Lens-Luxe.git
   cd Lens&Luxe
   ```

2. Create and activate a virtual environment.
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install the dependencies.
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your environment variables.
   - Copy `.env.example` to `.env`
   - Fill in the email and news API values you want to use

5. Start the app.
   ```bash
   python app.py
   ```

6. Open the local site in your browser.
   - http://127.0.0.1:5000/

## Notes

- The app uses SQLite by default for local development.
- If you want password reset emails or fashion news updates to work locally, add the values required in `.env`.
