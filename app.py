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
from os import listdir
from os.path import isfile, join
# import enchant
#
# d = enchant.Dict("en_GB")
app = Flask(__name__, static_url_path="/static")
api = Api(app)

CORS(app, supports_credentials=True)

app.secret_key = b'\xdf\x89M+\xa0\x80#/\xa2\x1f\x86\xe4\xe5\xd0\x90\x89'

# session['topic']= None


# drm = None

#############
# Routing
#
@app.route('/spellcheck', methods=['POST'])
def spellcheck():
    sc = SC()
    userInput = request.form['msg']
    print(userInput, session)
    response = {}
    response['text'] = []
    if 'spellcheck' in session:
        print("entering session spellcheck")
        if userInput == "yes":
            response['spellcheck'] = True
            response['query'] = session['ques_corrected']
            response['text'].append("fine for now")
            del session['spellcheck']
            del session['ques_corrected']
            del session['ques']
        elif userInput == "no":
            response['spellcheck'] = True
            response['query'] = session['ques']
            response['text'].append("going ahead with {}".format(session['ques']))
            del session['spellcheck']
            del session['ques_corrected']
            del session['ques']
        else:
            del session['spellcheck']
            del session['ques_corrected']
            del session['ques']
    else:

        word_list = userInput.split(' ')
        sq = list(filter(lambda x: x, map(lambda x: re.sub(r'[^A-Za-z]', '', x), word_list)))
        print("\nsq: ", sq)
        corrected = []
        # self.stopWords = stopwords.words("english")
        for word in sq:
            # if word in stopwords.words("english"):
            #     continue
            poss = sc.correction(word)
            if word != poss and not word in stopwords.words("english") and len(poss) > 4:
                corrected.append(poss)
            else:
                corrected.append(word)

        print("corrected: ", corrected)

        if sq != corrected:
            corrected = ' '.join(corrected)
            print("\n\nDid you mean: {}?".format(corrected))
            response['text'].append("Did you mean: {}?".format(corrected))
            response['query'] = corrected
            response['spellcheck'] = False
            session['spellcheck'] = False
            session['ques_corrected'] = corrected
            session['ques'] = userInput
        else:
            response['spellcheck']=True
            response['query'] = userInput
            response['text'].append("fine for now")

    return jsonify(response)


@app.route('/message', methods=['POST'])
# @cross_origin
def reply():
    greetPattern = re.compile("^\ *((hi+)|((good\ )?morning|evening|afternoon)|(he((llo)|y+)))\ *$", re.IGNORECASE)
    print(request.get_json())
    receive = request.form.get('msg')
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
    if (userQuery is None):
        print("Bot> You need to ask something")
        response['text'].append("Just trying")
        return jsonify(response)

    elif greetPattern.findall(userQuery):
        response['text'].append("Hello!")
        response['text'].append("You can now send me your topic in the format Topic_Name.txt")

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
    elif 'spellcheck' in session:
        if session['spellcheck'] == False and userQuery.lower() == "yes":
            topic = session['topic']
            ques = session['ques_corrected']
            pq = PQ(ques, True, False, True)
            print("session topic: ", topic)
            path = 'dataset/' + topic
            drm = retrievePara(path)
            response['text'].append(drm.query(pq))
            del session['spellcheck']
            del session['ques_corrected']
            del session['ques']
        else:
            topic = session['topic']
            ques = session['ques']
            pq = PQ(ques, True, False, True)
            print("session topic: ", topic)
            path = 'dataset/' + topic
            drm = retrievePara(path)
            response['text'].append(drm.query(pq))
            del session['spellcheck']
            del session['ques_corrected']
            del session['ques']


    elif 'topic' in session:
        # Proocess Question
        topic = session['topic']
        print("session topic: ", topic)
        path = 'dataset/' + topic
        drm = retrievePara(path)
        if type(drm) == str:
            response['text'].append(drm)
            del session['topic']
        else:
            sc = SC()
            word_list = userQuery.split(' ')
            sq = list(filter(lambda x: x, map(lambda x: re.sub(r'[^A-Za-z]', '', x), word_list)))
            print("\nsq: ", sq)
            corrected = []
            # self.stopWords = stopwords.words("english")
            for word in sq:
                # if word in stopwords.words("english"):
                #     continue
                poss = sc.correction(word, topic)
                if word != poss and not word in stopwords.words("english") and len(poss)>4:
                    corrected.append(poss)
                else:
                    corrected.append(word)

            print("corrected: ", corrected)

            if sq != corrected:
                corrected = ' '.join(corrected)
                print("\n\nDid you mean {}?".format(corrected))
                response['text'].append("Did you mean: {}?".format(corrected))
                response['spellcheck'] = True
                session['spellcheck'] = False
                session['ques_corrected'] = corrected
                session['ques'] = userQuery

            else:

                # Get Response From Bot
                pq = PQ(userQuery, True, False, True)
                response['text'].append(drm.query(pq))
                if 'spellcheck' in session:
                    del session['spellcheck']

    else:
        response['text'].append("Please provide a relevant topic before you start asking me a question.")

    if 'topic' in session:
        print("topic is in session")


    return jsonify(response)  # execute.decode_line(sess, model, enc_vocab, rev_dec_vocab

@app.route("/response", methods=['POST'])
def response():
    json_data = request.get_json()
    intent = json_data["queryResult"]["intent"]["displayName"]


    response = {}
    response['fulfillmentText'] = []
    #
    print("intent: ", intent)
    if intent == "end_session":
        store =[]
        for entry in session:
            store.append(str(entry))
        for ent in store:
            del session[ent]
        print("empty session: ", session)
        response['fulfillmentText'].append("Thank you for talking to me, hope you found what you were looking for. Until next time!")
        return jsonify(response)
    elif intent == "get_topics":
        allFiles = getTopics(id="2345")


        quickReply = {

                "platform": "ACTIONS_ON_GOOGLE",
                "quickReplies": {
                    "title": "Choose one from the list of topics: ",
                    "quickReplies": [


                    ]

                }

        }

        for top in allFiles:
            quickReply["quickReplies"]['quickReplies'].append("select {}".format(top))


        response["fulfillmentMessages"]= [quickReply]

        # response['fulfillmentText'].append("Here are all your topics: pick one. \n{}".format(" ".join(allFiles)))
        del response['fulfillmentText']

        return jsonify(response)
    elif intent == "storeID" or intent == "Retain Id":
        print("store id intent")
        contexts = json_data['queryResult']['outputContexts']
        for entry in contexts:
            if  'id' in entry['parameters']:
                id = entry['parameters']['id']
                session['id'] = id
                print("Just received ID: ", id)
                break

        response['fulfillmentText'] = "ID has been stored."
        return jsonify(response)

    print(request.get_json()['queryResult']['outputContexts'])

    # receive = request.form.get('msg')
    contexts = json_data['queryResult']['outputContexts']
    for entry in contexts:
        print(entry)
        if 'topic_name' in entry['parameters']:
            topic = entry['parameters']['topic_name']
    print("topic: ", topic)
    session['topic'] = topic
    # receive = request.data
    userQuery = json_data['queryResult']['queryText']
    print(userQuery)
    # userQuery="Hi"
    print("sess: ", session)
    # userQuery = "Hi"

    # session['filecheck'] = False
    # drm = None
    if (userQuery is None):
        print("Bot> You need to ask something")
        response['fulfillmentText'].append("Just trying")
        return jsonify(response)



    elif 'topic' in session:
        # Proocess Question
        topic = session['topic']
        print("session topic: ", topic)
        path = 'dataset/' + topic
        drm = retrievePara(path)
        if type(drm) == str:
            response['fulfillmentText'].append(drm)
            del session['topic']
        else:
            # sc = SC()
            # word_list = userQuery.split(' ')
            # sq = list(filter(lambda x: x, map(lambda x: re.sub(r'[^A-Za-z]', '', x), word_list)))
            # print("\nsq: ", sq)
            # corrected = []
            # # self.stopWords = stopwords.words("english")
            # for word in sq:
            #     # if word in stopwords.words("english"):
            #     #     continue
            #     poss = sc.correction(word, topic)
            #     if word != poss and not word in stopwords.words("english") and len(poss) > 4:
            #         corrected.append(poss)
            #     else:
            #         corrected.append(word)
            #
            # print("corrected: ", corrected)
            #
            # if sq != corrected:
            #     corrected = ' '.join(corrected)
            #     print("\n\nDid you mean {}?".format(corrected))
            #     response['fulfillmentText'].append("Did you mean: {}?".format(corrected))
            #     # response['spellcheck'] = True
            #     session['spellcheck'] = False
            #     session['ques_corrected'] = corrected
            #     session['ques'] = userQuery
            #
            # else:

            # Get Response From Bot
            pq = PQ(userQuery, True, False, True)
            response['fulfillmentText'].append(drm.query(pq))
            if 'spellcheck' in session:
                del session['spellcheck']

    else:
        response['fulfillmentText'].append("Please provide a relevant topic before you start asking me a question.")

    if 'topic' in session:
        print("topic is in session")

    # response['fullfillmentText'] = response['fulfillmentText']
    response['source'] = 'ques answer'

    # response["payload"] = {
    #     "google": {
    #         "expectUserResponse": "true",
    #         "richResponse": {
    #             "items": [
    #                 {
    #                     "simpleResponse": {
    #                         "textToSpeech": "this is a simple response"
    #                     }
    #                 }
    #             ]
    #         }
    #     },
    #     "facebook": {
    #         "text": "Hello, Facebook!"
    #     },
    #     "slack": {
    #         "text": "This is a text response for Slack."
    #     }
    # }
    return jsonify(response)


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

def getTopics(id):
    print("id: ", id)
    mypath = "dataset/"
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    print(onlyfiles)
    return onlyfiles

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
