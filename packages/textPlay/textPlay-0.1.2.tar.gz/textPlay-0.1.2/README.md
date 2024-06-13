# TextPlay 💬

**Welcome to the TextPlay repository! 👋**  
This versatile Python module provides a range of text-related functions and tools to enhance your text analysis, summarization, translation, Morse code encoding/decoding, Google search, and more.  

### To use my module
```python
import textPlay
```

## Features

- **Text Summarizer 📝:** Generate concise summaries of long articles, documents, or text.
  
- **Link Summarizer 🌐:** Automatically generate summaries of web articles and provide condensed information.
  
- **Spell Checker ✨:** Correct spelling errors in text to improve text quality.
  
- **Extract Keywords 🔤:** Identify important keywords in text for indexing, tagging, or search optimization.
  
- **Morse Coder and Decoder 🚦:** Encode and decode messages in Morse code for communication or fun.
  
- **Google Search 🔍:** Fetch and display search results from Google.
  
- **Translator 🌍:** Translate text from one language to another.
  
- **Sort Dictionary 📚:** Organize and present data in a specific order.
  
- **Sentiment Analysis 😃:** Perform Sentiment Label, Sentiment Polarity, and Sentiment Subjectivity analysis - simultaneously.
  
- **Simple Chat Bot 💬:** Engage with users, answer queries, and integrate with Google search.

    

  
## Installation

To install the TextPlay module, you can download it directly by using `pip`

```bash
pip install textPlay
```

## Modules Used  
  
**Summarization**
- `spacy`
- `STOP_WORDS` from `spacy.lang.en.stop_words`
- `punctuation` from `string`
- `nlargest` from `heapq`
- `newspaper`

**Sentiment Analysis**
- `TextBlob` from `textblob`

**Spell Checking**
- `SpellChecker` from `spellchecker`

**Web Scraping**
- `requests`
- `BeautifulSoup` from `bs4`

**Translation**
- `Translator` from `googletrans`

**Stop Word Removal**
- `string`

**Bot**
- `random`

**After installing package install a external english module for spacy by:**  
```bash
python -m spacy download en_core_web_sm
```

## Module Detials
- **Version:** `0.1.0`
- **Title:** `textPlay`
- **License:** `Apache License Version 2.0`
- **AUTHOR:** `Rakesh Kanna`
- **Author Email:** [rakeshkanna0108@gmail.com](mailto:rakeshkanna0108@gmail.com)
- **GITHUB LIBRARY:**  https://github.com/rakeshkanna-rk/textPlay
- **GITHUB PROFILE:**  https://github.com/rakeshkanna-rk



