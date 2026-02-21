import joblib

# Загружаем модель из файла
model = joblib.load("faq_model.pkl")

# Предсказание нового вопроса

def resp(question):
    print("Вопрос:", question)
    prediction = model.predict([question])
    print(model.predict_proba([question]))
    print("Предсказанный класс:", prediction[0])
    return prediction[0]

def test():
    while True:
        question = input("Введите вопрос (или 'exit' для выхода): ")
        if question.lower() == 'exit':
            break
        resp(question)

test()
