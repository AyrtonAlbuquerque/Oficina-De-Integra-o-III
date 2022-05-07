from datetime import datetime
from src.utils.password import generate_password, check_password
from src.database import get_cursor
from src.dao.user_dao import UserDAO
from src.exceptions import InsufficientFunds


class TransactionDAO:
  
  @staticmethod
  def transact(from_account, to_account, amount):
    from_user = UserDAO.get(from_account)
    to_user = UserDAO.get(to_account)

    if from_user['balance'] < amount: raise InsufficientFunds

    from_balance = from_user['balance'] - amount
    to_balance = to_user['balance'] + amount
    with get_cursor() as (conn, cur):
      cur.execute("""
        INSERT INTO transactions (to_account, from_account, amount, created_at)
          VALUES (%s, %s, %s, %s) RETURNING id;
        """,
        (to_account, from_account, amount, datetime.now()))
      transaction_id = cur.fetchone()[0]
      cur.execute(
        "UPDATE users SET balance=%s WHERE username=%s",
        (from_balance, from_account))
      cur.execute(
        "UPDATE users SET balance=%s WHERE username=%s",
        (to_balance, to_account))
      conn.commit()
      return transaction_id
  
  @staticmethod
  def get(transaction_id):
    with get_cursor() as (conn, cur):
      cur.execute(
        "SELECT * FROM transactions WHERE ID=%s;",
        (transaction_id, ))
      (ID, to_account, from_account, amount, balance) = cur.fetchone()

      return {
        'ID': ID,
        'to_account': to_account,
        'from_account': from_account,
        'amount': amount,
        'balance': balance,
      }

  @staticmethod
  def give_credits(username, amount):
    user = UserDAO.get(username)
    with get_cursor() as (conn, cur):
      cur.execute(
        "UPDATE users SET balance=%s WHERE username=%s",
        (user['balance'] + amount, username))
      conn.commit()


  @staticmethod
  def delete_transaction(transaction_id):
    with get_cursor() as (conn, cur):
      cur.execute(
        "DELETE FROM transactions WHERE ID=%s;",
        (transaction_id, ))
      conn.commit()

def test_transaction_dao():
  try:
    UserDAO.create('test_user1', 'test_pass', False)
    UserDAO.create('test_user2', 'test_pass', False)
    
    TransactionDAO.give_credits('test_user1', 1.85)
    test_user1 = UserDAO.get('test_user1')
    assert test_user1['balance'] == 1.85

    transaction_id = TransactionDAO.transact('test_user1', 'test_user2', 0.75)
    test_user1 = UserDAO.get('test_user1')
    test_user2 = UserDAO.get('test_user2')

    assert test_user1['balance'] == 1.10
    assert test_user2['balance'] == 0.75

    print('Tests in transaction_dao passed')
  finally:
    UserDAO.delete('test_user1')
    UserDAO.delete('test_user2')
    TransactionDAO.delete_transaction(transaction_id)

if __name__ == '__main__':
  test_transaction_dao()

