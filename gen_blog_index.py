import os
import re
import json

# Read the blog posts from a JSON file
with open('blog_posts.json', 'r') as f:
    blog_posts = json.load(f)

# Create the index.html content
index_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Blog Index</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
        <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
    
      gtag('config', 'G-P7D0WEMF23');
    </script>
</head>
<body class="bg-gray-50 text-gray-800 font-roboto">
    <header class="bg-blue-600 text-white py-8 text-center">
        <h1 class="text-4xl font-bold">Blog Posts Index</h1>
        <p class="mt-2 text-lg">Explore all our blog posts below.</p>
    </header>
    <main class="container mx-auto py-10">
        <h2 class="text-2xl font-semibold mb-6">All Blog Posts</h2>
        <ul class="list-disc pl-5 space-y-3">
"""

# Create the blog folder if it doesn't exist
if not os.path.exists('blog'):
    os.makedirs('blog')

# Loop through the blog posts and generate links
for post in blog_posts:
    # Create a filename from the title, preserving underscores
    title = post['title'].replace(' ', '_').lower()
    clean_title = re.sub(r'[^a-zA-Z0-9_\s]', '', title)

    # Create the link to the post
    file_name = f"{clean_title}.html"
    index_content += f'            <li><a href="{file_name}" class="text-blue-600 hover:underline">{post["title"]}</a></li>\n'

index_content += """        </ul>
    </main>        
    </footer>

        <footer class="bg-gray-900 text-white py-6">
        <div class="container">
        <p>&copy; 2024 sup.sg.  All rights reserved.</p>
            <ul class="flex justify-center space-x-4">
                <li><a href="#" class="text-gray-400">Privacy Policy</a></li>
                <li><a href="#" class="text-gray-400">Terms of Service</a></li>
                <li><a href="https://discord.gg/kwSqTYneRT" class="text-gray-400">Contact</a></li>
                <li><a href="../links.html" class="text-gray-400">Links</a></li>
                <li><a href="../sitemap.html" class="text-gray-400">Sitemap</a></li>
            </ul>
        </div>
    </footer>

</body>
</html>
"""

# Write the index.html file to the blog directory
with open('blog/index.html', 'w') as f:
    f.write(index_content)

print("Generated blog index.html with links to all posts.")
