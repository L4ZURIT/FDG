import json

class JSONm():
    
    @staticmethod
    def read(path:str)->dict:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data

    @staticmethod
    def write(path:str, new_data:dict):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(new_data, f)
            


def main():

    print(JSONm.read("data/connections/sqlite.json"))

    pass


if __name__ == '__main__':
    main()