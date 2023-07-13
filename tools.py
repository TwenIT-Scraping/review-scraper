from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from api import ERApi
from random import randint, random


months_fr = {
    'janvier': '01',
    'février': '02',
    'mars': '03',
    'avril': '04',
    'mai': '05',
    'juin': '06',
    'juillet': '07',
    'août': '08',
    'septembre': '09',
    'octobre': '10',
    'novembre': '11',
    'décembre': '12'
}

months_en = {
    'January': '01',
    'February': '02',
    'March': '03',
    'April': '04',
    'May': '05',
    'June': '06',
    'July': '07',
    'August': '08',
    'September': '09',
    'October': '10',
    'November': '11',
    'December': '12'
}

def month_number(name, lang):
    return globals()[f"months_{lang}"][name]

def get_score(text):
    model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    classifier = pipeline('sentiment-analysis', model=model, tokenizer=tokenizer)
    print(classifier(text))

get_score("Leur service n'est pas au top")

def random_score():

    for review_id in range(2168, 4496):
        print("set value for ", review_id)
        patch_instance = ERApi(method='put', entity='reviews', id=review_id)
        score = float("%.2f" % random())
        feeling = ["negative", "neutre", "positive"][randint(0,2)]

        if feeling == "negative":
            confidence = -1 * score
        elif feeling == "neutre":
            confidence = 0
        else:
            confidence = score
        
        body = {"feeling": feeling, "confidence": confidence, "score": score}

        patch_instance.set_body(body)

        try:
            res = patch_instance.execute()
        except Exception as e:
            print(e)


# random_score()