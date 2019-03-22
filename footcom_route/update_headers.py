from accounts.login import login
from db.basic_db import db_session
from db.models import LoginInfo
# from insert_accounts import insert_accounts


def save_headers():
    # 从mysql读取所有账号
    accounts = db_session.query(LoginInfo).all()
    for account in accounts:
        # 读取出用户名和密码后登陆，传回headers
        headers = login(account.user, account.password)
        if headers != '':
            # 如果headers不为空则存入mysql
            db_session.query(LoginInfo).filter_by(user=account.user).update({
                "headers": headers
            })
            print(account.user + ' headers stored success')
        else:
            # 否则说明账户有问题，更新账户enable状态码
            db_session.query(LoginInfo).filter_by(user=account.user).update({
                "enable": 2
            })
            print(str(account.user) + ' login failed\n')
        db_session.commit()


if __name__ == "__main__":
    # insert_accounts()
    save_headers()
