# import json
# import sqlite3

# # Đọc file JSON
# with open('data.json', 'r', encoding='utf-8') as f:
#     data = json.load(f)

# # Kết nối tới SQLite database (hoặc tạo nếu chưa tồn tại)
# conn = sqlite3.connect('data.sqlite')
# c = conn.cursor()

# # Tạo bảng
# c.execute('''CREATE TABLE IF NOT EXISTS entries
#              (_id TEXT PRIMARY KEY, name TEXT, length TEXT)''')
# c.execute('''CREATE TABLE IF NOT EXISTS results
#              (entry_id TEXT, tu_tuong_hinh TEXT, am_nom TEXT, am_nom_khac TEXT, 
#              ma_unicode TEXT, so_net TEXT, so_them_net TEXT, bo_tuong_hinh TEXT, 
#              bo_quoc_ngu TEXT, tu_loai TEXT, tu_dien TEXT, giai_nghia TEXT, FOREIGN KEY(entry_id) REFERENCES entries(_id))''')
# c.execute('''CREATE TABLE IF NOT EXISTS tu_hinh
#              (result_id INTEGER, content TEXT, imageSrc TEXT, FOREIGN KEY(result_id) REFERENCES results(rowid))''')
# c.execute('''CREATE TABLE IF NOT EXISTS di_the
#              (result_id INTEGER, content TEXT, href TEXT, cach_viet TEXT, FOREIGN KEY(result_id) REFERENCES results(rowid))''')

# # Chèn dữ liệu vào bảng
# for entry in data:
#     c.execute('INSERT INTO entries VALUES (?, ?, ?)', (entry['_id'], entry['name'], entry['length']))
    
#     for result in entry['results']:
#         c.execute('INSERT INTO results (entry_id, tu_tuong_hinh, am_nom, am_nom_khac, ma_unicode, so_net, so_them_net, bo_tuong_hinh, bo_quoc_ngu, tu_loai, tu_dien, giai_nghia) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
#                   (entry['_id'], result['tu_tuong_hinh'], result['am_nom'], 
#                    ','.join(result['am_nom_khac']), result['description']['ma_unicode'], result['description']['so_net'], 
#                    result['description']['so_them_net'], result['description']['bo_tuong_hinh'], result['description']['bo_quoc_ngu'], 
#                    result['description']['tu_loai'], result['tu_dien'], result['giai_nghia']))
#         result_id = c.lastrowid
        
#         for tu_hinh in result.get('tu_hinh', []):
#             c.execute('INSERT INTO tu_hinh (result_id, content, imageSrc) VALUES (?, ?, ?)',
#                       (result_id, tu_hinh['content'], tu_hinh['imageSrc']))
            
#         for di_the in result.get('di_the', []):
#             c.execute('INSERT INTO di_the (result_id, content, href, cach_viet) VALUES (?, ?, ?, ?)',
#                       (result_id, di_the['content'], di_the['href'], di_the.get('cach_viet')))

# # Lưu thay đổi và đóng kết nối
# conn.commit()
# conn.close()



import sqlite3
import json

# Đọc dữ liệu từ tệp JSON
def load_data_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# Tạo bảng và chèn dữ liệu vào SQLite
def create_and_populate_tables(data, conn):
    cursor = conn.cursor()

    # Tạo bảng chính
    cursor.execute('''CREATE TABLE IF NOT EXISTS main_data (
                    _id TEXT PRIMARY KEY,
                    name TEXT,
                    length INTEGER,
                    __v INTEGER
                    )''')

    # Tạo bảng cho các phần tử trong mảng results
    cursor.execute('''CREATE TABLE IF NOT EXISTS results (
                    main_id TEXT,
                    tu_tuong_hinh TEXT,
                    am_nom TEXT,
                    description_ma_unicode TEXT,
                    description_so_net TEXT,
                    description_so_them_net TEXT,
                    description_bo_tuong_hinh TEXT,
                    description_bo_quoc_ngu TEXT,
                    description_tu_loai TEXT,
                    tu_dien TEXT,
                    giai_nghia TEXT,
                    FOREIGN KEY (main_id) REFERENCES main_data(_id)
                    )''')

    # Chèn dữ liệu vào bảng
    for item in data:
        _id = item['_id']
        name = item['name']
        length = int(item['length'])
        __v = int(item['__v'])

        cursor.execute('''INSERT INTO main_data (_id, name, length, __v) 
                        VALUES (?, ?, ?, ?)''', (_id, name, length, __v))

        for result in item['results']:
            tu_tuong_hinh = result['tu_tuong_hinh']
            am_nom = result['am_nom']
            description_ma_unicode = result['description']['ma_unicode']
            description_so_net = result['description']['so_net']
            description_so_them_net = result['description']['so_them_net']
            description_bo_tuong_hinh = result['description']['bo_tuong_hinh']
            description_bo_quoc_ngu = result['description']['bo_quoc_ngu']
            description_tu_loai = result['description']['tu_loai']
            tu_dien = result['tu_dien']
            giai_nghia = result['giai_nghia']

            cursor.execute('''INSERT INTO results (main_id, tu_tuong_hinh, am_nom, description_ma_unicode, description_so_net,
                            description_so_them_net, description_bo_tuong_hinh, description_bo_quoc_ngu, description_tu_loai,
                            tu_dien, giai_nghia) 
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                           (_id, tu_tuong_hinh, am_nom, description_ma_unicode, description_so_net,
                            description_so_them_net, description_bo_tuong_hinh, description_bo_quoc_ngu,
                            description_tu_loai, tu_dien, giai_nghia))

    conn.commit()

# Tạo kết nối đến cơ sở dữ liệu SQLite
def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return None

# Hàm chính
def main():
    json_file = 'data.json'
    db_file = 'data.db'

    # Tạo kết nối đến cơ sở dữ liệu
    conn = create_connection(db_file)
    if conn is not None:
        # Đọc dữ liệu từ tệp JSON
        data = load_data_from_json(json_file)
        if data is not None:
            # Tạo và chèn dữ liệu vào các bảng SQLite
            create_and_populate_tables(data, conn)
        else:
            print("Không thể đọc dữ liệu từ file JSON.")
        # Đóng kết nối
        conn.close()
    else:
        print("Không thể kết nối đến cơ sở dữ liệu SQLite.")

if __name__ == '__main__':
    main()
