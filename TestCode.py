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