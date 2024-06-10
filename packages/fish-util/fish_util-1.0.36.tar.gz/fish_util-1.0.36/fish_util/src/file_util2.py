def write_file(file_path, file_content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(file_content)
    print('File saved to', file_path)

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        file_content = file.read()
    return file_content

def clear_file(file_path):
    open(file_path, 'w', encoding='utf-8').close()
    # print('File cleared:', file_path)

def main():
    print(__file__)
    file_path = '/Users/yutianran/Documents/MyPKM/test.md'
    print(read_file(file_path))
    clear_file(file_path)
    print(read_file(file_path))


if __name__ == "__main__":
    main()