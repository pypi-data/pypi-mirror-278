def parse(command_output):
    lines = command_output.strip().splitlines()
    headers = [header.strip() for header in lines[0].split()]
    data = []

    for line in lines[1:]:
        values = line.split()
        entry = {headers[i]: values[i] for i in range(len(values))}
        data.append(entry)

    return data
