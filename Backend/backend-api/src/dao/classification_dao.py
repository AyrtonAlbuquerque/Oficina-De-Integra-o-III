from src.database import get_cursor

class ClassificationDAO:
  
  @staticmethod
  def create(classification):
    recycler_id = classification['recycler_id']
    label = classification['label']
    redeem_code = classification['redeem_code']
    image_path = classification['image_path']
    with get_cursor() as (conn, cur):
      cur.execute("""
        INSERT INTO classifications (recycler_id, label, redeem_code, is_redeemed, image_path)
          VALUES (%s, %s, %s, %s, %s);
      """, (recycler_id, label, redeem_code, False, image_path))
      conn.commit()

  @staticmethod
  def classification_with_redeem_code_exists(redeem_code):
    with get_cursor() as (conn, cur):
      cur.execute(
        "SELECT * FROM classifications WHERE redeem_code=%s;",
        (redeem_code, ))
      if cur.fetchone(): return True
      return False

  @staticmethod
  def redeem_code_from_classification(redeem_code):
    with get_cursor() as (conn, cur):
      cur.execute("""
          UPDATE classifications
            SET is_redeemed=true
            WHERE redeem_code=%s;
        """, (redeem_code, ))
      conn.commit()

  @staticmethod
  def classification_statistics():
    with get_cursor() as (conn, cur):
      cur.execute("""
          SELECT label, COUNT(*)
            FROM classifications
            GROUP BY label;
        """)
      return cur.fetchall()

if __name__ == '__main__':
  test_user_dao()

