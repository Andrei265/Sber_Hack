import json

def new_json(file_path : str, content : dict) -> None: # Запись в JSON файл без сохранение старого содержимого
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(content, file, ensure_ascii=False, indent=3)

def add_json(file_path : str, content : list) -> None: # Запись в JSON файл с сохранение старого содержимого
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            old_content = json.load(file)
    except Exception:
        print(f"File {file_path} don`t exist")
        old_content = []
    
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(content + old_content , file, ensure_ascii=False, indent=3)

def read_json(file_path : str) -> list or dict:
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def main():
    pass

if __name__ == '__main__': 
    main()

print(f'{__name__} is here !')