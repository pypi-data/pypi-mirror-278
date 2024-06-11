import json

def parse(command_output):
    lines = command_output.strip().split('\n')
    headers = lines[0].split()
    memory_data = []

    for line in lines[1:]:
        values = line.split()
        # Ensure that the length of headers and values are the same
        if len(values) == len(headers):
            entry = {headers[i]: values[i] for i in range(len(headers))}
        else:
            # Handle cases where the line might not match header length
            entry = {}
            for i in range(len(values)):
                key = headers[i] if i < len(headers) else f'unknown_{i}'
                entry[key] = values[i]
        memory_data.append(entry)

    return json.dumps(memory_data, indent=2)

