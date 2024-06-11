# includes/write_and_read.py

class WriteAndRead:
    def write_to_file(self, file_path, data):
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(data)
        except Exception as e:
            print(f"Error writing to file {file_path}: {e}")

    def read_payloads_one_by_one(self, file_path, scanner):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    payload = line.strip()
                    scanner.brute_force_single_payload(payload)
        except Exception as e:
            print(f"Error reading payloads from file {file_path}: {e}")

    def read_from_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            print(f"Error reading from file {file_path}: {e}")
            return ""
