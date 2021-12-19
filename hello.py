from flask import Flask,render_template,redirect,url_for,request
from myForms import SearchForm
import getTweets

app = Flask(__name__)

app.config['SECRET_KEY'] = '0x000002033DB9AD00'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

    
@app.route('/',methods=['POST','GET'])
@app.route('/home_page',methods=['POST','GET'])

def home_page():
    form = SearchForm() 
    if request.method == 'POST':
        term = request.form.get('term')
        num = request.form.get('num')
        st= getTweets.tweets(term,num)
        twt= getTweets.twtImg(term,num)
        return redirect(url_for('result_page', st = st,twt=twt))
    return render_template('search.html', form = form)


@app.route('/result',methods=['POST','GET'])
def result_page():  
    st = request.args.get('st')
    twt = request.args.get('twt')
    return render_template('result.html', st = st,twt=twt)

# No caching at all for API endpoints.
@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

if __name__ == "__main__":
    app.run()