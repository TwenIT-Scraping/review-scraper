# from transformers import AutoTokenizer, AutoModelForSequenceClassifier, pipeline


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

# def get_score(text):
#     model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
#     model = AutoModelForSequenceClassification.from_pretrained(model_name)
#     tokenizer = AutoTokenizer.from_pretrained(model_name)
#     classifier = pipeline('sentiment-analysis', model=model, tokenizer=tokenizer)
#     print(classifier(text))

# get_score("Leur service n'est pas au top")