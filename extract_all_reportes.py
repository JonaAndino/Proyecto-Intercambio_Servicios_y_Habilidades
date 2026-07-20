import json

found = []
with open('/home/dilmer/.gemini/antigravity/brain/215d44a8-f6d3-40a4-96b5-e04492017e55/.system_generated/logs/transcript_full.jsonl', 'r') as f:
    for line in f:
        try:
            data = json.loads(line)
            # look for any step that contains the text of the html
            if data.get('type') == 'TOOL_RESPONSE':
                content = str(data.get('content', ''))
                if '<!DOCTYPE html>' in content and 'abrirModalEditarPermisos' in content:
                    found.append(content)
        except Exception as e:
            pass

print(f"Found {len(found)} instances of Reportes.html in the transcript!")
if found:
    with open('SemackroFrontend/Reportes_from_transcript.txt', 'w') as out:
        out.write(found[0])
