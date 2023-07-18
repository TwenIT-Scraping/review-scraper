# from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
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

shortmonths_fr = {
    'janv.':'01',
    'févr.':'02',
    'mars':'03',
    'avr.':'04',
    'mai': '05',
    'juin':'06',
    'juil.':'07',
    'août':'08',
    'sept.':'09',
    'oct.':'10',
    'nov.':'11',
    'déc.':'12'
}

def month_number(name, lang, t=""):
    return globals()[f"{t}months_{lang}"][name]



# class ReviewScore:

#     def __init__(self):
#         self.model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
#         self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
#         self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
#         self.classifier = pipeline('sentiment-analysis', model=self.model, tokenizer=self.tokenizer)

#     def get_score(self, text, lang):
#         if lang in ['en', 'nl', 'de', 'fr', 'it', 'es']:
#             try:
#                 return self.classifier(text.replace('\"', "\'"))
#             except Exception as e:
#                 print(e)
#                 return False
#         else:
#             print("Langue inconnue !!! => ", lang)
#             return False

#     def compute_score(self, text, lang):
#         score_data = self.get_score(text, lang )

#         if score_data:
#             score_value = score_data[0]['score']
#             score_label = score_data[0]['label']
#             score_stars = int(score_label.split()[0])
#             feeling = "negative" if score_stars < 3 else ("positive" if score_stars > 3 else "neutre")

#             if feeling == "negative":
#                 confidence = -1 * score_value
#             elif feeling == "neutre":
#                 confidence = 0
#             else:
#                 confidence = score_value

#             return {'score': score_value, 'confidence': confidence, 'feeling': feeling}
        
#         else:
#             return {'score': 0, 'confidence': 0, 'feeling': "neutre"}

#     def update_scores(self):
#         for review_id in range(1, 5187):
#             print("set value for ", review_id)
#             try:
#                 get_instance = ERApi(method='getone', entity='reviews', id=review_id)
#                 review_data = get_instance.execute()

#                 patch_instance = ERApi(method='put', entity='reviews', id=review_id)
#                 body = {}

#                 if review_data['comment']:
#                     body = self.compute_score(review_data['comment'], review_data['language'])
#                 else:
#                     body = {'score': 0, 'confidence': 0, 'feeling': "neutre"}
                
#                 patch_instance.set_body(body)
#                # print(body)

#                 try:
#                     res = patch_instance.execute()
#                     print(res)
#                 except Exception as e:
#                     print(e)
                    
#             except Exception as e:
#                 print(e)
#                 pass


# review_score = ReviewScore()
# review_score.update_scores()
