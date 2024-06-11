class URLReader:
    def read_urls_one_by_one(self, file_path, scanner):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    url = line.strip()
                    scanner.add_url(url)
        except Exception as e:
            print(f"Error reading URLs from file {file_path}: {e}")
