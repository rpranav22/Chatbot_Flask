from flask import Flask, render_template, request, session
from flask import jsonify
from flask_cors import CORS, cross_origin
from flask_restful import Resource,Api
import sys
sys.path.insert(0, '/home/ls41/Desktop/Factoid-based-Question-Answer-Chatbot' )
from spellcheck import spellcheck as SC
from DocumentRetrievalModel import DocumentRetrievalModel as DRM
from ProcessedQuestion import ProcessedQuestion as PQ
from nltk.corpus import stopwords
import re
import os

app = Flask(__name__, static_url_path="/static")
api = Api(app)

CORS(app)

app.secret_key = os.urandom(16)
# session['topic']= None


# drm = None

#############
# Routing
#
@app.route('/message', methods=['POST'])
def reply():
    greetPattern = re.compile("^\ *((hi+)|((good\ )?morning|evening|afternoon)|(he((llo)|y+)))\ *$", re.IGNORECASE)
    receive = request.form['msg']
    # receive = request.data
    userQuery = receive
    print(userQuery)
    # userQuery="Hi"
    print("sess: ", session)
    # userQuery = "Hi"
    response = {}
    response['text']=[]
    # session['filecheck'] = False
    # drm = None
    if (not len(userQuery) > 0):
        print("Bot> You need to ask something")

    elif greetPattern.findall(userQuery):
        response['text'].append("Hello!")
        response['text'].append("You can now send me your topic in the format Topic_Name.txt")
        # res = jsonify({'text': [response,response2]})
        # print(res)
        # return res

    elif userQuery.strip().lower() == "bye":
        response['text'].append("Bye Bye!")
        if 'topic' in session:
            del session['topic']

    elif userQuery.split('.')[-1:] == ['txt']:

        response['text'].append("Thanks for giving the topic, let me load the required files")

        topic = str(userQuery)

        response['topic'] = topic
        # drm = retrievePara(path)
        session['topic'] = topic
        print("now: ",session)
    elif 'topic' in session:
        # Proocess Question
        topic = session['topic']
        sc = SC()
        pq = PQ(userQuery, True, False, True)
        sq = pq.searchQuery
        sq = list(filter(lambda x: x, map(lambda x: re.sub(r'[^A-Za-z]', '', x), sq)))
        print("\nsq: ", sq)
        corrected = []
        # self.stopWords = stopwords.words("english")
        for word in sq:
            # if word in stopwords.words("english"):
            #     continue
            poss = sc.correction(word, topic)
            if word != poss:
                corrected.append(poss)
            else:
                corrected.append(word)

        print("corrected: ", corrected)

        if sq != corrected:
            corrected = ' '.join(corrected)
            print("\n\nDid you mean {}?".format(corrected))
            response['text'].append("Did you mean: {}?".format(corrected))
        else:

            # Get Response From Bot

            print("session topic: ", session['topic'])
            path = 'dataset/' + topic
            drm = retrievePara(path)
            if type(drm) == str:
                response['text'].append(drm)
                del session['topic']
            else:
                response['text'].append(drm.query(pq))

    else:
        response['text'].append("Please provide a relevant topic before you start asking me a question.")

    if 'topic' in session:
        print("topic is in session")


    return jsonify(response)  # execute.decode_line(sess, model, enc_vocab, rev_dec_vocab


@app.route("/", methods=['POST'])
def index():
    # data = request.form['msg']
    # print(data)
    # return render_template("index.html")
    return jsonify({'text': "I really hope this works"})



def retrievePara(datasetName):
    try:
        datasetFile = open(datasetName, "r")
    except FileNotFoundError:
        return "Topic {} not found. Go through the topics and pick one again.".format(''.join(datasetName.split('/')[-1:]))
        # print("Bot> Oops! I am unable to locate \"" + datasetName + "\"")
        # exit()

    # Retrieving paragraphs : Assumption is that each paragraph in dataset is
    # separated by new line character
    paragraphs = []
    for para in datasetFile.readlines():
        if (len(para.strip()) > 0):
            paragraphs.append(para.strip())

    # Processing Paragraphs
    return DRM(paragraphs, True, True)
#############

'''
Init seq2seq model

    1. Call main from execute.py
    2. Create decode_line function that takes message as input
'''
# _________________________________________________________________
# import sys
# import os.path
#
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
# import tensorflow as tf
# import execute
#
# sess = tf.Session()
# sess, model, enc_vocab, rev_dec_vocab = execute.init_session(sess, conf='seq2seq_serve.ini')
# _________________________________________________________________

# start app
if (__name__ == "__main__"):
    app.run(port=5004)
