import unittest
import os
import re
import json
import tempfile
import datetime

# Mocking configuration for the test
BLOG_REPO_PATH = ""

def insert_post_into_index_html(content, location="南京", blog_repo_path=None):
    html_path = os.path.join(blog_repo_path, "index.html")
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    escaped_content = json.dumps(content, ensure_ascii=False)
    new_item = f'            {{ date: "{now_str}", location: "{location}", content: {escaped_content} }},'
    
    marker = "const posts = ["
    if marker in html_content:
        parts = html_content.split(marker, 1)
        updated_content = parts[0] + marker + "\n" + new_item + parts[1]
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(updated_content)
        return True, now_str
    else:
        match = re.search(r'const\s+posts\s*=\s*\[', html_content)
        if match:
            matched_str = match.group(0)
            parts = html_content.split(matched_str, 1)
            updated_content = parts[0] + matched_str + "\n" + new_item + parts[1]
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(updated_content)
            return True, now_str
        return False, None

class TestPyBotHTMLInsertion(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory and a mock index.html
        self.test_dir = tempfile.TemporaryDirectory()
        self.mock_html = os.path.join(self.test_dir.name, "index.html")
        
        self.sample_html = """<!DOCTYPE html>
<html>
<body>
    <script>
        const posts = [
            { date: "2026-07-08 10:30", location: "南京", content: "今天把个人博客和微博" }
        ];
    </script>
</body>
</html>"""
        with open(self.mock_html, "w", encoding="utf-8") as f:
            f.write(self.sample_html)

    def tearDown(self):
        self.test_dir.cleanup()

    def test_insertion_normal(self):
        post_content = '这是一个测试内容，包含"双引号"和\n换行符！'
        success, timestamp = insert_post_into_index_html(post_content, "北京", self.test_dir.name)
        
        self.assertTrue(success)
        
        with open(self.mock_html, "r", encoding="utf-8") as f:
            updated_html = f.read()
            
        # Verify the new item is present and correctly escaped
        self.assertIn(f'date: "{timestamp}"', updated_html)
        self.assertIn('location: "北京"', updated_html)
        # Check that content is correctly serialized as JSON string inside JS object
        escaped_expected = json.dumps(post_content, ensure_ascii=False)
        self.assertIn(f'content: {escaped_expected}', updated_html)
        
        # Verify const posts structure still holds and parses
        self.assertIn("const posts = [", updated_html)
        self.assertIn('{ date: "2026-07-08 10:30"', updated_html)

if __name__ == "__main__":
    unittest.main()
