import bcrypt

def generate_password(plain_text_password):
  salt = bcrypt.gensalt(10)
  return bcrypt.hashpw(plain_text_password.encode('utf8'), salt).decode('utf8')

def check_password(password, hashed_password):
  return bcrypt.checkpw(password.encode('utf8'), hashed_password.encode('utf8'))

if __name__ == '__main__':
  hashed = generate_password('some_pass')
  print('Hashed password:', hashed)
  assert check_password('other', hashed) == False
  assert check_password('some_pass', hashed) == True
