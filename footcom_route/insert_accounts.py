from db.basic_db import db_session
from db.tables import login_info


def insert_accounts():
    accounts = (
        (17127290868, "Spider2018", 1),
        (17124267535, "Spider2018", 1),
        (17124267519, "Spider2018", 1),
        (17124267526, "Spider2018", 1),
        (17034662088, "Spider2018", 1),
        (17034662087, "Spider2018", 1),
        (17157721142, "Spider2018", 1),
        (17034662070, "Spider2018", 1),
        (17157725704, "Spider2018", 1),
        (17034662059, "Spider2018", 1)
    )
    try:
        db_session.execute("TRUNCATE TABLE  account")
        for account in accounts:
            insert_sql = login_info.insert().values({
                "user": str(account[0]),
                "password": str(account[1]),
                "enable": str(account[2])
            })
            db_session.execute(insert_sql)
        db_session.commit()
        print("插入账号成功\n")
    except Exception as e:
        print("插入失败", e)


if __name__ == "__main__":
    insert_accounts()
