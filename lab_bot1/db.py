import asyncpg

class Database:
    def __init__(self, config):
        self.config = config
        self.pool = None


    async def connect(self):
        self.pool = await asyncpg.create_pool(**self.config)
        print("Successfully connected")


    async def create_tables(self):
        async with self.pool.acquire() as connection:
            await connection.execute("""
                CREATE TABLE IF NOT EXISTS user_words (
                    id SERIAL PRIMARY KEY,
                    user_id BIGINT NOT NULL,
                    word TEXT NOT NULL,
                    translation TEXT NOT NULL,
                    UNIQUE(user_id, word)
                );
            """)
            await connection.execute("""
                CREATE TABLE IF NOT EXISTS user_buttons (
                    id SERIAL PRIMARY KEY,
                    user_id BIGINT NOT NULL,
                    word TEXT NOT NULL,
                    translation TEXT NOT NULL,
                    UNIQUE(user_id, word)
                );
            """)
            print("Tables created")


    async def save_words(self, user_id, words_dict):
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                for word, translation in words_dict.items():
                    await connection.execute("""
                        INSERT INTO user_words (user_id, word, translation)
                        VALUES ($1, $2, $3)
                        ON CONFLICT (user_id, word) DO UPDATE
                        SET translation = EXCLUDED.translation
                    """, user_id, word, translation)


    async def save_buttons(self, user_id, buttons_dict):
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                for word, translation in buttons_dict.items():
                    await connection.execute("""
                        INSERT INTO user_buttons (user_id, word, translation)
                        VALUES ($1, $2, $3)
                        ON CONFLICT (user_id, word) DO UPDATE
                        SET translation = EXCLUDED.translation
                    """, user_id, word, translation)


    async def get_words(self, user_id):
        async with self.pool.acquire() as connection:
            rows = await connection.fetch("""
                SELECT word, translation FROM user_words WHERE user_id = $1
            """, user_id)
            return {row['word']: row['translation'] for row in rows}


    async def get_buttons(self, user_id):
        async with self.pool.acquire() as connection:
            rows = await connection.fetch("""
                SELECT word, translation FROM user_buttons WHERE user_id = $1
            """, user_id)
            return {row['word']: row['translation'] for row in rows}


    async def delete_word(self, user_id, word):
        async with self.pool.acquire() as connection:
            await connection.execute("""
                DELETE FROM user_words WHERE user_id = $1 AND word = $2
            """, user_id, word)


    async def delete_button(self, user_id, word):
        async with self.pool.acquire() as connection:
            await connection.execute("""
                DELETE FROM user_buttons WHERE user_id = $1 AND word = $2
            """, user_id, word)
