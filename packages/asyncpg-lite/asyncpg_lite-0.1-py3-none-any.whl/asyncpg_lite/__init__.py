import asyncpg
from typing import Dict, Optional, List, Union
import logging


class DatabaseManager:
    """
    Класс для управления базой данных PostgreSQL с использованием библиотеки asyncpg.
    """

    def __init__(self, dsn: Optional[str] = None,
                 deletion_password: str = "my_root_password",
                 dsn_flag: bool = True,
                 host: Optional[str] = None,
                 port: Optional[int] = None,
                 user: Optional[str] = None,
                 password: Optional[str] = None,
                 database: Optional[str] = None):
        """
        Инициализация менеджера базы данных.

        :param dsn: Строка DSN для подключения к базе данных.
        :param deletion_password: Пароль для удаления данных или таблиц.
        :param dsn_flag: Флаг, указывающий использовать ли DSN для подключения.
        :param host: Хост базы данных.
        :param port: Порт базы данных.
        :param user: Имя пользователя базы данных.
        :param password: Пароль базы данных.
        :param database: Имя базы данных.
        """
        self.dsn = dsn
        self.deletion_password = deletion_password
        self.dsn_flag = dsn_flag
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

    async def __aenter__(self):
        """
        Устанавливает соединение с базой данных при входе в асинхронный контекстный менеджер.
        """
        try:
            if self.dsn_flag:
                self.connection = await asyncpg.connect(dsn=self.dsn)
            else:
                self.connection = await asyncpg.connect(
                    host=self.host,
                    port=self.port,
                    user=self.user,
                    password=self.password,
                    database=self.database
                )
            self.logger.info("Соединение с базой данных установлено.")
        except asyncpg.PostgresError as e:
            self.logger.error(f"Ошибка при подключении к базе данных: {e}")
            raise
        return self

    async def __aexit__(self, exc_type, exc, tb):
        """
        Закрывает соединение с базой данных при выходе из асинхронного контекстного менеджера.
        """
        if self.connection:
            try:
                await self.connection.close()
                self.logger.info("Соединение с базой данных закрыто.")
            except asyncpg.PostgresError as e:
                self.logger.error(f"Ошибка при закрытии соединения с базой данных: {e}")

    async def create_table(self, table_name: str, columns: List[str]):
        """
        Создает таблицу в базе данных.

        :param table_name: Имя таблицы.
        :param columns: Список строк, определяющих столбцы таблицы.
        """
        try:
            async with self.connection.transaction():
                columns_clause = ', '.join(columns)
                query = f'CREATE TABLE IF NOT EXISTS {table_name} ({columns_clause});'
                await self.connection.execute(query)
                self.logger.info(f"Таблица {table_name} успешно создана.")
        except asyncpg.PostgresError as e:
            self.logger.error(f'Ошибка при создании таблицы: {e}')

    async def select_data(self, table_name: str, where_dict: Optional[Union[Dict, List[Dict]]] = None,
                          columns: Optional[List[str]] = None, one_dict: bool = False) -> Union[List[Dict], Dict]:
        """
        Извлекает данные из таблицы базы данных.

        :param table_name: Имя таблицы.
        :param where_dict: Условия для фильтрации данных.
        :param columns: Список столбцов для извлечения.
        :param one_dict: Возвращать ли только одну запись в виде словаря.
        :return: Список словарей с данными или один словарь, если one_dict=True.
        """
        try:
            async with self.connection.transaction():
                column_names = ', '.join(columns) if columns else '*'
                where_clause = ''
                all_values = []
                if where_dict:
                    if isinstance(where_dict, dict):
                        conditions = ' AND '.join(f"{key} = ${i + 1}" for i, key in enumerate(where_dict.keys()))
                        where_clause = f' WHERE {conditions}'
                        all_values = list(where_dict.values())
                    elif isinstance(where_dict, list):
                        where_clauses = []
                        index = 1
                        for condition in where_dict:
                            where_clauses.append(
                                ' AND '.join(f"{key} = ${index + i}" for i, key in enumerate(condition.keys())))
                            index += len(condition)
                            all_values.extend(condition.values())
                        where_clause = ' WHERE (' + ') OR ('.join(where_clauses) + ')'
                query = f'SELECT {column_names} FROM {table_name}{where_clause};'
                rows = await self.connection.fetch(query, *all_values)
                all_data = [dict(row) for row in rows]
                if one_dict and all_data:
                    self.logger.info(f"Успешно получили 1 словарь из таблицы {table_name}.")
                    return all_data[0]
                if len(all_data):
                    self.logger.info(f"Успешно получили {len(all_data)} словарей из таблицы {table_name}.")
                else:
                    self.logger.info(f"Из таблицы {table_name} по вашему запросу нет данных!")
                return all_data
        except asyncpg.PostgresError as e:
            self.logger.error(f'Ошибка при выполнении запроса: {e}')
            return []

    async def insert_data(self, table_name: str, records_data: Union[dict, List[dict]]):
        """
        Вставляет данные в таблицу базы данных.

        :param table_name: Имя таблицы.
        :param records_data: Словарь или список словарей с данными для вставки.
        """
        try:
            async with self.connection.transaction():
                if isinstance(records_data, dict):
                    records_data = [records_data]

                if not records_data:
                    self.logger.info("Список записей пуст.")
                    return

                first_record = records_data[0]
                columns = ', '.join(first_record.keys())
                placeholders = ', '.join(f'(${i + 1})' for i in range(len(first_record)))

                query = f'INSERT INTO {table_name} ({columns}) VALUES {", ".join([placeholders] * len(records_data))};'
                values = [value for record in records_data for value in record.values()]

                await self.connection.execute(query, *values)
                self.logger.info("Записи успешно добавлены.")
        except asyncpg.PostgresError as e:
            self.logger.error(f'Ошибка при добавлении записей: {e}')

    async def update_data(self, table_name: str,
                          where_dict: Union[Dict[str, Union[str, int]], List[Dict[str, Union[str, int]]]],
                          update_dict: Dict[str, Union[str, int]]):
        """
        Обновляет данные в таблице базы данных.

        :param table_name: Имя таблицы.
        :param where_dict: Условия для выбора записей для обновления.
        :param update_dict: Словарь с данными для обновления.
        """
        try:
            async with self.connection.transaction():
                set_clause = ', '.join(f"{key} = ${i + 1}" for i, key in enumerate(update_dict.keys()))
                where_clause = ''
                all_values = list(update_dict.values())
                if isinstance(where_dict, dict):
                    where_clause = ' AND '.join(
                        f"{key} = ${len(update_dict) + i + 1}" for i, key in enumerate(where_dict.keys()))
                    all_values.extend(where_dict.values())
                elif isinstance(where_dict, list):
                    where_clauses = []
                    index = len(update_dict) + 1
                    for condition in where_dict:
                        where_clauses.append(
                            ' AND '.join(f"{key} = ${index + i}" for i, key in enumerate(condition.keys())))
                        index += len(condition)
                        all_values.extend(condition.values())
                    where_clause = ' OR '.join(f'({clause})' for clause in where_clauses)

                query = f'UPDATE {table_name} SET {set_clause} WHERE {where_clause};'
                await self.connection.execute(query, *all_values)
                self.logger.info("Записи успешно обновлены.")
        except asyncpg.PostgresError as e:
            self.logger.error(f'Ошибка при обновлении записей: {e}')

    async def delete_data(self, table_name: str,
                          where_dict: Union[Dict[str, Union[str, int]], List[Dict[str, Union[str, int]]]]):
        """
        Удаляет данные из таблицы базы данных.

        :param table_name: Имя таблицы.
        :param where_dict: Условия для выбора записей для удаления.
        """
        try:
            async with self.connection.transaction():
                where_clause = ''
                all_values = []
                if isinstance(where_dict, dict):
                    where_clause = ' AND '.join(f"{key} = ${i + 1}" for i, key in enumerate(where_dict.keys()))
                    all_values.extend(where_dict.values())
                elif isinstance(where_dict, list):
                    where_clauses = []
                    index = 1
                    for condition in where_dict:
                        where_clauses.append(
                            ' AND '.join(f"{key} = ${index + i}" for i, key in enumerate(condition.keys())))
                        index += len(condition)
                        all_values.extend(condition.values())
                    where_clause = ' OR '.join(f'({clause})' for clause in where_clauses)

                query = f'DELETE FROM {table_name} WHERE {where_clause};'
                await self.connection.execute(query, *all_values)
                self.logger.info("Записи успешно удалены.")
        except asyncpg.PostgresError as e:
            self.logger.error(f'Ошибка при удалении записей: {e}')

    async def delete_all_data(self, table_name: str, password: str):
        """
        Удаляет все данные из таблицы базы данных.

        :param table_name: Имя таблицы.
        :param password: Пароль для подтверждения операции удаления всех данных.
        """
        if password != self.deletion_password:
            self.logger.warning("Неверный пароль. Удаление всех записей невозможно.")
            return
        try:
            async with self.connection.transaction():
                await self.connection.execute(f'DELETE FROM {table_name};')
                self.logger.info("Все записи успешно удалены.")
        except asyncpg.PostgresError as e:
            self.logger.error(f'Ошибка при удалении всех записей: {e}')

    async def drop_table(self, table_name: str, password: str):
        """
        Удаляет таблицу из базы данных.

        :param table_name: Имя таблицы.
        :param password: Пароль для подтверждения операции удаления таблицы.
        """
        if password != self.deletion_password:
            self.logger.warning("Неверный пароль. Удаление таблицы невозможно.")
            return
        try:
            async with self.connection.transaction():
                query = f'DROP TABLE IF EXISTS {table_name};'
                await self.connection.execute(query)
                self.logger.info(f"Таблица {table_name} успешно удалена.")
        except asyncpg.PostgresError as e:
            self.logger.error(f'Ошибка при удалении таблицы: {e}')