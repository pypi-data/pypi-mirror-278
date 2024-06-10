def find_paths_by_key(data, input_key):
    paths = []

    def recurse(data, path):
        if isinstance(data, dict):
            for key, value in data.items():
                new_path = path + [key]
                if key == input_key:
                    paths.append(new_path)
                recurse(value, new_path)
        elif isinstance(data, list):
            for index, item in enumerate(data):
                recurse(item, path + [index])

    recurse(data, [])

    # 중복 경로 제거를 위한 집합
    unique_paths = set()
    results = []

    for path in paths:
        formatted_path = ''.join([f'["{item}"]' if isinstance(item, str) else f"[{item}]" for item in path])
        result = f"data{formatted_path}"
        if result not in unique_paths:
            unique_paths.add(result)
            results.append(result)

    return results


def find_paths_by_value(data, input_value):
    paths = []

    def recurse(data, path):
        if isinstance(data, dict):
            for key, value in data.items():
                if value == input_value:
                    paths.append(path + [key])
                recurse(value, path + [key])
        elif isinstance(data, list):
            for index, item in enumerate(data):
                recurse(item, path + [index])
        else:
            if data == input_value:
                paths.append(path)

    recurse(data, [])

    # 중복 경로 제거를 위한 집합
    unique_paths = set()
    results = []

    for path in paths:
        formatted_path = ''.join([f'["{item}"]' if isinstance(item, str) else f"[{item}]" for item in path])
        result = f"data{formatted_path}"
        if result not in unique_paths:
            unique_paths.add(result)
            results.append(result)

    return results

