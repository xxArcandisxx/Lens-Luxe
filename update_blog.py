"""
Updates blog posts to be fashion photography with short descriptions.
"""
import os, sys
from datetime import datetime, timedelta
sys.path.insert(0, os.path.dirname(__file__))

from app import app, db, User, Post

SEED_EMAIL = "editorial@lensandluxe.com"

BLOG_POSTS = [
    {
        "title": "Golden Hour Elegance",
        "content": "<p>Draped in flowing silk against the fading sun -- this is what happens when warm light meets effortless movement. The golden hour transforms every fabric into liquid gold.</p>",
        "tags": "golden hour,silk,editorial,warm tones,fashion photography",
        "image": "https://images.unsplash.com/photo-1509631179647-0177331693ae?w=800&q=80",
    },
    {
        "title": "Monochrome & Minimalism",
        "content": "<p>A study in restraint. Clean lines, sharp tailoring, and the quiet power of black and white. Sometimes the absence of color says everything.</p>",
        "tags": "monochrome,minimalist,black and white,tailoring,editorial",
        "image": "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=800&q=80",
    },
    {
        "title": "Street Layers",
        "content": "<p>Oversized denim, chunky knits, and a walk that owns the pavement. Street style isn't styled -- it's lived. Captured raw on a rainy afternoon in Brooklyn.</p>",
        "tags": "street style,layers,denim,urban,candid",
        "image": "https://images.unsplash.com/photo-1529139574466-a303027c1d8b?w=800&q=80",
    },
    {
        "title": "Velvet Dusk",
        "content": "<p>Deep burgundy velvet catching the last sliver of twilight. There's a reason velvet keeps coming back every season -- it photographs like a dream and wears like armor.</p>",
        "tags": "velvet,evening wear,twilight,burgundy,texture",
        "image": "https://images.unsplash.com/photo-1469334031218-e382a71b716b?w=800&q=80",
    },
    {
        "title": "The Trench Coat Diaries",
        "content": "<p>Classic khaki, cinched waist, collar popped against the wind. The trench coat is not a garment -- it's a character in every story ever told about style.</p>",
        "tags": "trench coat,classic,outerwear,timeless,street photography",
        "image": "https://images.unsplash.com/photo-1483985988355-763728e1935b?w=800&q=80",
    },
    {
        "title": "Neon Nights & Leather",
        "content": "<p>Tokyo after dark. Neon reflections on wet leather, the city humming in electric pink and blue. Fashion that only comes alive when the sun goes down.</p>",
        "tags": "neon,leather,night photography,Tokyo,edgy",
        "image": "https://images.unsplash.com/photo-1558171813-4c088753af8f?w=800&q=80",
    },
    {
        "title": "Linen & Sea Breeze",
        "content": "<p>Unstructured linen billowing in the coastal wind. No accessories, no shoes, no effort -- just fabric and freedom. Summer distilled into a single frame.</p>",
        "tags": "linen,summer,coastal,natural light,effortless",
        "image": "https://images.unsplash.com/photo-1490481651871-ab68de25d43d?w=800&q=80",
    },
    {
        "title": "Architecture Meets Couture",
        "content": "<p>A sculptural gown framed by brutalist concrete. Fashion photography at its best is a conversation between body and space -- and here, both are speaking volumes.</p>",
        "tags": "couture,architecture,editorial,sculptural,high fashion",
        "image": "https://images.unsplash.com/photo-1445205170230-053b83016050?w=800&q=80",
    },
    {
        "title": "The Red Lip Moment",
        "content": "<p>Sometimes the entire outfit is secondary. A bold red lip, sharp eye contact, and the confidence to own the frame. That's the shot. That's the whole story.</p>",
        "tags": "beauty,red lip,portrait,confidence,close-up",
        "image": "https://images.unsplash.com/photo-1560343090-f0409e92791a?w=800&q=80",
    },
    {
        "title": "Florals in Motion",
        "content": "<p>A floral midi dress caught mid-spin on a cobblestone street. The blur is intentional -- because real style is never standing still. Shot at 1/60s to let the fabric dance.</p>",
        "tags": "florals,motion blur,midi dress,movement,romantic",
        "image": "https://images.unsplash.com/photo-1567401893414-76b7b1e5a7a5?w=800&q=80",
    },
]


def update():
    with app.app_context():
        user = User.query.filter_by(email=SEED_EMAIL).first()
        if not user:
            print("[ERROR] Seed user not found. Run seed_content.py first.")
            return

        # Delete old blog posts from seed user
        old = Post.query.filter_by(section='blog', user_id=user.id).all()
        for p in old:
            db.session.delete(p)
        db.session.commit()
        print(f"[OK] Removed {len(old)} old blog posts.")

        # Insert new ones
        now = datetime.utcnow()
        for i, data in enumerate(BLOG_POSTS):
            post = Post(
                title=data["title"],
                content=data["content"],
                image=data["image"],
                tags=data["tags"],
                section="blog",
                user_id=user.id,
                created_at=now - timedelta(days=len(BLOG_POSTS) - i),
            )
            db.session.add(post)
        db.session.commit()
        print(f"[OK] Inserted {len(BLOG_POSTS)} new fashion photography blog posts.")
        print(f"   Total blog posts now: {Post.query.filter_by(section='blog').count()}")


if __name__ == "__main__":
    update()
