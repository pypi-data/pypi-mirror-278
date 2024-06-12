import pymysql

class MySQLConnector:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def connect(self):
        try:
            self.connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=3306
            )
            self.cursor = self.connection.cursor()
            print("Connected to MySQL database")
        except Exception as e:
            print("Error connecting to MySQL database:", e)

    def disconnect(self):
        if hasattr(self, 'connection') and self.connection.open:
            self.cursor.close()
            self.connection.close()
            print("Disconnected from MySQL database")

    def execute_query(self, query):
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            return result
        except Exception as e:
            print("Error executing query:", e)

    def execute_query_by_id_list(self, query, idList):
        try:
            self.cursor.execute(query,idList)
            result = self.cursor.fetchall()
            return result
        except Exception as e:
            print("Error executing query:", e)

# Example usage:
if __name__ == "__main__":
    # Initialize MySQLConnector object
    connector = MySQLConnector(
        host="localhost",
        user="root",
        password="password",
        database="mydatabase"
    )

    # Connect to MySQL database
    connector.connect()

    # Example query
    query = "SELECT * FROM mytable LIMIT 10"

    # Execute query and print results
    result = connector.execute_query(query)
    print(result)

    # Disconnect from MySQL database
    connector.disconnect()
