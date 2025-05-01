NLP Analyzer

This idea builds off of a previous idea to visualize whatsapp chats with interactive charts.

# NLP Analyzer

A comprehensive Python application for analyzing time-stamped chat exports with advanced natural language processing capabilities.

![Dashboard Preview](https://via.placeholder.com/800x450)

## Features

- **Chat Statistics** - Message counts, word usage, activity patterns
- **Sentiment Analysis** - Track emotional tone across conversations and time
- **Topic Modeling** - Discover and visualize conversation themes
- **Multilingual Analysis** - Identify language usage patterns across chats

## Getting Started

### Prerequisites

- Python 3.8+
- Chat Messaging data (.txt format)

### Installation

1. Clone this repository

```bash
git clone https://github.com/CosmicSurgery/NLPanalyzer.git
cd nlp-analyzer
```

2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages

```bash
pip install -r requirements.txt
```

### Usage

1. **Acquire .txt files of chat data**:

   - Open WhatsApp
   - Go to a chat
   - Click on ⋮ (three dots) > More > Export chat > Without media
   - Transfer the .txt files to your computer

2. **Place chat exports in the data folder**:

   - Move all .txt files to `data/DROP_TXT_HERE/`

3. **Process the data**:

```bash
python app.py --process
```

4. **Launch the interactive dashboard**:

```bash
python app.py --dashboard
```

5. **Generate a static report**:

```bash
python app.py --report
```

## Analysis Capabilities

### Basic Chat Statistics

- Message frequency by time (hour, day, month)
- Word count analysis
- Response time patterns
- Media sharing patterns

### Sentiment Analysis

- Message sentiment scoring using VADER and transformer models
- Sentiment trends over time
- Person-to-person sentiment comparison
- Emotional peaks identification

### Topic Modeling

- Automatic discovery of conversation themes
- Topic evolution visualization
- Key phrases identification
- Topic distribution by participant

### Multilingual Analysis

- Language detection and classification
- Language usage patterns
- Code-switching behavior analysis
- Language distribution visualization

## Project Structure

```
project/
├── app.py                  # Main entry point
├── config.yaml             # User configuration
├── data/
│   ├── DROP_TXT_HERE/      # Where users place chat exports
│   ├── processor.py        # Processing pipeline
│   └── status.log          # log file to store results of processing
├── vis/
│   ├── main.py             # Bokeh server setup
│   ├── tabs/               # One module per dashboard tab
│   └── static_report.py    # Static report generator
└── utils/
    └── parser.py           # python helper functions to parse txt file
```

## Technical Implementation

This project utilizes several advanced data science techniques:

- **Text preprocessing** - Regular Expressions, Tokenization, and cleaning
- **Sentiment analysis** - Using VADER and transformer-based models
- **Topic modeling** - LDA and BERTopic implementations
- **Language detection** - Using fasttext language identification models
- **Interactive visualization** - Bokeh dashboards with linked graphs

## Performance Considerations

The application uses:

- HDF5 storage for efficient data management
- Optimized preprocessing pipeline to handle large chat histories

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- NLTK and Hugging Face for NLP tools
- Bokeh for interactive visualizations

Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for
Sentiment Analysis of Social Media Text. Eighth International Conference on
Weblogs and Social Media (ICWSM-14). Ann Arbor, MI, June 2014.

## About the Author

This project was developed as part of my data science portfolio to demonstrate skills in data processing, natural language processing, and interactive visualization.
