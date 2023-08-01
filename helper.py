import json
from ipaddress import ip_address, IPv4Address
import sqlite3
import requests

class scraper:

    def ipdetails(address):
        try:
            last_semicolon = address.rfind(":")
            if last_semicolon != -1:
                ip = ip_address(address[:last_semicolon])
                port = address[last_semicolon +1 :]
            return ip, port if type(ip_address(ip)) is IPv4Address else False
        except ValueError:
            return False
    
    
    def data2db(data, filename):
        conn = sqlite3.connect(f'{filename}')
        cursor = conn.cursor()
        all_keys = set()
        for config in data.values():
            all_keys.update(config.keys())

        create_table_sql = f'''
            CREATE TABLE IF NOT EXISTS config_data (
                server TEXT PRIMARY KEY,
                {", ".join(f"{key} TEXT" for key in all_keys)}
            )
        '''
        cursor.execute(create_table_sql)

        existing_columns = set()
        cursor.execute(f"PRAGMA table_info(config_data)")
        for column_info in cursor.fetchall():
            existing_columns.add(column_info[1])

        missing_columns = all_keys - existing_columns

        for column in missing_columns:
            alter_table_sql = f"ALTER TABLE config_data ADD COLUMN {column} TEXT"
            cursor.execute(alter_table_sql)

        for server, config in data.items():
            insert_values = [server] + [config.get(key) for key in all_keys]
            insert_sql = f'''
                INSERT OR REPLACE INTO config_data (server, {", ".join(all_keys)})
                VALUES ({", ".join(["?"] * (len(all_keys) + 1))})
            '''
            cursor.execute(insert_sql, insert_values)

        conn.commit()
        conn.close()
        return True
    
    def sortdata(filename):
        file_path = filename
        with open(file_path, "r") as file:
            lines = file.readlines()

        current_dict_name = None
        data_dict = {}


        for line in lines:
            line = line.strip()
            if not line:
                continue
            if line.endswith(':'):
                current_dict_name = line[:-1]
                data_dict[current_dict_name] = {}
            else:
                key_value = line.replace('[+] ', '', 1)
                key, value = key_value.split(': ', 1)
                data_dict[current_dict_name][key] = value

        file_path = "data.json"

        json_data = json.dumps(data_dict, indent=4)
        with open(file_path, "w") as file:
            file.write(json_data)
        return data_dict
    
    def send2tele(token,chat_id):

        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()
        query = "SELECT * FROM config_data"
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()

        token = f"{token}"
        chat_id = f"{chat_id}"

        for row in rows:
            server = row[0]
            config = {}
            for key, value in zip(cursor.description[1:], row[1:]):
                if value:
                    config[key[0]] = value


            message = f"Server: {server}\n"
            for key, value in config.items():
                message += f"{key}: {value}\n"
                
            api_url = f"https://api.telegram.org/bot{token}/sendMessage"
            data = {"chat_id": chat_id, "text": message}
            response = requests.post(api_url, data=data)
