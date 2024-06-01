import os
from typing import Final

import aiomysql
import asyncio
from dotenv import load_dotenv

DATABASE_NAME = 'Bot Database'
DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = '3306'

load_dotenv()
USER: Final[str] = os.getenv('MYSQL_USER')
PASS: Final[str] = os.getenv('MYSQL_PASS')


async def init_db():
    conn = await aiomysql.connect(
        host=DEFAULT_HOST,
        port=DEFAULT_HOST,
        user=USER,
        password=PASS,
        db=DATABASE_NAME
    )
    async with conn.cursor() as cursor:
        await cursor.execute('''CREATE TABLE IF NOT EXISTS gamers (
            id INT AUTO_INCREMENT PRIMARY KEY, 
            name VARCHAR(255) NOT NULL
        )''')
    await conn.ensure_closed()


async def get_db_connection():
    return await aiomysql.connect(
        host=DEFAULT_HOST,
        port=DEFAULT_HOST,
        user=USER,
        password=PASS,
        db=DATABASE_NAME
    )


async def add_user(name):
    conn = await get_db_connection()
    async with conn.cursor() as cursor:
        await cursor.execute("INSERT INTO gamers (name) VALUES (%s)", (name,))
    await conn.commit()
    await conn.ensure_closed()


async def list_users():
    conn = await get_db_connection()
    async with conn.cursor() as cursor:
        await cursor.execute("SELECT name FROM gamers")
        result = await cursor.fetchall()
    await conn.ensure_closed()
    return [row[0] for row in result]
