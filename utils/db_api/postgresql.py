from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config


class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME,
        )

    async def execute(
        self,
        command,
        *args,
        fetch: bool = False,
        fetchval: bool = False,
        fetchrow: bool = False,
        execute: bool = False,
    ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
        id SERIAL PRIMARY KEY,
        full_name VARCHAR(255) NOT NULL,
        username varchar(255) NULL,
        telegram_id BIGINT NOT NULL UNIQUE
        );
        """
        await self.execute(sql, execute=True)

    async def create_table_course(self):
        sql = """
        CREATE TABLE IF NOT EXISTS course (
        id SERIAL PRIMARY KEY,
        course_name VARCHAR(255) NOT NULL UNIQUE,
        description varchar(355) NOT NULL,
        months VARCHAR(20) NULL,
        price VARCHAR(100) NULL 
        );
        """
        await self.execute(sql, execute=True)

    async def create_table_enroll_user(self):
        sql = """
        CREATE TABLE IF NOT EXISTS enroll_user (
        id SERIAL PRIMARY KEY,
        user_name VARCHAR(255) NOT NULL,
        user_phone VARCHAR(255) NOT NULL,
        course_name VARCHAR(255) NOT NULL
        );
        """
        await self.execute(sql, execute=True)

    async def create_table_advice_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS advice_users (
        id SERIAL PRIMARY KEY,
        user_name VARCHAR(255) NOT NULL, 
        user_id BIGINT NOT NULL,
        user_phone VARCHAR(255) NOT NULL,
        user_advice VARCHAR(600) NOT NULL
        );
        """
        await self.execute(sql, execute=True)


    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join(
            [f"{item} = ${num}" for num, item in enumerate(parameters.keys(), start=1)]
        )
        return sql, tuple(parameters.values())
    
    async def add_course(self, course_name, description, months, price):
        sql = "INSERT INTO course (course_name, description, months, price) VALUES($1, $2, $3, $4) returning *"
        return await self.execute(sql, course_name, description, months, price, fetchrow=True)

    async def add_enroll_user(self, user_name, user_phone, course_name):
        sql = "INSERT INTO enroll_user (user_name, user_phone, course_name) VALUES($1, $2, $3) returning *"
        return await self.execute(sql, user_name, user_phone, course_name, fetchrow=True)
    
    async def add_advice(self, user_name, user_id, user_phone, user_advice):
        sql = "INSERT INTO advice_users (user_id, user_name, user_phone, user_advice) VALUES($1, $2, $3, $4) returning *"
        return await self.execute(sql, user_id, user_name, user_phone, user_advice, fetchrow=True)
    
    async def add_user(self, full_name, username, telegram_id):
        sql = "INSERT INTO users (full_name, username, telegram_id) VALUES($1, $2, $3) returning *"
        return await self.execute(sql, full_name, username, telegram_id, fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT * FROM Users"
        return await self.execute(sql, fetch=True)

    async def select_all_course(self):
        sql = "SELECT * FROM course"
        return await self.execute(sql, fetch=True)
    
    async def select_all_enroll_users(self):
        sql = "SELECT * FROM enroll_user"
        return await self.execute(sql, fetch=True)

    async def select_all_advices(self):
        sql = "SELECT * FROM advice_users"
        return await self.execute(sql, fetch=True)
    
    async def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)
    
    async def select_course(self, **kwargs):
        sql = "SELECT * FROM course WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM Users"
        return await self.execute(sql, fetchval=True)

    async def update_user_username(self, username, telegram_id):
        sql = "UPDATE Users SET username=$1 WHERE telegram_id=$2"
        return await self.execute(sql, username, telegram_id, execute=True)

    async def delete_users(self):
        await self.execute("DELETE FROM Users WHERE TRUE", execute=True)

    async def delete_advice(self, user_advice):
        await self.execute("DELETE FROM advice_users WHERE user_advice=$1", user_advice, execute=True)

    async def delete_course(self, course_name):
        await self.execute("DELETE FROM course WHERE course_name=$1", course_name, execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE Users", execute=True)

    async def drop_course(self):
        await self.execute("DROP TABLE course", execute=True)

    async def drop_enroll_users(self):
        await self.execute("DROP TABLE enroll_user", execute=True)

    async def drop_advice_users(self):
        await self.execute("DROP TABLE advice_users", execute=True)   