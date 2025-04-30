from tqdm import tqdm
import re
import os
import json
import pandas as pd
import time

from lingua import LanguageDetectorBuilder, Language

def detectPattern(s):
    patterns = [
    r'^(\d+/\d+/\d+, \d+:\d+\d+ [A-Z]*) -',
    r'^(\d+/\d+/\d+ \d+:\d+\d+) -',
    r'^(\[\d+-\d+-\d+ \d+:\d+\d+\])' # <---- Add other leading timestamp regex patterns here
    ]
    
    for i,p in enumerate(patterns):
        if len(re.split(p,s)) > 1:
            return patterns[i]
    
    raise ValueError(f"No timestamp pattern detected for file {file}")

def startsWithDatetime(s, p):
    if len(re.split(p, s)[1:]) > 1:
        return True
    return False

def startsWithAuthor(s):
    return len(s.split(':', maxsplit=1)) > 1

def load_status_log(PATH):
    if os.path.exists(os.path.join(PATH,"status.log")):
        with open(os.path.join(PATH,"status.log"), "r") as f:
            try:
                return json.load(f)
            except:
                return {"success": [], "failed": {}}
    return {"success": [], "failed": {}}

def save_status_log(status, PATH):
    with open(os.path.join(PATH,"status.log"), "w") as f:
        json.dump(status, f, indent=2)

# Transforms the Datetime column to type pandas Datetime, also returns any files that don't match with a provided datetime format
def detect_datetime_formats(df):
    result_df = df.copy()
    conversation_formats = {}
    formats = [ '%Y-%m-%d %H:%M',"%d/%m/%y %H:%M",'%m-%d-%Y %H:%M', "%m/%d/%y, %I:%M %p"]
    drops = []
    for conversation_id, group in df.groupby('Conversation'):
        original_indices = group.index.tolist()
        format_scores = []
        
        for format_ in formats:

            try:
                parsed_dates = pd.to_datetime(
                    group['Datetime'], 
                    format=format_
                )
                ordering_score = (original_indices == parsed_dates.sort_values().index).mean()
                format_scores.append((format_, ordering_score))
            except:
                format_scores.append((format_, 0.0))

        format_scores.sort(key=lambda x:x[1],reverse=True)
        best_format = format_scores[0]

        mask = result_df['Conversation'] == conversation_id
        result_df.loc[mask, 'Datetime'] = pd.to_datetime(
            result_df.loc[mask, 'Datetime'],
            format=best_format[0]
        )

        
        if best_format[1] < 0.1:
            drops.append(conversation_id)
            
    for conversation_id in drops:
        result_df = result_df[result_df.Conversation != conversation_id]
       
    return result_df, drops


# This is a function that will take a dataframe with column "Message", and option list of languages ( ie. ['ENGLISH','SPANISH'])
# and return the same dataframe with additional columns n=len(detect) with a one-hot encoding of the languages detected
def lang_detect(df, detect=['ENGLISH','SPANISH']):
    languages = [getattr(Language, k) for k in detect]
    detector = LanguageDetectorBuilder.from_languages(*languages).build()
    langs = df.Message.apply(lambda x:detector.detect_language_of(x))
    langs = langs.apply(lambda x:x.name if x is not None else None)
    langs = pd.get_dummies(langs)
    return pd.concat((df,langs),axis=1)

def main(PATH=None):


    if PATH is None:
        PATH = os.getcwd()

    # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath('DROP_TXT_HERE')))
    # PATH = os.path.join(BASE_DIR, 'DROP_TXT_HERE')
    directory = os.listdir(os.path.join(PATH,'DROP_TXT_HERE'))

    status = load_status_log(PATH)
    successful_files = []
    failed_files = {}
    errors = []
    
    parsedData = [] # append all data onto each other creating one big df
    
    # for file in directory:
    total_files = len(directory)
    remaining_files = [f for f in directory if f not in status["success"]]
    total_remaining = len(remaining_files)
    
    # Create a single progress bar instance
    progress_bar = tqdm(remaining_files) #tqdm(total=len(remaining_files), desc="Processing files", position=0, leave=True)
    
    
    for file in remaining_files:
        progress_bar.set_description(f"Success: {len(successful_files)} | Failed: {len(failed_files)}")
        try:
            with open(os.path.join(PATH,"DROP_TXT_HERE", file), encoding='utf-8') as fp:
                messageBuffer = []
                dateTime, author = None, None
                conversation = file[:-4]
                line = fp.readline()
                pattern = detectPattern(line) 
                while True:
                    if startsWithDatetime(line,pattern): ### COME BACK AND CHECK CASE FOR NO AUTHOR -> throw out message
                        if len(messageBuffer) > 0:
                            parsedData.append([dateTime, author, ' '.join(messageBuffer), conversation])#### COME BACK TO THIS
                        messageBuffer.clear()
                        dateTime, author = re.split(pattern, line)[1:]
                        if startsWithAuthor(author):
                            author, message = author.split(':', maxsplit=1)
                            messageBuffer.append(message)
                    else:
                        messageBuffer.append(line)
                    
                    line = fp.readline() # Read next line 
                    if not line:
                        break
                    line = line.strip() # Strip leading/trailing whitespaces
        
                    
                if len(messageBuffer) > 0:
                    parsedData.append([dateTime, author, ' '.join(messageBuffer), conversation])
                    
            successful_files.append(file)
    
            
        except Exception as e:
            failed_files[file] = str(e)
            errors.append(str(e))
            
        progress_bar.update(1)   
        progress_bar.set_description(f"Processing files | Success: {len(successful_files)} | Failed: {len(failed_files)}")
        # time.sleep(.5)
    
    df = pd.DataFrame(parsedData, columns = ['Datetime', 'Author', 'Message', 'Conversation'])
    df.Datetime = df.Datetime.apply(lambda x : x.replace('[','').replace(']',''))

    df, drops = detect_datetime_formats(df)
    for c in drops:
        failed_files[c] = "The timestamps in this file were not read correctly, and is therefore being discarded. Make sure the file is already sorted chronologically, and that the regex is correct."
        successful_files.remove(c+'.txt')

    # Update status log
    status["success"].extend(successful_files)
    status["failed"].update(failed_files)
    status["success"] = list(set(status["success"]))  # Remove duplicates
    # status["failed"] = list(set(status["failed"]))
    save_status_log(status, PATH)
    
    # Store data in memory
    # df.drop(columns=['Message'], inplace=True) # test the memory usage of the keeping the chat messages
    # DROPPING THE MESSAGES COLUMN SAVES ~40% OF THE MEMORY COST
    
    hd5_file_path = os.path.join(PATH.replace("data","vis"),"data.h5")
    df.to_hdf(hd5_file_path, "df")

    # df = lang_detect(df)
    # hd5_file_path = os.path.join(PATH.replace("data","vis"),"demo.h5")
    # df.to_hdf(hd5_file_path, "df")

