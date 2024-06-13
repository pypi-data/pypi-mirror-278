from typing import Any
from sqlalchemy import text
from sqlalchemy.orm import Session
from afeng_tools.sqlalchemy_tools.core.sqlalchemy_class import SqlalchemyDb
from afeng_tools.sqlalchemy_tools.core.sqlalchemy_items import DatabaseInfoItem
from afeng_tools.sqlalchemy_tools.crdu import sequence_crdu


class DBAdmin:
    """数据库管理"""
    def __init__(self, database_uri: str, echo_sql: bool = False):
        self.database_uri = database_uri
        self.sqlalchemy_db = SqlalchemyDb(DatabaseInfoItem(
            database_uri=database_uri,
            echo_sql=echo_sql
        ))

    def query_more_by_sql(self, sql: str) -> list[dict[str, Any]]:
        with self.sqlalchemy_db.engine.connect() as conn:
            cursor = conn.execute(text(sql))
            result_list = []
            for tmp_line in cursor.fetchall():
                result_list.append({tmp_key: tmp_line[index] for index, tmp_key in enumerate(cursor.keys())})
            return result_list

    def query_one_by_sql(self, sql: str) -> dict[str, Any]:
        with self.sqlalchemy_db.engine.connect() as conn:
            cursor = conn.execute(text(sql))
            sql_result = cursor.fetchone()
            return {tmp_key: sql_result[index] for index, tmp_key in enumerate(cursor.keys())}

    def query_by_sql(self, sql: str) -> list[tuple]:
        """通过sql语句查找"""
        with self.sqlalchemy_db.engine.connect() as conn:
            cursor = conn.execute(text(sql))
            return cursor.fetchall()

    def exec_by_sql(self, sql: str):
        """通过sql运行"""
        with self.sqlalchemy_db.engine.connect() as conn:
            cursor = conn.execute(text(sql))
            conn.commit()
            return cursor.lastrowid

    def get_session(self) -> Session:
        return self.sqlalchemy_db.get_session()

    def update_sequence_value_to(self, sequence_name: str, max_id: int):
        with self.sqlalchemy_db.get_session() as tmp_session:
            sequence_crdu.update_sequence_value_to(sequence_name, to_value=max_id, db=tmp_session)
            tmp_session.commit()

    def query_max_id(self, table_name: str):
        query_result = self.query_one_by_sql(f'SELECT max(id) FROM {table_name};')
        if query_result:
            return query_result.get('max')
        return 0

    def update_table_sequence_to_new(self, table_name: str):
        self.update_sequence_value_to(sequence_name=f'{table_name}_id_seq',
                                      max_id=self.query_max_id(table_name))


if __name__ == '__main__':
    db_admin = DBAdmin('postgresql://www_user:123456@127.0.0.1:5432/test_db')
    result = db_admin.query_one_by_sql('SELECT max(id) FROM tb_blacklist_info;')
    # result = db_admin.exec_by_sql('SELECT * FROM tb_blacklist_info;')
    print()
