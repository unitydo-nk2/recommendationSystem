import mysql.connector
import pandas as pd

mydb = mysql.connector.connect(
  # host="10.4.85.19",
  host="172.26.0.3",
  user="root",
  password="dreamtongphop",
  database="unityDoDB"
)

def get_activitywithcategoryview():
  mycursor = mydb.cursor()
  mycursor.execute("SELECT * FROM activityWithCategoryView")
  myresult = mycursor.fetchall()
  df = pd.DataFrame(myresult, columns=mycursor.column_names)
  return df

def get_usercategoryrankingview():
  mycursor = mydb.cursor()
  mycursor.execute("SELECT * FROM userCategoryRankingView")
  myresult = mycursor.fetchall()
  df = pd.DataFrame(myresult, columns=mycursor.column_names)
  return df
