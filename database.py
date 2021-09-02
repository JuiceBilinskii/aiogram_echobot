import psycopg2


class Database:
    UPDATE_USER = (
        "INSERT INTO chat_selections (id, number_of_replies) "
        "VALUES (%s, %s) "
        "ON CONFLICT (id) DO UPDATE "
        "SET number_of_replies = excluded.number_of_replies"
    )
    GET_NUMBER_OF_REPLIES = "SELECT number_of_replies FROM chat_selections WHERE id=%s"


    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
    
    def open_connection_false_if_fails(self):
        try:
            conn = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
            )
            return conn
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return False
    

    def close_connection(self, conn):
        if conn is not False:
            conn.close()
            print('Database connection closed.')
        return True


    def update_user(self, chat_id, number_of_replies):
        conn = self.open_connection_false_if_fails()

        try:
            cur = conn.cursor()

            cur.execute(self.UPDATE_USER, (chat_id, number_of_replies))
            conn.commit()

            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            self.close_connection(conn)
    

    def get_number_of_replies(self, chat_id):
        conn = self.open_connection_false_if_fails()

        try:
            cur = conn.cursor()

            cur.execute(self.GET_NUMBER_OF_REPLIES, (chat_id,))
            result = cur.fetchone()

            cur.close()
            return result
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            self.close_connection(conn)  
