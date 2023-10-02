from project import app

app.secret_key = b'5f214cacbd30c2ae4784b520f17912ae0d5d8c16ae98128e3f549546221265e4'

if __name__ == "__main__":
  app.run(debug=True)
   
