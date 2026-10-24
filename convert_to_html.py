#!/usr/bin/env python3
"""
Convert all markdown files to HTML with embedded images and create index.html
"""

import os
import re
import base64
import markdown
from pathlib import Path
from urllib.parse import unquote
import mimetypes

class MarkdownToHTMLConverter:
    def __init__(self, root_dir):
        self.root_dir = Path(root_dir)
        self.converted_files = []
        self.failed_files = []
        
    def get_mime_type(self, file_path):
        """Get MIME type for a file"""
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type is None:
            # Default based on extension
            ext = file_path.suffix.lower()
            mime_types = {
                '.png': 'image/png',
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.gif': 'image/gif',
                '.svg': 'image/svg+xml',
                '.webp': 'image/webp'
            }
            mime_type = mime_types.get(ext, 'application/octet-stream')
        return mime_type
    
    def image_to_base64(self, image_path):
        """Convert image to base64 data URI"""
        try:
            with open(image_path, 'rb') as img_file:
                img_data = img_file.read()
                mime_type = self.get_mime_type(image_path)
                base64_data = base64.b64encode(img_data).decode('utf-8')
                return f"data:{mime_type};base64,{base64_data}"
        except Exception as e:
            print(f"Warning: Could not encode image {image_path}: {e}")
            return None
    
    def resolve_image_path(self, md_file_path, img_ref):
        """Resolve image path relative to markdown file"""
        md_dir = md_file_path.parent
        
        # Clean up the image reference
        img_ref = unquote(img_ref)
        
        # Try different path resolutions
        possible_paths = [
            md_dir / img_ref,  # Relative to markdown file
            self.root_dir / img_ref,  # Relative to root
            self.root_dir / img_ref.lstrip('./'),  # Remove leading ./
        ]
        
        for path in possible_paths:
            if path.exists() and path.is_file():
                return path
        
        return None
    
    def embed_images_in_markdown(self, md_content, md_file_path):
        """Replace image references with base64 embedded data"""
        # Pattern to match markdown images: ![alt](path)
        img_pattern = r'!\[([^\]]*)\]\(([^\)]+)\)'
        
        def replace_image(match):
            alt_text = match.group(1)
            img_path = match.group(2)
            
            # Skip if already a data URI or external URL
            if img_path.startswith('data:') or img_path.startswith('http'):
                return match.group(0)
            
            resolved_path = self.resolve_image_path(md_file_path, img_path)
            
            if resolved_path:
                base64_uri = self.image_to_base64(resolved_path)
                if base64_uri:
                    return f'![{alt_text}]({base64_uri})'
            
            # If image not found or couldn't encode, keep original
            return match.group(0)
        
        return re.sub(img_pattern, replace_image, md_content)
    
    def update_markdown_links(self, content, current_file_path):
        """Update markdown links from .md to .html"""
        # Pattern to match markdown links: [text](path.md)
        link_pattern = r'\[([^\]]+)\]\(([^\)]+\.md)\)'
        
        def replace_link(match):
            link_text = match.group(1)
            link_path = match.group(2)
            
            # Skip external URLs
            if link_path.startswith('http'):
                return match.group(0)
            
            # Convert .md to .html
            html_path = link_path.replace('.md', '.html')
            return f'[{link_text}]({html_path})'
        
        return re.sub(link_pattern, replace_link, content)
    
    def markdown_to_html(self, md_content, title="Document", md_file_path=None):
        """Convert markdown to HTML with styling"""
        # Convert markdown to HTML
        md = markdown.Markdown(extensions=['extra', 'codehilite', 'toc', 'meta'])
        html_body = md.convert(md_content)
        
        # Extract title from meta if available
        if hasattr(md, 'Meta') and 'title' in md.Meta:
            title = md.Meta['title'][0]
        
        # Handle banner image from frontmatter
        banner_html = ""
        if hasattr(md, 'Meta') and 'banner' in md.Meta and md_file_path:
            banner_path = md.Meta['banner'][0]
            resolved_banner = self.resolve_image_path(md_file_path, banner_path)
            if resolved_banner:
                banner_base64 = self.image_to_base64(resolved_banner)
                if banner_base64:
                    banner_html = f'<div class="banner-image"><img src="{banner_base64}" alt="Banner"></div>'
        
        # Create full HTML document with styling
        html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica', 'Arial', sans-serif;
            line-height: 1.6;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
            background-color: #fff;
        }}
        h1, h2, h3, h4, h5, h6 {{
            margin-top: 24px;
            margin-bottom: 16px;
            font-weight: 600;
            line-height: 1.25;
        }}
        h1 {{
            font-size: 2em;
            border-bottom: 1px solid #eaecef;
            padding-bottom: 0.3em;
        }}
        h2 {{
            font-size: 1.5em;
            border-bottom: 1px solid #eaecef;
            padding-bottom: 0.3em;
        }}
        a {{
            color: #0366d6;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        img {{
            max-width: 100%;
            height: auto;
            display: block;
            margin: 20px 0;
        }}
        code {{
            background-color: #f6f8fa;
            padding: 0.2em 0.4em;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            font-size: 85%;
        }}
        pre {{
            background-color: #f6f8fa;
            padding: 16px;
            overflow: auto;
            border-radius: 3px;
        }}
        pre code {{
            background-color: transparent;
            padding: 0;
        }}
        blockquote {{
            border-left: 4px solid #dfe2e5;
            padding-left: 16px;
            color: #6a737d;
            margin: 0;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }}
        table th, table td {{
            border: 1px solid #dfe2e5;
            padding: 6px 13px;
        }}
        table tr:nth-child(2n) {{
            background-color: #f6f8fa;
        }}
        ul, ol {{
            padding-left: 2em;
        }}
        .back-link {{
            display: inline-block;
            margin-bottom: 20px;
            padding: 8px 16px;
            background-color: #f1f3f5;
            border-radius: 4px;
            color: #0366d6;
        }}
        .back-link:hover {{
            background-color: #e1e4e8;
            text-decoration: none;
        }}
        .banner-image {{
            width: 100%;
            max-height: 200px;
            overflow: hidden;
            margin-bottom: 20px;
            border-radius: 8px;
        }}
        .banner-image img {{
            width: 100%;
            height: auto;
            object-fit: cover;
        }}
    </style>
</head>
<body>
    <a href="index.html" class="back-link">← Back to Index</a>
    {banner_html}
    {html_body}
</body>
</html>"""
        return html_template
    
    def convert_file(self, md_file_path):
        """Convert a single markdown file to HTML"""
        try:
            # Read markdown file
            with open(md_file_path, 'r', encoding='utf-8', errors='ignore') as f:
                md_content = f.read()
            
            # Embed images
            md_content = self.embed_images_in_markdown(md_content, md_file_path)
            
            # Update links
            md_content = self.update_markdown_links(md_content, md_file_path)
            
            # Convert to HTML
            title = md_file_path.stem
            html_content = self.markdown_to_html(md_content, title, md_file_path)
            
            # Write HTML file
            html_file_path = md_file_path.with_suffix('.html')
            with open(html_file_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            self.converted_files.append(str(md_file_path.relative_to(self.root_dir)))
            return True
            
        except Exception as e:
            print(f"Error converting {md_file_path}: {e}")
            self.failed_files.append(str(md_file_path.relative_to(self.root_dir)))
            return False
    
    def create_index_html(self):
        """Create a comprehensive index.html with all converted files"""
        # Group files by directory
        files_by_dir = {}
        for file_path in self.converted_files:
            path = Path(file_path)
            dir_name = str(path.parent) if str(path.parent) != '.' else 'Root'
            if dir_name not in files_by_dir:
                files_by_dir[dir_name] = []
            files_by_dir[dir_name].append(path)
        
        # Sort directories
        sorted_dirs = sorted(files_by_dir.keys())
        
        # Build index HTML
        index_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NAMED Repository - HTML Index</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica', 'Arial', sans-serif;
            line-height: 1.6;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
            background-color: #f5f5f5;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            border-radius: 8px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .header h1 {
            margin: 0 0 10px 0;
            font-size: 2.5em;
        }
        .header p {
            margin: 0;
            font-size: 1.1em;
            opacity: 0.9;
        }
        .stats {
            display: flex;
            gap: 20px;
            margin-bottom: 30px;
            flex-wrap: wrap;
        }
        .stat-card {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            flex: 1;
            min-width: 200px;
        }
        .stat-card h3 {
            margin: 0 0 10px 0;
            color: #667eea;
            font-size: 1em;
        }
        .stat-card .number {
            font-size: 2.5em;
            font-weight: bold;
            color: #333;
        }
        .directory-section {
            background: white;
            margin-bottom: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .directory-header {
            background: #667eea;
            color: white;
            padding: 15px 20px;
            font-weight: 600;
            font-size: 1.1em;
            cursor: pointer;
            user-select: none;
        }
        .directory-header:hover {
            background: #5568d3;
        }
        .file-list {
            padding: 15px 20px;
        }
        .file-item {
            padding: 8px 0;
            border-bottom: 1px solid #eee;
        }
        .file-item:last-child {
            border-bottom: none;
        }
        .file-item a {
            color: #0366d6;
            text-decoration: none;
            font-size: 0.95em;
        }
        .file-item a:hover {
            text-decoration: underline;
            color: #0256c4;
        }
        .search-box {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }
        .search-box input {
            width: 100%;
            padding: 12px;
            font-size: 16px;
            border: 2px solid #ddd;
            border-radius: 4px;
            box-sizing: border-box;
        }
        .search-box input:focus {
            outline: none;
            border-color: #667eea;
        }
        .hidden {
            display: none;
        }
    </style>
    <script>
        function searchFiles() {
            const searchTerm = document.getElementById('searchInput').value.toLowerCase();
            const fileItems = document.querySelectorAll('.file-item');
            const dirSections = document.querySelectorAll('.directory-section');
            
            fileItems.forEach(item => {
                const text = item.textContent.toLowerCase();
                if (text.includes(searchTerm)) {
                    item.classList.remove('hidden');
                } else {
                    item.classList.add('hidden');
                }
            });
            
            // Hide empty sections
            dirSections.forEach(section => {
                const visibleItems = section.querySelectorAll('.file-item:not(.hidden)');
                if (visibleItems.length === 0) {
                    section.classList.add('hidden');
                } else {
                    section.classList.remove('hidden');
                }
            });
        }
        
        function toggleDirectory(event) {
            const fileList = event.target.nextElementSibling;
            fileList.classList.toggle('hidden');
        }
    </script>
</head>
<body>
    <div class="header">
        <h1>📚 NAMED Repository - HTML Documentation</h1>
        <p>Comprehensive documentation with embedded images</p>
    </div>
    
    <div class="stats">
        <div class="stat-card">
            <h3>Total Documents</h3>
            <div class="number">""" + str(len(self.converted_files)) + """</div>
        </div>
        <div class="stat-card">
            <h3>Directories</h3>
            <div class="number">""" + str(len(files_by_dir)) + """</div>
        </div>
        <div class="stat-card">
            <h3>Conversion Status</h3>
            <div class="number">✓</div>
        </div>
    </div>
    
    <div class="search-box">
        <input type="text" id="searchInput" placeholder="Search documents..." onkeyup="searchFiles()">
    </div>
    
"""
        
        # Add directory sections
        for dir_name in sorted_dirs:
            files = sorted(files_by_dir[dir_name])
            index_content += f"""    <div class="directory-section">
        <div class="directory-header" onclick="toggleDirectory(event)">
            📁 {dir_name} ({len(files)} files)
        </div>
        <div class="file-list">
"""
            for file_path in files:
                html_path = str(file_path.with_suffix('.html'))
                file_name = file_path.name
                index_content += f"""            <div class="file-item">
                <a href="{html_path}">{file_name}</a>
            </div>
"""
            index_content += """        </div>
    </div>
    
"""
        
        index_content += """</body>
</html>"""
        
        # Write index.html
        index_path = self.root_dir / 'index.html'
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(index_content)
        
        print(f"Created index.html with {len(self.converted_files)} documents")
    
    def convert_all(self):
        """Convert all markdown files in the repository"""
        # Find all markdown files
        md_files = list(self.root_dir.rglob('*.md'))
        
        print(f"Found {len(md_files)} markdown files to convert")
        
        # Convert each file
        for i, md_file in enumerate(md_files, 1):
            if i % 100 == 0:
                print(f"Progress: {i}/{len(md_files)} files converted")
            self.convert_file(md_file)
        
        print(f"\nConversion complete!")
        print(f"Successfully converted: {len(self.converted_files)} files")
        print(f"Failed: {len(self.failed_files)} files")
        
        if self.failed_files:
            print("\nFailed files:")
            for f in self.failed_files[:10]:  # Show first 10
                print(f"  - {f}")
        
        # Create index
        self.create_index_html()

if __name__ == '__main__':
    converter = MarkdownToHTMLConverter('/home/runner/work/named/named')
    converter.convert_all()
