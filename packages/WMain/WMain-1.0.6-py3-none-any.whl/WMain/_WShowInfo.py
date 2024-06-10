import os

if __name__ == '__main__':
    char_num = 0
    line_num = 0
    path = os.getcwd()
    path = "D:\py_project"
    for root, dirs, files in os.walk(path):
        for file in files:
            file = os.path.join(root, file)
            if os.path.isfile(file) and file.endswith('.py'):
                with open(file, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            char_num += len(line)
                            line_num += 1
    print('Total characters:', char_num)
    print('Total lines:', line_num)