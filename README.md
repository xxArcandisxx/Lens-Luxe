# Lens&Luxe - Fashion & Lifestyle Blog

A modern, elegant fashion blog website showcasing the perfect blend of burgundy and ivory aesthetics.

## 📋 Project Overview

Lens&Luxe is a professional fashion and lifestyle blog designed to capture style, celebrate elegance, and share luxury living insights. The website features a clean, modern design with a sophisticated color palette.

## 🎨 Design Specifications

### Color Palette
- **Primary Color (Burgundy):** #800020
- **Primary Dark:** #400010
- **Primary Light:** #a0003a
- **Accent Color (Ivory):** #fffef9
- **Accent Light:** #fffaf0
- **Dark Text:** #2a2a2a

### Features
- Responsive design (mobile-friendly)
- Smooth scrolling navigation
- Featured blog posts section
- Image gallery with interactive lightbox
- Newsletter subscription form
- Contact form
- Smooth animations and transitions
- Social media links
- Professional footer

## 📁 File Structure

```
Lens&Luxe/
├── index.html      # Main HTML file
├── styles.css      # Complete styling with responsive design
├── script.js       # JavaScript for interactivity
└── README.md       # Project documentation
```

## 🚀 Getting Started

### Prerequisites
- A modern web browser (Chrome, Firefox, Safari, Edge)
- A text editor or IDE (VS Code recommended)

### Installation

1. Clone or download the project
```bash
git clone https://github.com/xxArcandisxx/Lens-Luxe.git
cd Lens-Luxe
```

2. Open in browser
Simply open `index.html` in your web browser or use a local server:

```bash
# Using Python 3
python -m http.server 8000

# Using Python 2
python -m SimpleHTTPServer 8000

# Using Node.js (if you have http-server installed)
http-server
```

Then navigate to `http://localhost:8000` in your browser.

## 📱 Sections

### 1. Navigation Bar
- Sticky navigation with smooth scrolling
- Logo branding
- Quick links to all main sections

### 2. Hero Section
- Eye-catching gradient background
- Compelling headline
- Call-to-action button

### 3. Featured Stories
- Blog post cards with images
- Post metadata (date, title, excerpt)
- "Read More" links
- Hover animations

### 4. Gallery Section
- Visual gallery grid
- Interactive lightbox feature
- Gradient backgrounds

### 5. About Section
- Blog description
- Key statistics
- Mission statement

### 6. Newsletter Section
- Email subscription form
- Engaging call-to-action

### 7. Contact Section
- Contact information
- Contact form for inquiries

### 8. Footer
- Social media links
- Quick navigation
- Copyright information

## 🛠️ Customization

### Adding Blog Posts
Edit the `.posts-grid` section in `index.html` to add new post cards:

```html
<article class="post-card">
    <div class="post-image" style="background: [your-gradient];"></div>
    <div class="post-content">
        <span class="post-date">Your Date</span>
        <h3>Your Title</h3>
        <p>Your excerpt</p>
        <a href="#" class="read-more">Read More →</a>
    </div>
</article>
```

### Changing Colors
Modify the CSS variables in `styles.css`:

```css
:root {
    --primary: #800020;        /* Change burgundy */
    --accent: #fffef9;         /* Change ivory */
    /* ... */
}
```

### Adding Gallery Images
Replace the gradient backgrounds in the gallery section with image URLs:

```html
<div class="gallery-item" style="background-image: url('your-image.jpg');"></div>
```

## 📧 Contact Form Integration

To make the contact and newsletter forms functional, integrate with:
- **EmailJS** - For client-side email sending
- **Formspree** - For form submission backend
- **Web3 Forms** - Modern form backend

## 🔗 Deployment

### Deploy to Netlify
1. Connect your GitHub repository
2. Set build command: (none needed - static site)
3. Set publish directory: `/`
4. Deploy!

### Deploy to Vercel
1. Import your GitHub repository
2. Configure settings and deploy

### Deploy to GitHub Pages
1. Push to GitHub
2. Enable GitHub Pages in repository settings
3. Select `main` branch as source

## 📱 Browser Compatibility

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## 🎯 Future Enhancements

- [ ] Integrate actual blog backend
- [ ] Add user authentication
- [ ] Implement search functionality
- [ ] Add comment system
- [ ] Create admin dashboard
- [ ] Add image optimization
- [ ] Implement PWA features
- [ ] Add multi-language support

## 📄 License

This project is open source and available for personal and commercial use.

## 👤 Author

Lens&Luxe Team

## 🤝 Contributing

Contributions are welcome! Feel free to submit pull requests or open issues for improvements.

---

**Made with ❤️ for fashion enthusiasts and luxury lifestyle lovers.**
