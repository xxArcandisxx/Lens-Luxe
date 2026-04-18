import os
import glob

template_dir = r"c:\Users\aksha\OneDrive\Desktop\Lens&Luxe\templates"
files = glob.glob(os.path.join(template_dir, "*.html"))

for file_path in files:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    if "{{ url_for('home') }}#blog" in content:
        new_content = content.replace("{{ url_for('home') }}#blog", "{{ url_for('blog') }}")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Updated {os.path.basename(file_path)}")
