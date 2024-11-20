import sqlite3
from contextlib import closing
from typing import List, Optional


class BirdRecord:
    def __init__(self, id=None, url=None, serial_id=None, start_time=None, user=None,
                 location=None, number=None,status=None, is_done=None):
        self.id = id
        self.url = url
        self.serial_id = serial_id
        self.start_time = start_time
        self.user = user
        self.location = location
        self.number = number
        self.status = status
        self.is_done = is_done


class RecordDetail:
    def __init__(self, id=None, bird_no=None, bird_name=None, bird_latin_name=None, bird_eng_name=None, mu=None,
                 ke=None, num=None, record_no=None):
        self.id = id
        self.bird_no = bird_no
        self.bird_name = bird_name
        self.bird_latin_name = bird_latin_name
        self.bird_eng_name = bird_eng_name
        self.mu = mu
        self.ke = ke
        self.num = num
        self.record_no = record_no


class SqlUtils:
    # 获取数据连接
    @staticmethod
    def get_conn():
        return sqlite3.connect('bird_record.db')

    # 插入观鸟记录
    @staticmethod
    def insert_record(record: BirdRecord):
        with closing(SqlUtils.get_conn()) as conn:
            with closing(conn.cursor()) as cursor:
                insert_sql = """
                    INSERT INTO bird_record (url, serial_id, start_time, username, location, num, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """
                cursor.execute(insert_sql, (
                record.url, record.serial_id, record.start_time, record.user, record.location, record.number,
                record.status))
                conn.commit()

    # 插入观鸟记录明细
    @staticmethod
    def insert_detail(detail: RecordDetail):
        with closing(SqlUtils.get_conn()) as conn:
            with closing(conn.cursor()) as cursor:
                insert_sql = """
                    INSERT INTO bird_record_detail (bird_no, bird_name, bird_latin_name, bird_eng_name, mu, ke, num, record_no)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """
                cursor.execute(insert_sql, (
                detail.bird_no, detail.bird_name, detail.bird_latin_name, detail.bird_eng_name, detail.mu, detail.ke,
                detail.num, detail.record_no))
                conn.commit()

    # 根据观鸟记录编号查找记录
    @staticmethod
    def find_record(record_no: str) -> Optional[BirdRecord]:
        if not record_no:
            return None
        with closing(SqlUtils.get_conn()) as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute("""
                    SELECT id, url, serial_id, start_time, username, location, num, status, is_done
                    FROM bird_record
                    WHERE serial_id = ?
                    ORDER BY id DESC
                    LIMIT 1
                """, (record_no,))
                row = cursor.fetchone()
                if row:
                    return BirdRecord(*row)
        return None

    # 将数据库信息转换成记录对象
    @staticmethod
    def get_record(rs) -> BirdRecord:
        return BirdRecord(
            id=rs[0],
            url=rs[1],
            serial_id=rs[2],
            start_time=rs[3],
            user=rs[4],
            location=rs[5],
            number=rs[6],
            status=rs[7],
            is_done=rs[8]
        )

    # 查询未爬取明细的观鸟记录
    @staticmethod
    def find_not_done_records() -> List[BirdRecord]:
        with closing(SqlUtils.get_conn()) as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute("""
                    SELECT id, url, serial_id, start_time, username, location, num, status, is_done
                    FROM bird_record
                    WHERE is_done <> 1
                """)
                rows = cursor.fetchall()
                return [SqlUtils.get_record(row) for row in rows]

    # 根据观鸟记录id删除观鸟明细，用于重新爬取
    @staticmethod
    def delete_detail(serial_id: str):
        if not serial_id:
            return
        with closing(SqlUtils.get_conn()) as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute("DELETE FROM bird_record_detail WHERE record_no = ?", (serial_id,))
                conn.commit()

    # 更新观鸟记录状态
    @staticmethod
    def set_done(serial_id: str):
        if not serial_id:
            return
        with closing(SqlUtils.get_conn()) as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute("UPDATE bird_record SET is_done = 1 WHERE serial_id = ?", (serial_id,))
                conn.commit()
# 爬取全国保护动物信息
def save_animal_info(contents):
    sql = ("insert into animal_info(id, species_c, ass_level, rank_cn, order_c, family_c,class_c) "
           " values (?,?,?,?,?,?,?)")
    for content in contents:
        with closing(SqlUtils.get_conn()) as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute(sql, (
                    content['id'], content['speciesC'], content['assLevel'],
                    content['rankCn'], content['orderC'], content['familyC'],content["classC"]))
                conn.commit()