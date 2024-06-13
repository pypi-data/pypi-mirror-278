class FileUtil:

    @staticmethod
    def generate_file(file_path: str, content: str):
        with open(file_path, 'w+', encoding='utf-8') as f:
            f.write(content)
