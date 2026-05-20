import os

def fix_base_html():
    file_path = "templates/base.html"
    print(f"Reading {file_path}...")
    
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    new_lines = []
    skip_next = False
    
    for i, line in enumerate(lines):
        if skip_next:
            skip_next = False
            continue
            
        # Target the specific problematic split line
        if '{% if user.is_superuser %}Administrator{% else %}Staff{% endif' in line and lines[i+1].strip().startswith('%}'):
            print(f"Found target lines at {i+1} and {i+2}")
            # Combine them
            combined = '                        <p class="text-xs text-slate-500">{% if user.is_superuser %}Administrator{% else %}Staff{% endif %}</p>\n'
            new_lines.append(combined)
            skip_next = True # Skip the next line which is just "%}</p>"
        else:
            new_lines.append(line)
            
    print(f"Writing back {file_path}...")
    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
    print("Done.")

if __name__ == "__main__":
    fix_base_html()
