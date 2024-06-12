import mysql.connector

class MySQLDatabase:
    def __init__(self, host, user, password, database):
        self.db_config = {
            'host': host,
            'user': user,
            'password': password,
            'database': database
        }

    def connect_to_mysql(self):
        conn = mysql.connector.connect(**self.db_config)
        return conn

    def insert_data(self, query, values):
        try:
            conn = self.connect_to_mysql()
            cursor = conn.cursor()
            cursor.execute(query, values)
            conn.commit()
            cursor.close()
            conn.close()
            return "Data inserted successfully"
        except Exception as e:
            return f"Error inserting data: {e}"

    def query_data(self, query):
        data = None
        try:
            conn = self.connect_to_mysql()
            cursor = conn.cursor()
            cursor.execute(query)
            columns = cursor.description
            data = [{columns[index][0]: column for index, column in enumerate(value)} for value in cursor.fetchall()]
            cursor.close()
            conn.close()
            return data, ''
        except Exception as e:
            return None, f"Error querying data: {e}"

# Example usage:
# db = MySQLDatabase(host='localhost', user='root', password='password', database='test_db')
# insert_result = db.insert_data("INSERT INTO my_table (column1, column2) VALUES (%s, %s)", ("value1", "value2"))
# print(insert_result)
# query_result, query_msg = db.query_data("SELECT * FROM my_table")
# if query_msg:
#     print(query_msg)
# else:
#     print(query_result)


