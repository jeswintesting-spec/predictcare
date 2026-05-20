
import re
import os

file_path = 'templates/base.html'

with open(file_path, 'r') as f:
    content = f.read()

# Regex to find the broken tag which spans multiple lines
# Pattern: {% if user.is_superuser %}...{% endif [newline] %}
pattern = r'(\{% if user\.is_superuser %\}.*?\{% endif)\s+(%\})'

# Replacement: Join them
fixed_content = re.sub(pattern, r'\1 \2', content, flags=re.DOTALL)

# Also ensure it's explicitly single lined if regex misses
fixed_content = fixed_content.replace(
    "{% if user.is_superuser %}Administrator{% else %}Staff{% endif\n                            %}",
    "{% if user.is_superuser %}Administrator{% else %}Staff{% endif %}"
)

if content != fixed_content:
    print("Found and fixed broken tag.")
    with open(file_path, 'w') as f:
        f.write(fixed_content)
else:
    print("No broken tag found matching patterns.")

