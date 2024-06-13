def parse(command_output):
    lines = command_output.splitlines()
    data = []
    headers = []

    # Extract headers from the first line
    if lines:
        headers = [header.strip() for header in lines[0].split() if header.strip()]
        lines = lines[1:]

    for line in lines:
        if not line.strip():  # Skip empty lines
            continue

        values = [value.strip() for value in line.split() if value.strip()]
        if len(values) != len(headers):
            # For handling lines with different formats (like summary lines)
            data.append({headers[0]: " ".join(values)})
        else:
            entry = {headers[i]: values[i] for i in range(len(headers))}
            data.append(entry)

    return data

