NLP Analyzer

This idea builds off of a previous idea to visualize whatsapp chats with interactive charts.

# NLP Analyzer

A comprehensive Python application for analyzing time-stamped chat exports with advanced natural language processing capabilities.

https://github.com/user-attachments/assets/1943a761-5a7e-4b46-bd0f-33fa6843f343

## Features

- **Timeseries analysis** - Hourly Message data (PDF), Cumulative Messages over time (CDF), with first and second order filters (Savitzky-Golay)
- **Multilingual Analysis** - Identify language usage patterns across conversations with [Lingua-py](https://github.com/pemistahl/lingua-py)
- **Sentiment Analysis** - Track emotional tone across conversations and time (Very Negative, Negative, Neutral, Postive, Very Positive) with BERT-based sentiment classifier [Tabularis.ai](https://huggingface.co/tabularisai/multilingual-sentiment-analysis)
- **Topic Modeling** - Visualize topic clusters emerge in conversation data over time with [Siamese BERT-networks](paraphrase-multilingual-mpnet-base-v2)

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

5. **Clear the data and start over**:

```bash
python app.py --clear
```

## Analysis Capabilities

### Basic Chat Statistics

- Message frequency by time (hourly distribution, dayly average, cumulative sum)
- Word count analysis [Coming]
- Response time patterns [Coming]
- Media sharing patterns [Coming]

### Sentiment Analysis

- Message sentiment scoring using Tabularis.ai and transformer models
- Sentiment trends over time
- Person-to-person sentiment comparison
- Emotional peaks identification

### Topic Modeling

- Automatic clustering of conversation topics [Coming]
- Topic distribution evolution visualization
- Key phrases identification [Coming]
- Topic distribution by participant [Coming]

### Multilingual Analysis

- Language detection and classification
- Language usage patterns [Coming]
- Code-switching behavior analysis [Coming]
- Language distribution visualization

## Project Structure

```
project/
├── app.py                  # Main entry point
├── config.yaml             # User configuration
├── requirements.txt             # User configuration
├── data/
│   ├── DROP_TXT_HERE/      # Where users place chat exports
│   ├── processor.py        # Processing pipeline
│   └── status.log          # log file to store results of processing
├── vis/
│   ├── main.py             # Bokeh server setup
│   └── tabs/               # One module per dashboard tab
└── utils/
    └── parser.py           # python helper functions to parse txt file
```

## Technical Implementation

This project utilizes several advanced data science techniques:

- **Text preprocessing** - Regular Expressions, Tokenization, and cleaning
- **Sentiment analysis** - Using Tabularis.ai and transformer-based models
- **Topic modeling** - BERTopic implementations with a fine-tuned model [Siamese BERT-networks](paraphrase-multilingual-mpnet-base-v2)
- **Language detection** - Using lingua-py python package
- **Interactive visualization** - Bokeh dashboards with linked graphs

## Performance Considerations

The application uses:

- HDF5 storage for efficient data management
- Optimized preprocessing pipeline to handle large chat histories, although inference using these powerful models can be very slow during pre-proessing...

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- BERTopic, Tabularis.ai, Lingua-py and Hugging Face for NLP tools
- Bokeh for interactive visualizations

## About the Author

This project was developed as part of my data science portfolio to demonstrate skills in data processing, natural language processing, and interactive visualization.
