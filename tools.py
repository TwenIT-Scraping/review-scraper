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


class ReviewScore:

    def __init__(self):
        self.model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.classifier = pipeline('sentiment-analysis', model=self.model, tokenizer=self.tokenizer)

    def get_score(self, text, lang):
        if lang in ['en', 'nl', 'de', 'fr', 'it', 'es']:
            return self.classifier(text.replace('\"', "\'"))
        else:
            return False

    def update_scores(self):
        for review_id in range(1, 5):
            print("set value for ", review_id)
            try:
                get_instance = ERApi(method='getone', entity='reviews', id=review_id)
                review_data = get_instance.execute()

                patch_instance = ERApi(method='put', entity='reviews', id=review_id)
                body = {}

                if review_data['comment']:
                    score_data = self.get_score(review_data['comment'])
                    score_value = score_data['score']
                    score_label = score_data['label']
                    score_stars = int(score_label.split()[0])
                    feeling = "negative" if score_stars < 3 else ("positive" if score_stars > 3 else "neutre")

                    if feeling == "negative":
                        confidence = -1 * score_value
                    elif feeling == "neutre":
                        confidence = 0
                    else:
                        confidence = score_value

                    body = {'score': score_value, 'confidence': confidence, 'feeling': feeling}
                
                else:
                    body = {'score': 0, 'confidence': 0, 'feeling': "neutre"}
                
                patch_instance.set_body(body)

                try:
                    patch_instance.execute()
                except Exception as e:
                    print(e)
                    
            except Exception as e:
                print(e)
                pass


# def get_score(text):
    
#     print(classifier(text))

# get_score("Leur service n'est pas au top")

review_score = ReviewScore()
review_score.update_scores()



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