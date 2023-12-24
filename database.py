import sqlite3


class SQLiteDatabase:
    def __init__(self, path):
        """
        初始化数据库配置信息
        :param path:
        """
        self.path = path
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        try:
            cursor.executescript("""
                CREATE TABLE IF NOT EXISTS messages (
                    message_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    chat_id INTEGER NOT NULL, 
                    sender_name VARCHAR(50) NOT NULL,
                    sender_ip VARCHAR(50) NOT NULL,
                    content TEXT NOT NULL
                ); 
                CREATE TABLE IF NOT EXISTS chats (
                    chat_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    identifier CHAR(64) NOT NULL, 
                    created_time DATETIME DEFAULT CURRENT_TIMESTAMP
                );
            """)
            conn.commit()

        except sqlite3.Error as e:
            print("SQLite error: ", e)
        finally:
            conn.close()

    def create_chat(self, identifier, created_time):
        """
        创建一个新的聊天，返回聊天的chat_id
        :param identifier:
        :param created_time:
        :return:
        """
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO chats (identifier, created_time) VALUES (?, ?);", (identifier, created_time))
            conn.commit()
            # 获取刚生成的 chat_id
            cursor.execute("SELECT chat_id FROM chats WHERE chat_id = LAST_INSERT_ROWID();")
            chat_id = cursor.fetchone()[0]
            return chat_id

        except sqlite3.Error as e:
            print("SQLite error: ", e)
            return None, None

        finally:
            conn.close()

    def save_message(self, chat_id, sender_name, sender_ip, content):
        """
        保存一条聊天信息到数据库
        :param sender_name:
        :param sender_ip:
        :param chat_id:
        :param content:
        :return:
        """
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO messages (chat_id, sender_name, sender_ip, content) VALUES (?, ?, ?, ?);",
                           (chat_id, sender_name, sender_ip, content))
            conn.commit()

        except sqlite3.Error as e:
            print("SQLite error: ", e)

        finally:
            conn.close()

    def load_chat_history(self, identifier):
        """
        加载与当前聊天中所有成员相关的历史聊天记录
        :param identifier:
        :return:
        """
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT chat_id, created_time 
                FROM chats 
                WHERE identifier = ? 
                ORDER BY created_time;
            """, (identifier,))
            chat_infos = [row for row in cursor.fetchall()]

            chat_history = []
            for chat_info in chat_infos:
                chat_id = chat_info[0]
                item = {'time': chat_info[1]}
                cursor.execute("""
                    SELECT message_id, sender_name, sender_ip, content 
                    FROM messages 
                    WHERE chat_id = ? 
                    ORDER BY message_id;
                """, (chat_id,))
                messages = cursor.fetchall()
                item['content'] = messages
                chat_history.append(item)

            return chat_history

        except sqlite3.Error as e:
            print("SQLite error: ", e)
            return None
        finally:
            conn.close()
