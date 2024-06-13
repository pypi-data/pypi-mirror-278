'''
A Collection of Text Modeling

10 Functions:

summarizer --summarizer(text, num_sentences=0.4)
link summarizer --link_summary(article_url, num_sentences=0.4, summary=False)
spell checker --corrector(sentence)
remove stopwords --wordy(text, exclusion_list=None)
morsecode --MorseCoderDecoder.morse_coder(text)
morsedecode --MorseCoderDecoder.morse_decoder(morse_code)
Google scearch --google_search(query, num_results=1)
Translation --transify(text, translat_code)
dictionary sorter --dictkey(input_dict, reverse=False)
dictionary sorter --dictvalue(input_dict, reverse=False)
ChatBot --txtBot(text, g_result)
sentiment analysis --sentiment_analysis(text)

'''


VERSION = "0.1.1"
TITLE = "textPlay"
LICENSE = "Apache License Version 2.0"
AUTHOR = "Rakesh Kanna"
GITHUB_PROFILE = "https://github.com/rakeshkanna-rk"
GITHUB_LIBRARY = "https://github.com/rakeshkanna-rk/textPlay"


__all__ = [
    "summarizer",
    "link_summary",
    "corrector",
    "wordy",
    "MorseCoderDecoder",
    "google_search",
    "text_translator",
    "analyze_sentiment",
    "Spellify",
    "dictkey",
    "dictvalue",
    "BaseBot",
]

import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: textplay <command>")
        sys.exit(1)
    
    command = sys.argv[1]
    if command == 'summarizer':
        summarizer.main()
    elif command == 'link_summary':
        link_summary.main()
    elif command == 'corrector':
        Spellify.main()
    elif command == 'morse_coder':
        MorseCoderDecoder.main()
    elif command == 'google_search':
        google_search.main()
    elif command == 'text_translator':
        text_translator.main()
    elif command == 'wordy':
        wordy.main()
    elif command == 'dictkey':
        dictkey.main()
    elif command == 'dictvalue':
        dictvalue.main()
    elif command == 'base_bot':
        BaseBot.main()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

#================================================================================================

import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
import newspaper


def summarizer(text, num_sent=0.3):

    """
    Summarize a given text using extractive summarization.

    Parameters:
    - text (str): The input text to be summarized.
    - num_sent (float, optional): The proportion of sentences to include in the summary (default is 0.3, which means 30% of sentences).

    Returns:
    str: The summarized text.

    Note:
    This function uses extractive summarization to generate a concise summary of the input text.
    It tokenizes the text, calculates word frequencies, and scores sentences based on word frequency.
    The top 'num_sent' sentences with the highest scores are selected to form the summary.

    Example:
    >>> input_text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit..."
    >>> summary = summarizer(input_text, num_sent=0.2)
    >>> print(summary)
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit..."
    """


    #Listing stop words
    stopwords = list(STOP_WORDS)

    #Loading spacy
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)

    #Tokenizing
    tokens = [token.text for token in doc]

    #Creating word frequency
    word_freq = {}
    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
          if word.text not in word_freq.keys():
              word_freq[word.text] = 1
          else:
              word_freq[word.text] += 1


    #Normalizing word frequency
    max_freq = max(word_freq.values())

    #Normalizing word frequency with maximum frequency
    for word in word_freq.keys():
        word_freq[word] = word_freq[word]/max_freq

    #Creating sentence
    sent_tokens = [sent for sent in doc.sents]

    #Creating sentence frequency
    sent_score = {}
    for sent in sent_tokens:
        for word in sent:
            if word.text in word_freq.keys():
                if sent not in sent_score.keys():
                    sent_score[sent] = word_freq[word.text]
                else:
                    sent_score[sent] += word_freq[word.text]


    #Selecting top 'num_sent' sentences
    select_len = int(len(sent_tokens) * num_sent)

    #Creating summary
    summary =  nlargest(select_len, sent_score, key=sent_score.get)

    #final summary
    final_summary = [word.text for word in summary]
    summary = ' '.join(final_summary)

    return summary






def link_summary(article_url, num_sentences=0.5, summary=False):

    """
    Summarize a web article given its URL using Newspaper3k and extractive summarization.

    Parameters:
    - article_url (str): The URL of the web article to be summarized.
    - num_sentences (float, optional): The proportion of sentences to include in the summary (default is 0.5, which means 50% of sentences).
    - summary (bool, optional): If True, return the raw article summary (default is False). If False, further summarize the raw summary using extractive summarization.

    Returns:
    str: The summarized text of the web article.

    Note:
    This function uses the Newspaper3k library to extract and summarize content from a web article.
    It downloads and parses the article content and performs NLP-based summarization.
    If 'summary' is True, it returns the raw article summary; otherwise, it further summarizes the summary using extractive summarization based on 'num_sentences'.

    Example:
    >>> article_url = "https://example.com/article"
    >>> summary = link_summary(article_url, num_sentences=0.3, summary=False)
    >>> print(summary)
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit..."
    """
        
    # Initialize a newspaper Article object
    article = newspaper.Article(article_url)
    
    # Download and parse the article content
    article.download()
    article.parse()
    
    # NLP-based summarization using Newspaper3k
    article.nlp()
    
    # Get the summary
    summary = article.summary
    
    # Split the summary into sentences
    summary_sentences = summary.split('. ')
    
    # Select the top 'num_sentences' sentences for the summary
    final_summary = '. '.join(summary_sentences[:5])

    # Return the summary if True:
    if summary == True:
        if not final_summary:
            final_summarized = final_summary
            return final_summarized
    else:
            final_summarized = summarizer(final_summary, num_sentences)

    return final_summarized

#=========================================================================================

from textblob import TextBlob

def analyze_sentiment(text):

    """
    Analyze the sentiment of a given text using TextBlob's sentiment analysis.

    Parameters:
    - text (str): The input text to be analyzed for sentiment.

    Returns:
    tuple: A tuple containing sentiment information in the following format:
        (sentiment_label, sentiment_polarity, sentiment_subjectivity)

        - sentiment_label (str): The sentiment label indicating whether the text is 'positive', 'negative', or 'neutral'.
        - sentiment_polarity (float): The sentiment polarity score ranging from -1 (negative) to 1 (positive).
        - sentiment_subjectivity (float): The sentiment subjectivity score ranging from 0 (objective) to 1 (subjective).

    Note:
    This function utilizes TextBlob's sentiment analysis to determine the sentiment of the input text.
    The 'sentiment_label' provides a categorical sentiment label, 'sentiment_polarity' indicates the sentiment score,
    and 'sentiment_subjectivity' measures the text's subjectivity.

    Example:
    >>> result = analyze_sentiment("I love this product! It's amazing.")
    >>> sentiment_label, sentiment_polarity, sentiment_subjectivity = result
    >>> print(f"Sentiment Label: {sentiment_label}")
    "Sentiment Label: positive"
    >>> print(f"Sentiment Polarity: {sentiment_polarity}")
    "Sentiment Polarity: 0.6"
    >>> print(f"Sentiment Subjectivity: {sentiment_subjectivity}")
    "Sentiment Subjectivity: 0.8"
    """

    try:
        # Create a TextBlob object
        blob = TextBlob(text)

        # Get the sentiment polarity (-1 to 1, where -1 is negative, 1 is positive)
        sentiment_polarity = blob.sentiment.polarity

        # Determine sentiment labels based on polarity
        if sentiment_polarity > 0:
            sentiment_label = "positive"
        elif sentiment_polarity < 0:
            sentiment_label = "negative"
        else:
            sentiment_label = "neutral"

        # Get the sentiment subjectivity (0 to 1, where 0 is objective, 1 is subjective)
        sentiment_subjectivity = blob.sentiment.subjectivity

        return sentiment_label, sentiment_polarity, sentiment_subjectivity

    except Exception as e:
        # Handle any exceptions that may occur during sentiment analysis
        print(f"Error during sentiment analysis: {str(e)}")
        return "unknown", 0.0, 0.0


#=========================================================================================


from spellchecker import SpellChecker

class Spellify:
    def __init__(self):
        """
        Initialize a Spellify instance.

        This class uses the SpellChecker from the spellchecker library to provide spelling correction functionality.

        Usage:
        my_module = Spellify()
        """
        self.spell = SpellChecker()

    def corrector(self, sentence):
        """
        Correct the spelling of words in a sentence.

        Args:
            sentence (str): The input sentence to be corrected.

        Returns:
            str: The corrected sentence.

        This method takes an input sentence and performs spelling correction on each word using the SpellChecker.
        It splits the input sentence into words, corrects each word, and reconstructs the corrected sentence.

        Usage:
        my_module = Spellify()
        input_sentence = "Thes is an example of a sentance with speling errors."
        corrected_sentence = my_module.correct_sentence(input_sentence)
        print("Original Sentence:", input_sentence)
        print("Corrected Sentence:", corrected_sentence)
        """
        # Split the sentence into words
        words = sentence.split()

        # Correct each word and build the corrected sentence
        corrected_words = [self.spell.correction(word) for word in words]

        # Reconstruct the sentence
        corrected_sentence = ' '.join(corrected_words)

        return corrected_sentence



#=========================================================================================


import requests
from bs4 import BeautifulSoup


def google_search(query, num_results=1):
    """
    Parameters:
    - query (str): The search query to be used.
    - num_results (int, optional): The number of top results to retrieve (default is 1).

    Returns:
    str: A string containing the top search results.

    Note:
    This function performs a Google search using the provided query and retrieves
    the specified number of top results. It uses web scraping techniques to parse
    Google's search results page and extract relevant information.

    Example:
    >>> search_query = "Python programming"
    >>> top_results = google_search(search_query, num_results=3)
    >>> print(top_results)
    """
    try:
        search_url = f"https://www.google.com/search?q={query}"
        response = requests.get(search_url)
        soup = BeautifulSoup(response.text, "html.parser")

        search_results = soup.find_all("div", class_="BNeawe")
        top_results = [result.text for result in search_results[:num_results]]


        if not top_results:
            print("No results found")
        else:
            result_text = "\n\n".join(top_results)
            if len(result_text) < 3:
                more_results = google_search(query, num_results=5)  # Show next 5 results
                if more_results:
                    result_text += "\n" + "\n".join(more_results)

        return result_text

    except Exception as e:
        print(e)


#=========================================================================================


from googletrans import Translator


def text_translator(text, target_language):
    """
    Translate text to the specified target language using Google Translate.

    Parameters:
    - text (str): The input text to be translated.
    - target_language (str): The language code (e.g., 'en' for English) of the target language.

    Returns:
    str: The translated text in the specified target language.

    Note:
    This function uses the Google Translate API to translate the input text to the specified target language.
    The 'target_language' parameter should be a valid language code (e.g., 'en' for English).
    
    Example:
    >>> translated_text = text_translator("Hello, how are you?", 'es')
    >>> print(translated_text)
    "Hola, ¿cómo estás?"
    """
    translator = Translator()
    translation = translator.translate(text, dest=target_language)
    return translation.text



#=========================================================================================



import string

def wordy(text, exclusion_list=None):
    """
    Extract keywords from text by removing common stop words and specified exclusions.

    Parameters:
    - text (str): The input text from which keywords will be extracted.
    - exclusion_list (set, optional): A set of words to be excluded from keyword extraction (default is None).

    Returns:
    list: A list of unique keywords extracted from the input text after filtering out stop words and exclusions.

    Note:
    This function uses spaCy for text processing and filtering. It removes common stop words, punctuation, and words
    specified in the exclusion list (if provided), resulting in a list of unique keywords.

    Example:
    >>> text = "This is an example text with common words."
    >>> exclusion_list = {"example", "common"}
    >>> keywords = wordy(text, exclusion_list)
    >>> print(keywords)
    ['text', 'words']
    """
    # Load the English language model from spaCy
    nlp = spacy.load("en_core_web_sm")

    # Process the input text
    doc = nlp(text)

    # Use the provided exclusion_list or an empty set if not provided
    if exclusion_list is None:
        exclusion_list = set()

    # Filter out stop words, punctuation, and specific words
    keywords = [token.text.lower() for token in doc if token.text.lower() not in STOP_WORDS and token.text.lower() not in exclusion_list and token.text not in string.punctuation]

    # Remove duplicate keywords (if any)
    unique_keywords = list(set(keywords))

    return unique_keywords


#=========================================================================================




class MorseCoderDecoder:
    """
    A class for encoding and decoding text to/from Morse code.

    Usage:
    morse_coder_decoder = MorseCoderDecoder()
    encoded_text = morse_coder_decoder.morse_coder("Hello, World!")
    decoded_text = morse_coder_decoder.morse_decoder(encoded_text)
    """

    def __init__(self):
        # Define a dictionary mapping characters to Morse code
        self.morse_code_dict = {
            'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....',
            'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.',
            'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
            'Y': '-.--', 'Z': '--..',
            'a': '.-|', 'b': '-...|', 'c': '-.-.|', 'd': '-..|', 'e': '.|', 'f': '..-.|', 'g': '--.|', 'h': '....|',
            'i': '..|', 'j': '.---|', 'k': '-.-|', 'l': '.-..|', 'm': '--|', 'n': '-.|', 'o': '---|', 'p': '.--.|',
            'q': '--.-|', 'r': '.-.|', 's': '...|', 't': '-|', 'u': '..-|', 'v': '...-|', 'w': '.--|', 'x': '-..-|',
            'y': '-.--|', 'z': '--..|',
            '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....', '6': '-....',
            '7': '--...', '8': '---..', '9': '----.',
            ' ': '/'
        }


    def morse_coder(self, text):
        """
        Encode text to Morse code.

        Args:
            text (str): The input text to be encoded.

        Returns:
            str: The encoded Morse code.
        """
        morse_code = []
        for char in text.upper():
            if char in self.morse_code_dict:
                morse_code.append(self.morse_code_dict[char])
            else:
                morse_code.append(char)  # Keep non-alphanumeric characters as they are
        return ' '.join(morse_code)


    def morse_decoder(self, morse_code):
        """
        Decode Morse code to text.

        Args:
            morse_code (str): The input Morse code to be decoded.

        Returns:
            str: The decoded text.
        """
        morse_dict = {value: key for key, value in self.morse_code_dict.items()}

        words = morse_code.strip().split(" / ")
        decoded_words = []

        for word in words:
            decoded_letters = []
            letters = word.split()

            for letter in letters:
                if letter in morse_dict:
                    decoded_letters.append(morse_dict[letter])
                else:
                    decoded_letters.append(letter)

            decoded_words.append("".join(decoded_letters))

        return " ".join(decoded_words)

'''
# Example usage:
if __name__ == "__main__":
    morse_coder_decoder = MorseCoderDecoder()
    encoded_text = morse_coder_decoder.morse_coder("Hello, World!")
    decoded_text = morse_coder_decoder.morse_decoder(encoded_text)
    print("Encoded Text:", encoded_text)
    print("Decoded Text:", decoded_text)
'''

#=========================================================================================

def dictkey(input_dict, reverse=False):

    """
    Sort a dictionary by its keys, optionally in reverse order.

    Parameters:
    - input_dict (dict): The input dictionary to be sorted.
    - reverse (bool, optional): If True, sort the dictionary in reverse order (default is False).

    Returns:
    dict: A new dictionary with the keys sorted in ascending or descending order based on the 'reverse' parameter.

    Note:
    This function takes a dictionary as input and sorts its keys in either ascending or descending order.
    If 'reverse' is True, the keys will be sorted in descending order; otherwise, they will be sorted in ascending order.

    Example:
    >>> input_dict = {'apple': 3, 'banana': 2, 'cherry': 1}
    >>> sorted_dict = dictkey(input_dict)
    >>> print(sorted_dict)
    {'apple': 3, 'banana': 2, 'cherry': 1}
    
    >>> reversed_dict = dictkey(input_dict, reverse=True)
    >>> print(reversed_dict)
    {'cherry': 1, 'banana': 2, 'apple': 3}
    """
    
    if not isinstance(input_dict, dict):
        return {}

    try:
        return dict(sorted(input_dict.items(), key=lambda x: x[0], reverse=reverse))
    except TypeError:
        print("Error: Unable to sort the dictionary by keys.")
        return input_dict


def dictvalue(input_dict, reverse=False):

    """
    Sort a dictionary by its values, optionally in reverse order.

    Parameters:
    - input_dict (dict): The input dictionary to be sorted.
    - reverse (bool, optional): If True, sort the dictionary in reverse order (default is False).

    Returns:
    dict: A new dictionary with the keys sorted based on their corresponding values in ascending or descending order.

    Note:
    This function takes a dictionary as input and sorts its keys based on the values associated with each key.
    If 'reverse' is True, the keys will be sorted in descending order of their values; otherwise, they will be sorted in ascending order.

    Example:
    >>> input_dict = {'apple': 3, 'banana': 2, 'cherry': 1}
    >>> sorted_dict = dictvalue(input_dict)
    >>> print(sorted_dict)
    {'cherry': 1, 'banana': 2, 'apple': 3}
    
    >>> reversed_dict = dictvalue(input_dict, reverse=True)
    >>> print(reversed_dict)
    {'apple': 3, 'banana': 2, 'cherry': 1}
    """

    if not isinstance(input_dict, dict):
        return {}

    try:
        return dict(sorted(input_dict.items(), key=lambda x: x[1], reverse=reverse))
    except TypeError:
        print("Error: Unable to sort the dictionary by values.")
        return input_dict



#=========================================================================================


GREETING_RESPONSES=[
    "Hi there! How can I help you?",
    "Hello, Whatsup?",
    "Hi👋, How its going",
    "Hey my dear, wanna try text-to-speech? \nUse /tts",
    "Hey there!",
    "Hey, how are you doing?",
    "Greetings!",
    "What's up?",
    "Howdy!",
    "Hey!",
    "Good to see you!",
    "Hi, how can I assist you today?",
    "Yo!",
    "Hi, nice to meet you!",
    "Hi, what brings you here?",
    "Hello, how can I be of service?",
    "Hey, how's your day going?",
    "Hi, how's it going?",
    "Hi, what's happening?",
    "Hello, how's everything?",
    "Hey, how can I help you today?",
    "Hi, how's your day so far?",
    "Hello, how can I assist you?",
    "Hey, how's life treating you?",
    "Hi, what can I do for you?",
    "Hello, how are you today?",
    "Hey, what's going on?",
    "Hi, how can I support you?",
    "Hello, how may I assist you?",
    "Hey, what can I do for you today?",
    "Hi, how's everything going?",
    "Hello, how's your day been?",
    "Hey, how can I be of help?",
    "Hi, how's your day treating you?",
    "Hello, what's new with you?",
    "Hey, how can I make your day better?",
    "Hi, what's on your mind?",
    "Hello, how can I make your life easier?",
    "Hey, how can I make you smile today?",
    "Hi, what's the latest?",
    "Hello, how can I lighten your load?",
    "Hey, what's happening in your world?",
    "Hi, how can I assist you right now?",
    "Hello, how can I make your day brighter?",
    "Hey, what's been going on?",
    "Hi, how can I bring a little joy to your day?",
    "Hello, what's happening in your life?",
    "Hey, how can I make your day more enjoyable?",
    "Hi, what's been going on with you?",
    "Hello, how can I make your day more productive?",
]





import random

class BaseBot:
    """
    A simple text-based chatbot that responds to user input based on predefined responses.
    with predefined responses og GREETING_RESPONSES

    Attributes:
    - responses (dict): A dictionary containing keyword-response pairs for the chatbot.

    Methods:
    - get_response(text): Returns a response based on the provided user input text.
    """

    def __init__(self, responses, errormsg="I'm sorry, I don't have that information right now."):
        """
        Initialize the chatbot with predefined responses.

        Parameters:
        - responses (dict): A dictionary containing keyword-response pairs.
        """
        self.responses = responses
        self.errormsg = errormsg

    def textBot(self, text, g_results=3):
        """
        Get a response based on the user input text.else search in google

        Parameters:
        - text (str): The user's input text.
        - g_search (int): The search query

        Returns:
        str: A response generated by the chatbot based on the input.
        """
        for keyword, response_text in self.responses.items():
            if keyword in text.lower():
                # Check if the response_text is a list of options
                if isinstance(response_text, list):
                    return random.choice(response_text)
                else:
                    pass
            else:
                google = google_search(text, g_results)
                if not google:
                    return self.errormsg
                else:
                    return google

'''
# Example usage:
responses = {
    "hi": ["Hello there!", "Hi there!", "Hey there!"],
    "hello": ["Hello there!", "Hi there!"],
    "how are you": ["I'm just a bot, but I'm doing well. How can I assist you?"],
    "goodbye": ["Goodbye! Have a great day!"],
    # Add more keyword-response pairs as needed
}

# Create an instance of BaseBot
bot = BaseBot(responses)

user = input("User: ")
print (f"Hello {user} nice to meet you\n\n")
while True:
    user_input = input(f"{user}: ")
    bot_output = bot.textBot(user_input)
    print("Bot:", bot_output,"\n")
'''

















'''
**Disclaimer:**

The module used within this application may contain copyrighted materials. 
This module has been created solely for the purpose of enhancing user conven
ience and simplifying tasks. It is important to recognize that the module's 
functionality and content may be subject to copyright protection by their respective
owners. The use of this module should adhere to all relevant copyright laws and regulations. 
Users are responsible for ensuring compliance with copyright restrictions when using this module. 
The module's developers do not endorse or encourage any unauthorized use ofcopyrighted material
and assume no liability for any such use. Users are advised to exercise caution and seek
appropriate permissions or licenses when dealing with copyrighted content. This module should be
 used responsibly and ethically.
'''