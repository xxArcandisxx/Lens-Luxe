"""
Seed script for Lens&Luxe — populates the database with sample content:
  • 10 blog posts (fashion) with images, descriptions, and tags
  • 5 fashion tips + 5 photography tips
  • 10 daily scoops (fashion opinions)

Run:  python seed_content.py
"""

import os
import sys
from datetime import datetime, timedelta

# Ensure the app context is available
sys.path.insert(0, os.path.dirname(__file__))

from app import app, db, User, Post, Tip
from sqlalchemy import text

# ─────────────────────────────────────────────
# SEED USER
# ─────────────────────────────────────────────
SEED_EMAIL = "editorial@lensandluxe.com"
SEED_FIRST = "Lens&Luxe"
SEED_LAST  = "Editorial"

def get_or_create_seed_user():
    user = User.query.filter_by(email=SEED_EMAIL).first()
    if not user:
        user = User(
            first_name=SEED_FIRST,
            last_name=SEED_LAST,
            email=SEED_EMAIL,
            phone="",
            interests="fashion,photography",
            newsletter=False,
            bio="The official Lens&Luxe editorial team — curating style, culture, and creativity."
        )
        user.set_password("LensLuxe2025!")
        db.session.add(user)
        db.session.commit()
        print(f"[OK] Created seed user: {SEED_EMAIL}")
    else:
        print(f"[INFO] Seed user already exists: {SEED_EMAIL}")
    return user

# ─────────────────────────────────────────────
# 10 BLOG POSTS  (fashion, with images + tags)
# ─────────────────────────────────────────────
BLOG_POSTS = [
    {
        "title": "The Art of Minimalist Fashion: Less is More",
        "content": """<p>Minimalist fashion is more than just a trend — it's a philosophy of dressing that celebrates quality over quantity, clean lines over clutter, and timeless pieces over fast fashion impulses.</p>
<p>The core principle is simple: build a wardrobe of versatile, well-made pieces that can be mixed and matched effortlessly. Think crisp white shirts, tailored trousers, structured blazers, and neutral tones that never go out of style.</p>
<p>Brands like COS, The Row, and Jil Sander have built entire empires on the idea that restraint is the ultimate form of sophistication. When you strip away the noise, what remains is pure elegance.</p>
<p><strong>Key pieces to invest in:</strong> A perfectly cut trench coat, high-quality denim, cashmere knitwear, and leather accessories in black or tan. These become the foundation upon which you can build any look.</p>
<p>Remember: minimalism isn't about having less — it's about making room for more of what matters.</p>""",
        "tags": "minimalism,capsule wardrobe,timeless style,fashion philosophy",
        "image": "https://images.unsplash.com/photo-1558618666-fcd25c85f82e?w=800&q=80",
    },
    {
        "title": "Street Style Revolution: How Sidewalks Became Runways",
        "content": """<p>Once upon a time, fashion was dictated from the top down — designers set the trends, and the rest of us followed. Today, the most exciting fashion moments happen on the street, captured by photographers and shared millions of times online.</p>
<p>Street style has democratized fashion in ways that no designer collection ever could. It proves that style isn't about price tags or labels — it's about confidence, creativity, and the courage to express yourself.</p>
<p>From the cobblestones of Paris Fashion Week to the neon-lit streets of Tokyo's Harajuku district, street style tells the story of how real people interpret and reinvent trends on their own terms.</p>
<p>The best street style looks share one thing in common: they break rules. Mixing high and low, clashing prints, layering unexpected textures — these are the moves that catch the photographer's eye and set the next wave of trends in motion.</p>
<p>Whether you're pairing vintage denim with designer heels or throwing a leather jacket over a silk dress, street style is your permission to experiment.</p>""",
        "tags": "street style,fashion week,urban fashion,trend setting",
        "image": "https://images.unsplash.com/photo-1509631179647-0177331693ae?w=800&q=80",
    },
    {
        "title": "Sustainable Fashion: Dressing for a Better Tomorrow",
        "content": """<p>The fashion industry is the second-largest polluter in the world, right after oil. But a revolution is underway — and it starts in your closet.</p>
<p>Sustainable fashion means making conscious choices: buying fewer but better-quality pieces, supporting ethical brands, shopping secondhand, and caring for the clothes you already own.</p>
<p>Pioneering brands like Stella McCartney, Patagonia, and Reformation are proving that sustainability and style aren't mutually exclusive. From organic cotton tees to recycled polyester activewear, eco-friendly options have never looked this good.</p>
<p><strong>Simple swaps you can make today:</strong></p>
<ul>
<li>Choose natural fabrics like linen, hemp, and organic cotton</li>
<li>Shop vintage and thrift stores for unique finds</li>
<li>Learn basic mending and tailoring skills</li>
<li>Invest in timeless pieces that won't end up in landfill after one season</li>
</ul>
<p>Every purchase is a vote for the kind of world you want to live in. Make it count.</p>""",
        "tags": "sustainable fashion,eco-friendly,ethical style,slow fashion",
        "image": "https://images.unsplash.com/photo-1523381210434-271e8be1f52b?w=800&q=80",
    },
    {
        "title": "The Power of Accessories: Elevating Every Outfit",
        "content": """<p>Accessories are the punctuation marks of fashion — they can transform a whisper into an exclamation point. The right bag, shoe, or piece of jewelry can take the simplest outfit from forgettable to unforgettable.</p>
<p>Consider Audrey Hepburn's pearl necklace, Diana Ross's oversized sunglasses, or Rihanna's statement earrings. Accessories don't just complete a look — they define it.</p>
<p>This season, the trends are all about bold contrast: chunky gold chains against minimalist outfits, architectural bags that double as art, and shoes that make a statement from across the room.</p>
<p><strong>The accessories every wardrobe needs:</strong></p>
<ul>
<li>A structured leather handbag in a neutral shade</li>
<li>Gold hoop earrings (small for everyday, large for evenings)</li>
<li>A silk scarf that can be styled a dozen different ways</li>
<li>A quality watch that tells your story as well as the time</li>
<li>Sunglasses that frame your face with confidence</li>
</ul>
<p>The beauty of accessories is that they let you reinvent yourself every single day without buying a whole new wardrobe.</p>""",
        "tags": "accessories,jewelry,bags,fashion essentials",
        "image": "https://images.unsplash.com/photo-1611085583191-a3b181a88401?w=800&q=80",
    },
    {
        "title": "Color Theory in Fashion: How to Master Your Palette",
        "content": """<p>Color is the first thing people notice about your outfit — even before silhouette, fabric, or brand. Understanding color theory can transform the way you dress and how you're perceived.</p>
<p>The basics are simple: complementary colors (opposite on the color wheel) create bold contrast, analogous colors (neighbors on the wheel) create harmony, and monochromatic looks (shades of one hue) exude sophistication.</p>
<p>This season's palette leans into rich, saturated tones: burgundy, cobalt blue, emerald green, and mustard yellow. These colors work beautifully against the neutral backgrounds of everyday life and photograph exceptionally well.</p>
<p><strong>Pro tips for color confidence:</strong></p>
<ul>
<li>Find your skin's undertone (warm, cool, or neutral) to identify your most flattering shades</li>
<li>Start with one statement color piece and build the rest of the outfit around it</li>
<li>Don't be afraid of color-blocking — pairing unexpected hues is where magic happens</li>
<li>Use neutrals as anchors: black, white, navy, and camel ground any bold color choices</li>
</ul>
<p>Fashion is self-expression, and color is your most powerful tool.</p>""",
        "tags": "color theory,styling tips,fashion palette,outfit ideas",
        "image": "https://images.unsplash.com/photo-1445205170230-053b83016050?w=800&q=80",
    },
    {
        "title": "Denim Decoded: The History and Future of Jeans",
        "content": """<p>No single garment has had a more profound impact on global fashion than the humble pair of jeans. From gold miners in 1850s California to runway models in Milan, denim has been reimagined by every generation.</p>
<p>Levi Strauss and Jacob Davis patented the riveted blue jean in 1873, creating what would become the most universal garment in human history. Today, there are estimated to be over 1.2 billion pairs of jeans sold every year worldwide.</p>
<p>The beauty of denim lies in its versatility. Dress it up with a blazer and heels for a sophisticated evening look, or keep it casual with sneakers and a vintage tee. The fade, the wash, the cut — every detail tells a story.</p>
<p><strong>Denim trends to watch:</strong></p>
<ul>
<li>Wide-leg and barrel-cut silhouettes are dominating the scene</li>
<li>Vintage-inspired washes with natural fading</li>
<li>Double denim (yes, the "Canadian tuxedo" is back and better than ever)</li>
<li>Sustainable denim made with organic cotton and waterless processing</li>
</ul>
<p>The best pair of jeans is the one that makes you feel like the best version of yourself.</p>""",
        "tags": "denim,jeans,fashion history,wardrobe staple",
        "image": "https://images.unsplash.com/photo-1542272604-787c3835535d?w=800&q=80",
    },
    {
        "title": "Fashion Forward: How Technology is Reshaping Style",
        "content": """<p>The intersection of fashion and technology is producing some of the most exciting innovations of our time. From AI-powered personal styling to 3D-printed garments, the future of fashion is being written in code.</p>
<p>Virtual try-on technology is eliminating the guesswork of online shopping. Brands like Gucci, Nike, and Warby Parker now let you see how products look on your body before you click "buy." This isn't just convenient — it's dramatically reducing return rates and environmental waste.</p>
<p>Meanwhile, smart fabrics are blurring the line between clothing and technology. Imagine a jacket that adjusts its temperature based on the weather, or a dress that changes color with your mood. These aren't science fiction — they're being developed right now.</p>
<p><strong>Tech trends in fashion:</strong></p>
<ul>
<li>Digital fashion and NFT wearables for virtual worlds</li>
<li>AI-curated personal shopping experiences</li>
<li>Blockchain-verified supply chain transparency</li>
<li>Biofabricated materials grown in labs, not factories</li>
</ul>
<p>Technology won't replace the artistry of fashion — but it will amplify it in ways we're only beginning to imagine.</p>""",
        "tags": "fashion tech,innovation,future fashion,digital style",
        "image": "https://images.unsplash.com/photo-1558171813-4c088753af8f?w=800&q=80",
    },
    {
        "title": "The Renaissance of Vintage Fashion",
        "content": """<p>In a world obsessed with the new, there's something revolutionary about choosing the old. Vintage fashion is experiencing a golden age, driven by sustainability concerns, a desire for uniqueness, and pure nostalgia.</p>
<p>Thrift stores, consignment shops, and online platforms like Depop and The RealReal have made vintage shopping more accessible than ever. What was once the domain of dedicated collectors is now mainstream — and the fashion industry is paying attention.</p>
<p>The appeal of vintage goes beyond aesthetics. Every piece has a history, a provenance, a story woven into its fabric. That 1970s suede jacket wasn't designed by an algorithm — it was crafted by hands that understood the art of making something to last.</p>
<p><strong>How to shop vintage like a pro:</strong></p>
<ul>
<li>Know your measurements — vintage sizing is completely different from modern sizing</li>
<li>Inspect quality: check seams, zippers, and fabric condition</li>
<li>Focus on decades that complement your personal style</li>
<li>Don't be afraid to tailor vintage finds for a modern fit</li>
</ul>
<p>The greenest garment is the one that already exists.</p>""",
        "tags": "vintage fashion,thrifting,retro style,secondhand",
        "image": "https://images.unsplash.com/photo-1567401893414-76b7b1e5a7a5?w=800&q=80",
    },
    {
        "title": "Athleisure: When Comfort Met Couture",
        "content": """<p>The rise of athleisure represents one of the most significant shifts in fashion history — the moment when comfort stopped being the enemy of style and became its closest ally.</p>
<p>What started as yoga pants at the grocery store has evolved into a multi-billion-dollar industry where luxury brands like Balenciaga, Loewe, and Prada create sneakers that cost more than most people's rent.</p>
<p>The pandemic accelerated this trend dramatically. When the whole world was working from home, the line between loungewear and workwear didn't just blur — it disappeared. And now that we're back in the world, we refuse to give up our comfort.</p>
<p>The key to nailing athleisure is intentionality. This isn't about wearing gym clothes everywhere — it's about choosing athletic-inspired pieces that are elevated enough for any setting.</p>
<p><strong>Athleisure essentials:</strong></p>
<ul>
<li>Premium sneakers in clean, minimal designs</li>
<li>Structured joggers in luxe fabrics like silk or cashmere blends</li>
<li>Performance-fabric blazers that move with you</li>
<li>Elevated hoodies and sweatshirts in muted, sophisticated tones</li>
</ul>""",
        "tags": "athleisure,comfort style,sneaker culture,modern fashion",
        "image": "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=800&q=80",
    },
    {
        "title": "The Influence of Culture on Global Fashion Trends",
        "content": """<p>Fashion doesn't exist in a vacuum. It's a reflection of culture, history, politics, and identity. The most exciting fashion movements have always emerged from cultural crossroads — places where traditions collide, blend, and create something entirely new.</p>
<p>From the vibrant wax prints of West African fashion to the precise tailoring of Japanese design houses like Comme des Garçons and Issey Miyake, cultural heritage is fashion's richest source of inspiration.</p>
<p>K-fashion from South Korea has taken the global stage by storm, blending streetwear sensibilities with meticulous attention to detail. Meanwhile, Indian designers like Sabyasachi Mukherjee are bringing centuries-old textile traditions to international runways.</p>
<p>The conversation around cultural appreciation versus appropriation is more important than ever. True fashion innovation comes from understanding and respecting the traditions that inspire us.</p>
<p><strong>Cultural fashion moments that changed everything:</strong></p>
<ul>
<li>The Japanese avant-garde movement of the 1980s</li>
<li>African print's journey from tradition to global trend</li>
<li>The Mexican huipil inspiring haute couture collections</li>
<li>K-pop's influence on global street style</li>
</ul>
<p>Fashion at its best is a bridge between cultures, a universal language of creativity and self-expression.</p>""",
        "tags": "cultural fashion,global style,fashion diversity,heritage",
        "image": "https://images.unsplash.com/photo-1529139574466-a303027c1d8b?w=800&q=80",
    },
]

# ─────────────────────────────────────────────
# 5 FASHION TIPS + 5 PHOTOGRAPHY TIPS
# ─────────────────────────────────────────────
TIPS = [
    # --- Fashion Tips (5) ---
    {
        "title": "Build a Capsule Wardrobe That Works Year-Round",
        "subtitle": "A curated capsule wardrobe saves time, money, and decision fatigue — here's how to build one from scratch.",
        "content": """<h3>The Capsule Wardrobe Blueprint</h3>
<p>A capsule wardrobe is a carefully curated collection of 30-40 versatile pieces that can be mixed and matched to create dozens of outfits for every occasion.</p>

<h4>Step 1: Audit Your Current Closet</h4>
<p>Pull everything out. If you haven't worn it in 12 months, donate it. Be ruthless — clutter is the enemy of style.</p>

<h4>Step 2: Define Your Color Palette</h4>
<p>Choose 3-4 neutrals (black, white, navy, camel) and 2-3 accent colors that complement your skin tone. Every piece should work with at least three others.</p>

<h4>Step 3: Invest in Quality Basics</h4>
<ul>
<li><strong>Tops:</strong> 2 white tees, 2 striped/solid tees, 3 button-downs, 2 knit sweaters</li>
<li><strong>Bottoms:</strong> 2 jeans (dark + light), 1 tailored trouser, 1 skirt or shorts</li>
<li><strong>Outerwear:</strong> 1 blazer, 1 trench coat, 1 leather/denim jacket</li>
<li><strong>Shoes:</strong> White sneakers, ankle boots, loafers, one dress shoe</li>
</ul>

<h4>Step 4: The One-In-One-Out Rule</h4>
<p>For every new piece you add, one must leave. This keeps your wardrobe tight and intentional.</p>

<p><em>Pro tip: Lay out your weekly outfits on Sunday evening. You'll thank yourself every rushed morning.</em></p>""",
        "category": "fashion",
        "tags": "capsule wardrobe,wardrobe essentials,styling tips,minimalist fashion,closet organization",
        "image": "https://images.unsplash.com/photo-1558618666-fcd25c85f82e?w=800&q=80",
    },
    {
        "title": "How to Dress for Your Body Shape with Confidence",
        "subtitle": "Understanding your body shape isn't about hiding — it's about highlighting what you love most.",
        "content": """<h3>Finding Your Perfect Silhouette</h3>
<p>Every body is different, and the best-dressed people aren't those with "perfect" bodies — they're the ones who understand how to use proportion, line, and fit to their advantage.</p>

<h4>The Fit Test</h4>
<p>Before worrying about trends, master fit. Clothes that fit properly — not too tight, not too loose — will always look more expensive and polished than ill-fitting designer pieces.</p>

<h4>Universal Rules That Work for Everyone</h4>
<ul>
<li><strong>Tailoring is your best friend:</strong> A $20 alteration can make a $50 blazer look like $500</li>
<li><strong>Know your rise:</strong> High-waisted pants elongate the leg; mid-rise is universally flattering</li>
<li><strong>Monochrome magic:</strong> Wearing one color head-to-toe creates an unbroken vertical line that's inherently slimming</li>
<li><strong>The rule of thirds:</strong> Break your outfit into ⅓ and ⅔ proportions for visual balance</li>
</ul>

<h4>The Confidence Factor</h4>
<p>The single most important thing you can wear is confidence. No amount of styling tricks can replace the magnetic energy of someone who genuinely loves what they're wearing.</p>

<p><em>Try this: Find a full-length mirror, put on your favorite outfit, and stand tall. Notice what makes you feel powerful — then build your wardrobe around that feeling.</em></p>""",
        "category": "fashion",
        "tags": "body shape,styling tips,fit guide,fashion confidence,personal style",
        "image": "https://images.unsplash.com/photo-1483985988355-763728e1935b?w=800&q=80",
    },
    {
        "title": "Mastering the Art of Layering for Every Season",
        "subtitle": "Layering isn't just practical — it's one of the most creative ways to build depth and dimension in your outfits.",
        "content": """<h3>The Layering Playbook</h3>
<p>Great layering is like great music — it's about harmony between different elements, each adding something unique to the whole.</p>

<h4>The Three-Layer System</h4>
<ol>
<li><strong>Base layer:</strong> Lightweight, close to the body. Think fitted tees, tank tops, or thin turtlenecks</li>
<li><strong>Mid layer:</strong> Adds warmth and visual interest. Shirts, sweaters, cardigans, or vests</li>
<li><strong>Outer layer:</strong> The statement piece. Coats, jackets, blazers, or capes</li>
</ol>

<h4>Texture Mixing</h4>
<p>The secret to elevated layering is mixing textures: pair smooth silk with chunky knit, matte cotton with glossy leather, or soft cashmere with structured denim.</p>

<h4>Proportion Play</h4>
<ul>
<li>If your outer layer is oversized, keep the base slim</li>
<li>Cropped jackets work beautifully over longer tops and dresses</li>
<li>Let interesting base layers peek through — a lace collar, a patterned hem, or a colored cuff</li>
</ul>

<h4>Summer Layering</h4>
<p>Layering isn't just for winter. In warmer months, try lightweight linen shirts over cotton tanks, or a structured vest over a flowing maxi dress.</p>

<p><em>Golden rule: If you can remove one layer and still have a complete outfit, you've mastered the art.</em></p>""",
        "category": "fashion",
        "tags": "layering,seasonal style,outfit building,fashion tips,texture mixing",
        "image": "https://images.unsplash.com/photo-1490481651871-ab68de25d43d?w=800&q=80",
    },
    {
        "title": "The Ultimate Guide to Building a Shoe Collection",
        "subtitle": "Your shoes say more about you than any other item in your wardrobe — here's how to curate a collection that covers every occasion.",
        "content": """<h3>The Foundation Five</h3>
<p>You don't need 50 pairs of shoes. You need 5-7 great pairs that cover every scenario life throws at you.</p>

<h4>1. White Sneakers</h4>
<p>The most versatile shoe in existence. Works with jeans, chinos, dresses, suits (yes, suits). Look for leather or premium canvas in a clean, minimalist design. Keep them white — a suede eraser and gentle cleaner are your best friends.</p>

<h4>2. Classic Ankle Boots</h4>
<p>In black or brown leather, ankle boots bridge the gap between casual and formal. Chelsea boots for a sleek look, lace-ups for edge, or pointed-toe for elegance.</p>

<h4>3. Dress Shoes</h4>
<p>Oxfords, loafers, or heels — whatever matches your style. One impeccable pair in black or dark brown covers weddings, interviews, and every dressy occasion.</p>

<h4>4. Comfortable Sandals</h4>
<p>Quality leather sandals (not flip-flops) for summer. Brands like Birkenstock have proven that comfort and style can coexist beautifully.</p>

<h4>5. Statement Shoes</h4>
<p>One pair that's unapologetically YOU. Bold color, interesting texture, unique design. These are the shoes that make people stop and ask, "Where did you get those?"</p>

<p><em>Investment tip: Cost-per-wear beats sticker price every time. A $300 shoe worn 200 times costs $1.50 per wear. A $30 shoe worn 5 times costs $6.</em></p>""",
        "category": "fashion",
        "tags": "shoes,footwear,wardrobe essentials,shoe collection,fashion investment",
        "image": "https://images.unsplash.com/photo-1560343090-f0409e92791a?w=800&q=80",
    },
    {
        "title": "Transitional Dressing: Navigating Between Seasons in Style",
        "subtitle": "Those in-between weeks where it's too cold for summer clothes but too warm for winter gear — here's how to nail them.",
        "content": """<h3>The In-Between Wardrobe</h3>
<p>Transitional dressing is arguably the hardest style challenge of the year. Morning calls for a coat, afternoon wants a tee, and evening can go either way. The solution? Strategic versatility.</p>

<h4>Key Transitional Pieces</h4>
<ul>
<li><strong>The lightweight trench:</strong> Iconic for a reason — it handles rain, wind, and everything in between while looking effortlessly chic</li>
<li><strong>Knit vests:</strong> Layer over long-sleeve shirts for added warmth that's easy to remove</li>
<li><strong>Midi skirts and dresses:</strong> More coverage than minis, more breathable than pants</li>
<li><strong>Lightweight scarves:</strong> Add warmth to your neck without committing to full winter gear</li>
<li><strong>Closed-toe flats or loafers:</strong> The sweet spot between sandals and boots</li>
</ul>

<h4>The Temperature Hack</h4>
<p>Dress in layers you can add or remove throughout the day. Start with a breathable base, add a mid-layer for warmth, and carry a light outer layer in your bag for unpredictable weather swings.</p>

<h4>Fabric Focus</h4>
<p>This is where fabric choice matters most. Look for mid-weight fabrics like merino wool, ponte, cotton twill, and light denim. Avoid heavy knits (too warm) and sheer fabrics (too cold).</p>

<p><em>Style hack: A great pair of boots with a summer dress and a denim jacket is the ultimate transitional outfit formula.</em></p>""",
        "category": "fashion",
        "tags": "transitional dressing,seasonal fashion,layering tips,wardrobe planning,weather styling",
        "image": "https://images.unsplash.com/photo-1469334031218-e382a71b716b?w=800&q=80",
    },

    # --- Photography Tips (5) ---
    {
        "title": "Mastering Natural Light for Stunning Fashion Photography",
        "subtitle": "Natural light is a fashion photographer's best friend — learn to read it, shape it, and make it work for any shoot.",
        "content": """<h3>Light Is Everything</h3>
<p>The difference between an amateur snapshot and a professional fashion photograph often comes down to one thing: light. And the best part? The most beautiful light is completely free.</p>

<h4>The Golden Hour</h4>
<p>The first and last hour of sunlight produce the warmest, most flattering light. Skin glows, fabrics shimmer, and everything takes on a cinematic quality. Plan your shoots around these windows whenever possible.</p>

<h4>Open Shade</h4>
<p>On bright sunny days, move your subject into open shade — under a tree, the shadow of a building, or a covered walkway. You get even, soft light without harsh shadows or squinting.</p>

<h4>Window Light</h4>
<p>For indoor shoots, nothing beats a large north-facing window. Position your subject 2-3 feet from the window at a 45-degree angle. Use a white reflector or even a white bedsheet on the opposite side to fill in shadows.</p>

<h4>Overcast Days Are Gold</h4>
<p>Cloud cover acts like a giant softbox, diffusing sunlight evenly across your subject. Colors appear more saturated, skin looks smoother, and you can shoot from virtually any angle without worrying about harsh shadows.</p>

<h4>Reading Light Direction</h4>
<ul>
<li><strong>Front light:</strong> Flat and even — great for clean beauty shots</li>
<li><strong>Side light:</strong> Creates depth and dimension — perfect for editorial drama</li>
<li><strong>Back light:</strong> Produces rim light and ethereal glow — ideal for romantic, airy shoots</li>
</ul>

<p><em>Practice exercise: Photograph the same subject at five different times of day and compare the results. You'll start seeing light differently forever.</em></p>""",
        "category": "photography",
        "tags": "natural light,fashion photography,golden hour,lighting tips,photo techniques",
        "image": "https://images.unsplash.com/photo-1542038784456-1ea8e935640e?w=800&q=80",
    },
    {
        "title": "Composition Rules That Transform Fashion Photos",
        "subtitle": "Great composition is invisible — it guides the viewer's eye exactly where you want it to go, every single time.",
        "content": """<h3>Beyond the Rule of Thirds</h3>
<p>Composition is the silent language of photography. It determines what the viewer sees first, where their eye travels, and how the image makes them feel.</p>

<h4>Rule of Thirds (But Know When to Break It)</h4>
<p>Placing your subject at the intersection of thirds creates natural visual tension. But centering your subject can create powerful symmetry and dominance. Know the rule so you can break it intentionally.</p>

<h4>Leading Lines</h4>
<p>Use architectural elements — staircases, corridors, roads, railings — to draw the viewer's eye toward your subject. Fashion photography in urban environments benefits enormously from this technique.</p>

<h4>Framing Within the Frame</h4>
<p>Doorways, windows, arches, and even foliage can create natural frames around your subject. This adds depth and focuses attention exactly where you want it.</p>

<h4>Negative Space</h4>
<p>Don't fill every pixel. Generous negative space around your subject creates a sense of luxury and editorial sophistication. This is especially powerful for showcasing individual garments.</p>

<h4>The Power of Diagonals</h4>
<p>Diagonal lines create energy and movement. Tilt your camera slightly, have your model lean, or use diagonal architectural elements to add dynamism to static poses.</p>

<h4>Color Composition</h4>
<ul>
<li>Match the garment's color palette to the location's tones</li>
<li>Use contrasting background colors to make clothing pop</li>
<li>Monochromatic environments create clean, editorial looks</li>
</ul>

<p><em>Study the masters: Look at the work of Peter Lindbergh, Annie Leibovitz, and Mario Testino — notice how every element in their frames serves a purpose.</em></p>""",
        "category": "photography",
        "tags": "composition,photography rules,visual storytelling,fashion photography,framing techniques",
        "image": "https://images.unsplash.com/photo-1452587925148-ce544e77e70d?w=800&q=80",
    },
    {
        "title": "Essential Camera Settings for Fashion Photography",
        "subtitle": "Aperture, shutter speed, ISO — understanding these three pillars will give you complete creative control over your images.",
        "content": """<h3>The Exposure Triangle for Fashion</h3>
<p>Your camera is a tool, and like any tool, understanding its mechanics unlocks its full potential. Here are the settings that matter most for fashion photography.</p>

<h4>Aperture (f-stop)</h4>
<p>This controls depth of field — how much of your image is in sharp focus.</p>
<ul>
<li><strong>f/1.4–f/2.8:</strong> Creamy, blurred backgrounds that isolate your subject. Perfect for portraits and detail shots of accessories</li>
<li><strong>f/4–f/5.6:</strong> The sweet spot for most fashion work. Sharp subject with gentle background separation</li>
<li><strong>f/8–f/11:</strong> Maximum sharpness throughout the frame. Ideal for editorial and architectural fashion shots</li>
</ul>

<h4>Shutter Speed</h4>
<p>For static fashion poses, 1/125 second or faster is sufficient. For walking shots and movement (flowing fabrics, hair toss), go to 1/500 or faster. For intentional motion blur, drop to 1/30 and stabilize your camera.</p>

<h4>ISO</h4>
<p>Keep it as low as possible (100-400) for clean, noise-free images. Modern cameras handle ISO 800-1600 well for low-light situations. Anything above 3200 should be a last resort.</p>

<h4>White Balance</h4>
<p>Shoot in RAW and adjust in post, but setting an approximate white balance in-camera helps you evaluate images on set. Slightly warm tones (5500-6000K) tend to be most flattering for skin.</p>

<h4>Recommended Starting Settings</h4>
<p><strong>Outdoor portrait:</strong> f/2.8, 1/250s, ISO 100<br>
<strong>Indoor natural light:</strong> f/2.0, 1/125s, ISO 400<br>
<strong>Movement/editorial:</strong> f/4, 1/500s, ISO 200</p>

<p><em>Remember: There are no "correct" settings — only settings that serve your creative vision. Experiment relentlessly.</em></p>""",
        "category": "photography",
        "tags": "camera settings,aperture,ISO,shutter speed,photography basics,exposure",
        "image": "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=800&q=80",
    },
    {
        "title": "How to Direct Models and Create Natural Poses",
        "subtitle": "The best fashion photographs feel effortless — here's how to guide your subject toward authentic, dynamic poses.",
        "content": """<h3>Directing with Intention</h3>
<p>A photographer who can direct well will always produce better work than one who relies solely on technical skill. The ability to make your subject feel comfortable and confident in front of the camera is an art form in itself.</p>

<h4>Before the Shoot</h4>
<ul>
<li>Create a mood board with reference images — share it with your model beforehand</li>
<li>Discuss the concept, the mood, and the story you're trying to tell</li>
<li>Play music that matches the energy of the shoot — it transforms the atmosphere</li>
</ul>

<h4>Movement Over Stillness</h4>
<p>Static poses often feel stiff. Instead, give your model actions: "Walk toward me slowly," "Turn and look over your shoulder," "Fix your collar," "Adjust your sleeve." These micro-movements create natural, editorial moments.</p>

<h4>The Triangle Method</h4>
<p>Create triangles with the body: bent arms, tilted hips, crossed legs. Triangular shapes are visually dynamic and prevent the "standing like a cardboard cutout" look.</p>

<h4>Hand Placement</h4>
<p>Hands are the most awkward body part to pose. Give them purpose: touching fabric, adjusting jewelry, running through hair, or resting in pockets. Hands should always be doing something.</p>

<h4>Facial Expression Prompts</h4>
<ul>
<li>"Think of something that makes you genuinely smile" — for authentic joy</li>
<li>"Look just past the camera, like you see someone you know" — for soft, candid looks</li>
<li>"Take a deep breath and relax your jaw" — for editorial calm</li>
<li>"Tell me about your weekend" — conversation produces the most natural expressions</li>
</ul>

<p><em>Golden rule: Never stop shooting. Some of the best fashion photographs happen between the "official" poses.</em></p>""",
        "category": "photography",
        "tags": "model directing,posing tips,fashion shoots,portrait photography,creative direction",
        "image": "https://images.unsplash.com/photo-1469460340997-2f854421e72f?w=800&q=80",
    },
    {
        "title": "Post-Processing Fashion Photos: From Good to Magazine-Ready",
        "subtitle": "Editing is where good fashion photos become great — master these post-processing techniques to create polished, editorial-quality images.",
        "content": """<h3>The Editing Workflow</h3>
<p>Post-processing is not about making a bad photo good — it's about making a good photo great. The best editors enhance what's already there without creating an artificial look.</p>

<h4>Step 1: Culling and Selection</h4>
<p>Before you edit a single pixel, select your best images ruthlessly. Flag your top picks, rate them, and only edit the ones worth your time. A tight edit of 20 stunning images beats 200 mediocre ones.</p>

<h4>Step 2: Global Adjustments</h4>
<ul>
<li><strong>Exposure:</strong> Correct any under/overexposure first</li>
<li><strong>White balance:</strong> Ensure accurate skin tones — slightly warm is usually most flattering</li>
<li><strong>Contrast:</strong> Add subtle contrast to create depth without crushing shadows</li>
<li><strong>Highlights/Shadows:</strong> Recover highlight detail, lift shadows slightly for a modern, airy look</li>
</ul>

<h4>Step 3: Color Grading</h4>
<p>This is where you develop your signature style. Fashion photography tends toward two directions:</p>
<ul>
<li><strong>Clean and bright:</strong> Lifted shadows, desaturated highlights, soft pastels</li>
<li><strong>Rich and moody:</strong> Deep blacks, warm shadows, saturated jewel tones</li>
</ul>

<h4>Step 4: Skin Retouching</h4>
<p>Less is more. Remove temporary blemishes, even out major discoloration, but preserve skin texture. The "porcelain doll" look is outdated — authentic skin is beautiful.</p>

<h4>Step 5: Sharpening and Export</h4>
<p>Apply subtle sharpening for print or web. Export at the appropriate resolution: 300 DPI for print, 72 DPI and sRGB for web and social media.</p>

<p><em>Develop a consistent editing style across your portfolio — art directors and clients hire photographers partly for their distinctive visual language.</em></p>""",
        "category": "photography",
        "tags": "photo editing,post-processing,lightroom,fashion retouching,color grading",
        "image": "https://images.unsplash.com/photo-1572044162444-ad60f128bdea?w=800&q=80",
    },
]

# ─────────────────────────────────────────────
# 10 DAILY SCOOPS  (opinions on fashion stuff)
# ─────────────────────────────────────────────
DAILY_SCOOPS = [
    {
        "title": "Hot Take: Quiet Luxury Is Just Rich People Gatekeeping Style",
        "content": """<p>Let's be honest — the "quiet luxury" trend is less about refined taste and more about signaling wealth in a way that only other wealthy people can decode. A $3,000 cashmere sweater that looks identical to a $30 one from H&M isn't minimalism — it's expensive camouflage.</p>
<p>The fashion industry loves to rebrand elitism as taste. When they say "invest in quality," what they mean is "spend more than most people earn in a week on a single item." And the worst part? They've convinced us that visible logos and bold colors are somehow <em>less</em> sophisticated.</p>
<p>Real style has never been about price tags — visible or invisible. It's about how you put things together, the confidence you carry, and the story your outfit tells. A thrifted outfit styled with intention will always beat a $10,000 "quiet luxury" look worn without personality.</p>
<p>The real flex isn't being able to afford stealth wealth. It's being able to look incredible regardless of your budget.</p>""",
        "tags": "quiet luxury,fashion debate,hot take,style opinion",
        "image": "https://images.unsplash.com/photo-1490481651871-ab68de25d43d?w=800&q=80",
    },
    {
        "title": "Why Fast Fashion Will Never Actually Die (And Why That's Complicated)",
        "content": """<p>Every fashion publication has declared fast fashion dead at least once. And yet, Shein alone is valued at over $60 billion. Zara ships new designs in two weeks. H&M drops collaborations with luxury designers every season. Fast fashion isn't dying — it's mutating.</p>
<p>The uncomfortable truth is that sustainable fashion remains a privilege. When a "conscious" brand charges $120 for a basic t-shirt, they're not solving the problem — they're serving a different audience. Most people can't afford to "invest in quality" when they need clothes for a job interview next week.</p>
<p>The real conversation should be about systemic change: better wages for garment workers, stricter environmental regulations, and accessible alternatives at every price point. Shaming individuals for buying affordable clothes while corporations face zero consequences is not progress — it's performative activism.</p>
<p>We need solutions that work for everyone, not just those who can afford organic cotton at premium prices.</p>""",
        "tags": "fast fashion,sustainability debate,fashion industry,opinion",
        "image": "https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=800&q=80",
    },
    {
        "title": "Sneaker Culture Has Peaked — And That's a Good Thing",
        "content": """<p>Remember when sneakers were about actual design innovation? When each release told a story, honored a cultural moment, or pushed the boundaries of what footwear could be? Those days feel like ancient history.</p>
<p>Today's sneaker market is dominated by hype cycles, bot-driven resale, and endless colorway variants of the same silhouettes. The Jordan 1 has been released in approximately 4,000 versions. The Dunk has been done to death. Even the most passionate sneakerheads are admitting fatigue.</p>
<p>But here's the silver lining: as hype culture cools, we might actually return to buying shoes because we <em>like</em> them, not because they'll appreciate in value. The death of sneaker speculation could be the rebirth of genuine sneaker culture.</p>
<p>Maybe we'll start wearing our kicks instead of keeping them in plastic boxes. What a concept.</p>""",
        "tags": "sneaker culture,streetwear,fashion opinion,footwear,hype",
        "image": "https://images.unsplash.com/photo-1552346154-21d32810aba3?w=800&q=80",
    },
    {
        "title": "The Gender Binary in Fashion Is Officially Over",
        "content": """<p>The most exciting thing happening in fashion right now isn't a specific trend — it's the dismantling of the arbitrary line between "men's" and "women's" clothing.</p>
<p>Harry Styles in a Gucci gown. Zendaya in a perfectly tailored suit. Billy Porter closing the red carpet in a tuxedo gown. These aren't stunts — they're the future.</p>
<p>Fashion has always been gender-fluid; we just pretended it wasn't. High heels were invented for men. Pink was a "masculine" color until the 1940s. Skirts and robes have been standard menswear across most cultures throughout history.</p>
<p>What we're witnessing now is fashion returning to its natural state: a form of personal expression unconstrained by outdated rules about which fabrics and silhouettes belong to which gender. And honestly? The clothes are better for it. When designers stop thinking in binary categories, they create more interesting, more creative, more beautiful work.</p>
<p>Wear what makes you feel powerful. That's the only fashion rule worth following.</p>""",
        "tags": "gender fluid fashion,fashion evolution,inclusivity,style opinion",
        "image": "https://images.unsplash.com/photo-1558171813-4c088753af8f?w=800&q=80",
    },
    {
        "title": "Instagram Has Ruined Fashion — But TikTok Might Save It",
        "content": """<p>Instagram turned fashion into a carefully curated performance. Every outfit was styled for the grid, every pose calculated for maximum likes, and authenticity was replaced by aesthetic consistency. Fashion became a content strategy rather than a form of self-expression.</p>
<p>TikTok is different. The platform's raw, unfiltered energy has revived thrift culture, made outfit-of-the-day videos feel genuine again, and democratized fashion advice. A teenager in rural Kansas can build a following based purely on creative styling — no expensive camera, no designer wardrobe, no perfectly curated feed required.</p>
<p>TikTok fashion isn't perfect. Micro-trends burn through cycles at dizzying speed, and the platform's algorithm can trap users in aesthetic echo chambers. But at its best, TikTok fashion feels alive, spontaneous, and wonderfully messy — everything Instagram fashion stopped being years ago.</p>
<p>The fashion industry should be paying attention. The future of style isn't polished — it's real.</p>""",
        "tags": "social media,fashion influence,tiktok,instagram,digital fashion",
        "image": "https://images.unsplash.com/photo-1529139574466-a303027c1d8b?w=800&q=80",
    },
    {
        "title": "Unpopular Opinion: Designer Logos Are Tacky Again",
        "content": """<p>We've come full circle. After years of logomania — Gucci belts, Louis Vuitton monograms, Balenciaga everything — the pendulum is swinging back. And honestly? It's about time.</p>
<p>There was a moment when wearing a logo felt subversive, ironic, almost punk. Dapper Dan remixing luxury logos in 1980s Harlem was cultural commentary. But when every suburban mall has a Gucci store and every influencer is gifted the same monogrammed bag, the rebellion is over.</p>
<p>The most stylish people I know have moved past logos entirely. They're wearing independent designers, vintage pieces, and custom-tailored garments that don't need a brand name to prove their worth.</p>
<p>True luxury is not needing to advertise. When your clothes speak for themselves through cut, fabric, and fit, you don't need a logo to do the talking. Let the garment be the star — not the brand behind it.</p>""",
        "tags": "designer logos,fashion opinion,logomania,luxury debate",
        "image": "https://images.unsplash.com/photo-1445205170230-053b83016050?w=800&q=80",
    },
    {
        "title": "Fashion Weeks Need a Reality Check",
        "content": """<p>Four cities. Hundreds of shows. Thousands of flights. Millions of dollars. And for what? Collections that most people will never wear, shown to audiences that most people will never be part of.</p>
<p>Fashion Week was created in a world without the internet, when buyers and press needed to physically see collections to write about and order them. That world doesn't exist anymore. We have livestreams, digital showrooms, and AI-generated lookbooks.</p>
<p>The environmental cost alone should give us pause. Flying editors, models, photographers, and entire production teams across four continents in six weeks produces a carbon footprint that makes a mockery of any sustainability pledge these same brands make.</p>
<p>Imagine if the industry redirected even half of Fashion Week's budget toward paying garment workers fairly, investing in sustainable materials, or making design education more accessible. The fashion world would be transformed — and the clothes would still be just as beautiful.</p>
<p>Fashion weeks should evolve or step aside. The spectacle served its purpose. Now it's time for something better.</p>""",
        "tags": "fashion week,industry critique,sustainability,fashion opinion",
        "image": "https://images.unsplash.com/photo-1509631179647-0177331693ae?w=800&q=80",
    },
    {
        "title": "The Return of Maximalism: More is More and I'm Here For It",
        "content": """<p>After years of "clean girl aesthetic" and minimalist wardrobes in 47 shades of beige, maximalism is making a glorious comeback. And the fashion world is all the better for it.</p>
<p>Maximalism isn't about being loud for the sake of being loud. It's about joy. It's about walking into a room and making it more interesting just by being there. It's about choosing the printed jacket instead of the plain one, the statement earrings instead of the studs, the bold lip instead of the nude.</p>
<p>History's most iconic fashion moments were maximalist: Diana Ross in sequins, Prince in purple, Iris Apfel in everything. These people understood that fashion is performance, and the world is your stage.</p>
<p>So layer those necklaces. Clash those prints. Wear the feathered coat to the grocery store. Life is too short for beige — and your wardrobe should reflect that.</p>""",
        "tags": "maximalism,bold fashion,style philosophy,fashion trend,opinion",
        "image": "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=800&q=80",
    },
    {
        "title": "The Fashion Industry's Size Inclusivity Is Still Performative",
        "content": """<p>Every major brand has released a "body positive" campaign in the last five years. And yet, walk into most luxury stores and you'll struggle to find anything above a size 12. The disconnect between marketing and reality is staggering.</p>
<p>True size inclusivity isn't a capsule collection or a social media campaign — it's making your entire range available in sizes 00 through 30 as standard practice. It's using models of all sizes in your campaigns year-round, not just during "inclusivity" months. It's designing for diverse bodies from the start, not grading up a size 2 pattern and calling it plus-size.</p>
<p>Brands like Universal Standard, Girlfriend Collective, and Chromat are proving that designing for all bodies isn't just ethical — it's profitable. The extended-size market is worth over $28 billion. Ignoring it isn't a design choice; it's a business failure.</p>
<p>Until every body can walk into any store and find beautiful, well-made clothes that fit — not just "exist" in their size — the industry's inclusivity claims remain what they are: performance.</p>""",
        "tags": "size inclusivity,body positivity,fashion industry,representation,opinion",
        "image": "https://images.unsplash.com/photo-1483985988355-763728e1935b?w=800&q=80",
    },
    {
        "title": "Your Personal Style Matters More Than Any Trend Report",
        "content": """<p>Here's the most important fashion advice you'll ever receive: stop chasing trends and start building a personal style.</p>
<p>Trends are manufactured urgency. They exist to sell you things you don't need by making you feel like what you already own is somehow inadequate. The "coastal grandmother" aesthetic of 2023 became the "mob wife" aesthetic of 2024 which became whatever micro-trend is dominating your feed right now. It's exhausting, expensive, and ultimately empty.</p>
<p>Personal style is the opposite. It's understanding what colors make your skin glow, what silhouettes make you feel powerful, what fabrics make you feel luxurious. It's a wardrobe that evolves slowly, intentionally, and in harmony with who you actually are — not who TikTok says you should be this week.</p>
<p>The best-dressed people in history — from Coco Chanel to André Leon Talley to your impossibly chic grandmother — didn't follow trends. They established them by knowing exactly who they were and dressing accordingly.</p>
<p>Build your style like you build your character: authentically, patiently, and without apology. The trends will always be there. Your identity is what makes fashion worth caring about.</p>""",
        "tags": "personal style,fashion advice,authenticity,style philosophy,opinion",
        "image": "https://images.unsplash.com/photo-1469334031218-e382a71b716b?w=800&q=80",
    },
]


def seed():
    with app.app_context():
        user = get_or_create_seed_user()
        now = datetime.utcnow()

        # ── Blog Posts ──────────────────────────────
        existing_blog = Post.query.filter_by(section='blog', user_id=user.id).count()
        if existing_blog >= 10:
            print(f"[INFO] Blog already has {existing_blog} posts from seed user -- skipping.")
        else:
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
            print(f"[OK] Seeded {len(BLOG_POSTS)} blog posts.")

        # ── Tips ────────────────────────────────────
        existing_tips = Tip.query.filter_by(user_id=user.id).count()
        if existing_tips >= 10:
            print(f"[INFO] Tips already has {existing_tips} entries from seed user -- skipping.")
        else:
            for i, data in enumerate(TIPS):
                tip = Tip(
                    title=data["title"],
                    content=data["content"],
                    category=data["category"],
                    tags=data["tags"],
                    image=data["image"],
                    user_id=user.id,
                    created_at=now - timedelta(days=len(TIPS) - i),
                )
                db.session.add(tip)
                db.session.flush()

                # Set subtitle
                try:
                    db.session.execute(
                        text("UPDATE tip SET subtitle = :subtitle WHERE id = :id"),
                        {"subtitle": data["subtitle"], "id": tip.id},
                    )
                except Exception:
                    pass  # subtitle column might not exist

            db.session.commit()
            print(f"[OK] Seeded {len(TIPS)} tips (5 fashion + 5 photography).")

        # ── Daily Scoops ────────────────────────────
        existing_scoops = Post.query.filter_by(section='daily_scoops', user_id=user.id).count()
        if existing_scoops >= 10:
            print(f"[INFO] Daily Scoops already has {existing_scoops} posts from seed user -- skipping.")
        else:
            for i, data in enumerate(DAILY_SCOOPS):
                post = Post(
                    title=data["title"],
                    content=data["content"],
                    image=data["image"],
                    tags=data["tags"],
                    section="daily_scoops",
                    user_id=user.id,
                    created_at=now - timedelta(days=len(DAILY_SCOOPS) - i),
                )
                db.session.add(post)
            db.session.commit()
            print(f"[OK] Seeded {len(DAILY_SCOOPS)} daily scoops.")

        print("\n=== All content seeded successfully! ===")
        print(f"   Blog posts:   {Post.query.filter_by(section='blog').count()}")
        print(f"   Tips:          {Tip.query.count()}")
        print(f"   Daily Scoops: {Post.query.filter_by(section='daily_scoops').count()}")


if __name__ == "__main__":
    seed()
