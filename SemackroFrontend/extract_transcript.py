import json

found_contents = []

with open('/home/dilmer/.gemini/antigravity/brain/215d44a8-f6d3-40a4-96b5-e04492017e55/.system_generated/logs/transcript_full.jsonl', 'r') as f:
    for line in f:
        try:
            data = json.loads(line)
            if 'tool_calls' in data:
                for tc in data['tool_calls']:
                    # if we did a view_file on Reportes.html
                    if tc.get('name') == 'view_file' and 'Reportes.html' in str(tc.get('arguments', {})):
                        # Look at the next steps for the response? Actually tool responses are in a separate step or part of the same?
                        pass
            
            # Since tool responses aren't easily linked, let's just search all content fields for something unique to Reportes.html
            content = data.get('content', '')
            if isinstance(content, str) and 'idRolEditandoPermisos' in content and '<!DOCTYPE html>' in content:
                found_contents.append(content)
        except:
            pass

if found_contents:
    with open('Reportes_recovered.html', 'w') as out:
        out.write(found_contents[0])
    print("Recovered from transcript!")
else:
    print("Not found in transcript_full.jsonl")
