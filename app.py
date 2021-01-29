#  app for crud tact

from flask import Flask, render_template, request
import pymongo
from decouple import config

myclient = pymongo.MongoClient(config("MONGO_URI"))
db = myclient.data
collection = db.bestlines

app = Flask(__name__)

@app.route('/',methods=["POST","GET"])
def main():
    return render_template('main.html')

@app.route('/main/create',methods=["POST","GET"])
def main_create():
    return render_template('create.html')

@app.route('/create',methods=["POST","GET"])
def create():
    author = request.form['author'] 
    if author == '':
        return 'Enter values '
    else:
        author = request.form['author'] 
        quote = request.form['quote'] 
        my_dict = {'_id':author.title().strip(), 'names': quote.title().strip()}
        collection.insert_one(my_dict)
        q = 'author - '+author.title().strip()+'\n'+'quote - '+quote.title().strip()
        return render_template('status.html',q=q)

@app.route('/read',methods=["POST","GET"])
def read():
    get = collection.find()
    return render_template('statusread.html',get=get)
    
@app.route('/main/update',methods=["POST","GET"])
def main_update():
    return render_template('update.html')

@app.route('/update',methods=["POST","GET"])
def update():
    author = request.form['author']
    if author == '':
        return 'Enter values '
    else:
        author = request.form['author']
        quote = request.form['quote']
        myquery = { "_id":author.title().strip() }
        newvalues = { "$set": { "names":quote.title().strip() } }
        collection.update_one(myquery, newvalues)
        q = 'Author - '+author.title().strip()+'  Quote - '+quote.title().strip()
        return render_template('statusupdate.html',q=q)

@app.route('/main/delete',methods=["POST","GET"])
def main_delete():
    return render_template('delete.html')

@app.route('/delete',methods=["POST","GET"])
def delete():
    author = request.form['author']
    if author == '':
        return 'Enter values '
    else:
        author = request.form['author']
        get = 'Deleted Successfully - '+author.title().strip()
        my_dict = { "_id": author.title().strip() }
        collection.delete_one(my_dict)
        return render_template('statusdelete.html',get=get)

@app.route('/find/quotes',methods=["POST","GET"])
def find_quotes():
    get = collection.find({},{"_id":0,"names":1})
    return render_template('quotes.html',get=get)

@app.route('/find/authors',methods=["POST","GET"])
def find_authors():
    get = collection.find({},{"_id":1})
    return render_template('authors.html',get=get)

if __name__ =="__main__":
    app.run(debug=True)