# Code that can be used for custom payload quick replies
response = {}
response["payload"] = {
            "google": {
                "expectUserResponse": "true",
                "richResponse": {
                    "items": [
                        {
                            "simpleResponse": {
                                "textToSpeech": "Choose a item"
                            }
                        }
                    ],
                    "suggestions": [
                        {
                            "title": "Say this"
                        },
                        {
                            "title": "or this"
                        }
                    ]
                },
                "systemIntent": {
                    "intent": "actions.intent.OPTION",
                    "data": {
                        "@type": "type.googleapis.com/google.actions.v2.OptionValueSpec",
                        "listSelect": {
                            "title": "Hello",
                            "items": [
                                {
                                    "optionInfo": {
                                        "key": "first title key"
                                    },
                                    "description": "first description",

                                    "title": "first title"
                                },
                                {
                                    "optionInfo": {
                                        "key": "second"
                                    },
                                    "description": "second description",
                                    "image": {
                                        "url": "https://lh3.googleusercontent.com/Nu3a6F80WfixUqf_ec_vgXy_c0-0r4VLJRXjVFF_X_CIilEu8B9fT35qyTEj_PEsKw",
                                        "accessibilityText": "second alt"
                                    },
                                    "title": "second title"
                                }
                            ]
                        }
                    }
                }
            }
        }

# Using card in fulfillmentMessages
card = {
                "card": {
                    "title": "card title",
                    "subtitle": "card text",
                    "imageUri": "https://assistant.google.com/static/images/molecule/Molecule-Formation-stop.png",
                    "buttons": [
                        {
                            "text": "button text",
                            "postback": "https://assistant.google.com/"
                        }
                    ]
                }
            }


# Topic specific spellcheck
'''
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
                if word != poss and not word in stopwords.words("english") and len(poss) > 4:
                    corrected.append(poss)
                else:
                    corrected.append(word)

            print("corrected: ", corrected)

            if sq != corrected:
                corrected = ' '.join(corrected)
                print("\n\nDid you mean {}?".format(corrected))
                response['fulfillmentText'].append("Did you mean: {}?".format(corrected))
                # response['spellcheck'] = True
                session['spellcheck'] = False
                session['ques_corrected'] = corrected
                session['ques'] = userQuery

            else:
'''