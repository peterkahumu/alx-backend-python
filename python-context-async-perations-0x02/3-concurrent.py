import asyncio
import asyncpg
import os

async def async_fetch_users():
    conn = await asyncpg.connect(
        database=os.environ.get("DB_NAME"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        host=os.environ.get("DB_HOST", "localhost"),
        port=int(os.environ.get("DB_PORT", 5432))
    )
    try:
        users = await conn.fetch("SELECT * FROM user_data")
        for user in users:
            print(user)
    finally:
        await conn.close()

async def async_fetch_older_users():
    conn = await asyncpg.connect(
        database=os.environ.get("DB_NAME"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        host=os.environ.get("DB_HOST", "localhost"),
        port=int(os.environ.get("DB_PORT", 5432))
    )
    try:
        older_users = await conn.fetch("SELECT * FROM user_data WHERE age > 40")
        for user in older_users:
            print(user)
    finally:
        await conn.close()

async def fetch_concurrently():
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
