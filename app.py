from flask import Flask , render_template
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap 
from wtforms import *
from wtforms.validators import *
import mysql.connector
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = "ADFIAJDO;AWDHJPOAWDAPWODHAW;DOIAWHDUAWOYDGALWIDAWLG"
bootstrap = Bootstrap(app)

class Data():

	def __init__(self):

		self.host = "localhost"
		self.username = "root"
		self.password = "aasrith1906"
		self.database = "blogsite"

	def Connect(self):

		db = None

		try:

			db = mysql.connector.connect(host=self.host,user=self.username,password=self.password,database=self.database)
		
		except Exception as e:

			print(str(e))

		return db

	def AddPost(self,postdata):

		max_sno = None
		sno = 0 

		db = self.Connect()
		
		try:


			cursor = db.cursor()

			cursor.execute("select max(post_num) from blogposts")

		except Exception as e:

			print(str(e))

		for i in cursor:

			max_sno = i[0] 

		if max_sno == None or max_sno == 0:

			sno = 1

		else:

			sno = max_sno + 1 

		cursor = None

		cursor = db.cursor()

		try:

			command_string = "insert into blogposts values("+str(sno)+",'"+ postdata+"'"+",'"+ str(datetime.now()) + "')"

			cursor.execute(command_string)

			for i in cursor:

				if i[0] != None:

					print(i[0])

			db.commit()

			return True

		except Exception as e:

			print(str(e))

			return False

	def GetPosts(self):

		post_list = []
		

		try:

			db = self.Connect()

			cursor = db.cursor()

			command = "select post_data,post_time from blogposts"

			cursor.execute(command)

		except Exception as e:

			print(str(e))

		for post in cursor:

			if post != None:

				post_list.append(post)
				#date_list.append(post[1])
				#print(date_list)

		
		#return post_list

		if len(post_list) != 0:

			i = len(post_list) - 1

			post_list_reverse = []

			while i != 0:

				post_list_reverse.append(post_list[i])

				i = i - 1

			return post_list_reverse

		else:

			return None

		


class PostForm(FlaskForm):

	blog_post = TextAreaField(validators=[DataRequired()])
	submit = SubmitField()

@app.route("/",methods=['GET','POST'])
def MainPage():

	post_form = PostForm()

	DbClient = Data()

	post_list = DbClient.GetPosts()

	if post_list == None:

		post_list = ['No posts']

	if post_form.validate_on_submit():

		post_data = post_form.blog_post.data 

		post_form.blog_post.data = ""

		try:

			DbClient.AddPost(post_data)
			post_list = DbClient.GetPosts()

			if post_list == None:

				post_list = ['No posts']

		except Exception as e:

			print(str(e))


	return render_template('mainpage.html',form = post_form ,post_list= post_list)

if __name__ == '__main__':

	app.run(host="localhost",port='8897',debug=True)
