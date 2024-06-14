from experta import KnowledgeEngine, Rule
from experta.fact import Fact
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from random import choice

class Greeting(Fact):
    pass

class Inquiry(Fact):
    pass

class DecisionEngine(KnowledgeEngine):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.vectorizer = TfidfVectorizer()
        self.response = ""
        self.predefined_text = ""
        self.ask_follow_up = False
        self.ask_time_context = False
        self.ask_borrow_context = False
        self.ask_borrow = False
        self.ask_borrow_online = False
        self.ask_return = False
        self.ask_return_context = False
        self.ask_reserve_context = False
        self.ask_submit_context = False
        self.ask_contact_context = False
        self.ask_printing_context = False
        self.ask_requirements_context = False
        self.ask_end_session = False

    def reset_engine(self):
        self.reset()
        self.response = ""
        self.predefined_text = ""
        self.ask_follow_up = False
        self.ask_borrow_context = False
        self.ask_time_context = False
        self.ask_borrow = False
        self.ask_borrow_online = False
        self.ask_return_context = False
        self.ask_return = False
        self.ask_reserve_context = False
        self.ask_submit_context = False
        self.ask_contact_context = False
        self.ask_printing_context = False
        self.ask_requirements_context = False
        self.ask_end_session = False

    def cosine_similarity(self, input_text, predefined_texts):
        input_text_str = ' '.join(input_text)
        tfidf_matrix = self.vectorizer.fit_transform([input_text_str] + predefined_texts)
        similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])
        return similarities.flatten()

    def get_max_similarity(self, sentence, predefined_texts):
        similarities = self.cosine_similarity(sentence, predefined_texts)
        max_similarity = max(similarities)
        max_index = similarities.argmax()
        return max_similarity, max_index

    @Rule(Greeting(text="hi") | Greeting(text="hello") | Greeting(text="good morning") | Greeting(text="good evening") | Greeting(text="good day") | Greeting(text="good eve"))
    def greet_back(self):
        self.response = choice([
            "Hi there! How can I assist you today?",
            "Hello! How may I help you?",
            "Hi! How can I assist you?",
            "Hello. What can I do for you?",
            "How may I assist you?",
            "I'm Lilbot. How can I help you today?"
        ])
        self.ask_follow_up = True

    @Rule(Inquiry(sentence="MATCH.sentence"), salience=1)
    def time_keyword(self, sentence):
        if not self.ask_printing_context and not self.ask_requirements_context and not self.ask_borrow_context and not self.ask_return_context and not self.ask_reserve_context and not self.ask_submit_context and not self.ask_contact_context:
            predefined_texts = [
                "what time does the library opens?", "what is the available time of the library", "what is the closing time of library", 
                "what time does the library open", "what is the library schedule", "What is the library sched?",
                "What is the open hour of the library", "What is the library closing time", 
                "when is the library open", "time of library", "What time is the library open", "What is the daily schedule of the library?",
                "What is the available time of the library", "What is the closing time of library", "What is the library schedule"
            ]
            similarities = self.cosine_similarity(sentence, predefined_texts)
            max_similarity, max_index = self.get_max_similarity(sentence, predefined_texts)
            if any(similarities > 0.8):
                self.response = "Ladislao N. Diwa Memorial Library is open every Monday to Saturday from 7:00 AM to 6:00 PM."
                self.ask_follow_up = True
                self.ask_time_context = True
                self.ask_end_session = True