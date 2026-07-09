import os
import re

def reset_blog():
    html_path = "index.html"
    if not os.path.exists(html_path):
        print(f"❌ 找不到 {html_path} 文件")
        return

    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 正则替换：匹配 const posts = [...] 结构并置空
    # [\s\S]*? 匹配包括换行符在内的任意字符，懒惰模式
    new_content = re.sub(
        r'(const\s+posts\s*=\s*\[)([\s\S]*?)(\];)',
        r'\1\n        ];',
        content
    )

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    
    print("✅ 已成功重置博客数据，清空了 posts 数组。")

if __name__ == "__main__":
    confirm = input("⚠️  此操作将永久删除 index.html 中的所有历史文章数据，确定要继续吗？(y/n): ")
    if confirm.lower() == 'y':
        reset_blog()
    else:
        print("❌ 操作已取消。")
