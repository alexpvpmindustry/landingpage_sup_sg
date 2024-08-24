import os
import json

# HTML Template with Tailwind CSS via CDN, including previous/next links
html_template = """
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{description}">
    <meta name="keywords" content="{keywords}">
    <meta name="ahrefs-site-verification" content="386d4d2b557943129417428c3267b66e72d0a9a903b4ff02bee651e823bbb220">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-P7D0WEMF23"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
    
      gtag('config', 'G-P7D0WEMF23');
    </script>
</head>

<body class="bg-gray-100 font-inter">

    <header class="bg-white shadow-sm">
        <div class="container mx-auto p-6">
            <h1 class="text-3xl font-bold text-gray-900">{title}</h1>
            <p class="text-gray-700 mt-2">{subtitle}</p>
            <p class="mt-4 text-blue-500"><a href="../choose_your_own_adventure.html">Choose Your Own Adventure</a></p>
        </div>
    </header>

    <section id="about" class="bg-white py-10">
        <div class="container mx-auto px-6">
            <h2 class="text-2xl font-semibold text-gray-900 mb-4">About {title}</h2>
            <p class="text-gray-700">{about}</p>
        </div>
    </section>

    <section id="articles" class="py-10">
        <div class="container mx-auto px-6">
            <h2 class="text-2xl font-semibold text-gray-900 mb-4">Expert Articles on {title}</h2>
            <div class="space-y-4">
                {content}
            </div>
        </div>
    </section>

    <section id="pagination" class="py-6">
        <div class="container mx-auto flex justify-between">
            {prev_link}
            {next_link}
        </div>
    </section>

    <section id="contact" class="bg-white py-10">
        <div class="container mx-auto px-6">
            <h2 class="text-2xl font-semibold text-gray-900 mb-4">Contact Us</h2>
            <p class="text-gray-700"><strong>Email:</strong> <a href="mailto:info@sup.sg" class="text-blue-500">info@sup.sg</a></p>
            <p class="text-gray-700"><strong>Follow Us:</strong></p>
            <ul class="mt-4 space-y-2">
                <li><a href="https://discord.gg/kwSqTYneRT" class="text-blue-500">Twitter</a></li>
                <li><a href="https://discord.gg/kwSqTYneRT" class="text-blue-500">LinkedIn</a></li>
            </ul>
        </div>
    </section>

    <section id="cta" class="bg-blue-500 text-white py-10">
        <div class="container mx-auto px-6 text-center">
            <h2 class="text-2xl font-semibold">Subscribe Now</h2>
            <p class="mt-4">Stay informed with cutting-edge articles in <strong>cryptocurrencies, AI, fintech, and science</strong>.</p>
            <a href="#" class="mt-6 inline-block bg-white text-blue-500 font-semibold py-2 px-4 rounded shadow-md">Subscribe</a>
        </div>
    </section>

    <footer class="bg-gray-900 text-white py-6">
        <div class="container mx-auto px-6">
            <ul class="flex justify-center space-x-4">
                <li><a href="https://discord.gg/kwSqTYneRT" class="text-gray-400">Privacy Policy</a></li>
                <li><a href="https://discord.gg/kwSqTYneRT" class="text-gray-400">Terms of Service</a></li>
                <li><a href="https://discord.gg/kwSqTYneRT" class="text-gray-400">Contact</a></li>
                <li><a href="../links.html" class="text-gray-400">Links</a></li>
                <li><a href="../sitemap.html" class="text-gray-400">Sitemap</a></li>
            </ul>
        </div>
    </footer>

</body>

</html>
"""

# Function to generate HTML pages with previous/next links
def generate_html_pages(blog_data):
    if not os.path.exists('blog'):
        os.makedirs('blog')

    total_posts = len(blog_data)
    
    for i, post in enumerate(blog_data):
        # Join paragraphs into a single HTML string
        content_html = "".join([f"<p>{para}</p>" for para in post['content']])

        # Previous and next links
        prev_link = f'<a href="{blog_data[i-1]["title"].replace(" ", "_").lower()}.html" class="text-blue-500">Previous Post</a>' if i > 0 else ""
        next_link = f'<a href="{blog_data[i+1]["title"].replace(" ", "_").lower()}.html" class="text-blue-500">Next Post</a>' if i < total_posts - 1 else ""
        
        # Format the HTML template with the blog post data and links
        html_content = html_template.format(
            title=post['title'],
            description=post.get('description', 'Explore insights on cryptocurrencies, AI, fintech, and science in Singapore.'),
            keywords=post.get('keywords', 'cryptocurrencies, AI, fintech, science'),
            subtitle=post.get('subtitle', 'Discover insights on cutting-edge topics in Singapore.'),
            about=post.get('about', 'Your premier source for expert-driven content on the latest trends in Singapore.'),
            content=content_html,
            prev_link=prev_link,
            next_link=next_link
        )

        # Create the HTML file in the 'blog' directory
        file_name = f"blog/{post['title'].replace(' ', '_').lower()}.html"
        with open(file_name, 'w') as file:
            file.write(html_content)

        print(f"Generated: {file_name}")

# Read blog posts from the JSON file
with open('blog_posts.json', 'r') as f:
    blog_posts = json.load(f)

# Generate HTML pages
generate_html_pages(blog_posts)
