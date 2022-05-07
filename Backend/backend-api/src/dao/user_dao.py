from src.utils.password import generate_password, check_password
from src.database import get_cursor


class UserDAO:
  
  @staticmethod
  def create(username, password, is_admin):
    password_hashed = generate_password(password)

    with get_cursor() as (conn, cur):
      cur.execute("""
        INSERT INTO users (username, pwd_hash, is_admin, balance)
          VALUES (%s, %s, %s, %s);
      """, (username, password_hashed, is_admin, 0))
      conn.commit()
  
  @staticmethod
  def get(username):
    with get_cursor() as (conn, cur):
      cur.execute(
        "SELECT * FROM users WHERE username=%s;",
        (username, ))
      user_doc = cur.fetchone()
      if not user_doc: return None

      (username, pwd_hash, is_admin, balance) = user_doc
      return {
        'username': username,
        'pwd_hash': pwd_hash,
        'is_admin': is_admin,
        'balance': balance,
      }

  @staticmethod
  def delete(username):
    with get_cursor() as (conn, cur):
      cur.execute(
        "DELETE FROM users WHERE username=%s;",
        (username, ))
      conn.commit()
  
  @staticmethod
  def is_password_correct(username, password):
    user = UserDAO().get(username)
    if not user: return False
    return check_password(password, user['pwd_hash'])

def test_user_dao():
  try:
    UserDAO.create('test_user', 'test_pass', False)
    user_created = UserDAO.get('test_user')
    print(user_created)
    assert user_created['username'] == 'test_user'
    assert user_created['is_admin'] == False
    assert user_created['balance'] == 0
    assert UserDAO.is_password_correct('test_user', 'test_pass') == True
    assert UserDAO.is_password_correct('test_user', 'wrong_pass') == False
    print('Tests in user_dao passed')
  finally:
    UserDAO.delete('test_user')
    pass

if __name__ == '__main__':
  test_user_dao()

