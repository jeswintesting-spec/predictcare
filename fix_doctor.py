import re
with open('templates/dashboards/doctor_specialized.html', 'r') as f:
    content = f.read()

# Replace the broken tags
new_content = re.sub(
    r'<td class="p-3 text-sm text-gray-600 max-w-xs truncate" title="\{\{ visit\.medicines \}\}">\s*\{\{\s*visit\.medicines\s*\}\}\s*</td>',
    '<td class="p-3 text-sm text-gray-600 max-w-xs truncate" title="{{ visit.medicines }}">\n                            {{ visit.medicines }}\n                        </td>',
    content
)

new_content = re.sub(
    r'<td class="p-3 text-sm text-gray-600 max-w-xs truncate" title="\{\{ visit\.symptoms \}\}">\s*\{\{\s*visit\.symptoms\s*\}\}\s*</td>',
    '<td class="p-3 text-sm text-gray-600 max-w-xs truncate" title="{{ visit.symptoms }}">\n                            {{ visit.symptoms }}\n                        </td>',
    new_content
)

with open('templates/dashboards/doctor_specialized.html', 'w') as f:
    f.write(new_content)
