import pandas as pd
import spacy
import re
import streamlit as st
from difflib import get_close_matches

# Load the dataset
df = pd.read_excel('collegeRajasthanData.xlsx')
df.fillna('N/A', inplace=True)

# Split the 'Location' column into 'City', 'State', and 'Country'
location_split = df['Location'].str.split(',', n=2, expand=True)
df['City'] = location_split[0].str.strip()
df['State'] = location_split[1].str.strip()
df['Country'] = location_split[2].str.strip()

# Load the spaCy model
nlp = spacy.load('en_core_web_sm')

# Function definitions (extract_locations, extract_college_name, etc.) remain the same

def extract_locations(query, known_cities, known_states):
    doc = nlp(query)
    detected_locations = [ent.text.lower() for ent in doc.ents if ent.label_ in ["GPE", "LOC"]]
    fallback_locations = [word.lower() for word in query.split() if word.lower() in known_cities or word.lower() in known_states]
    return list(set(detected_locations + fallback_locations))

def extract_college_name(query):
    doc = nlp(query)
    college_names = [ent.text.lower() for ent in doc.ents if ent.label_ == "ORG"]
    possible_colleges = df['College name'].str.lower()
    for name in college_names:
        if any(college in name for college in possible_colleges):
            return name
    return None

def extract_college_names(query):
    doc = nlp(query)
    college_names = [ent.text.lower() for ent in doc.ents if ent.label_ == "ORG"]
    possible_colleges = df['College name'].str.lower().tolist()
    
    extracted_colleges = []
    for name in college_names:
        close_matches = get_close_matches(name, possible_colleges, n=1, cutoff=0.7)
        if close_matches:
            extracted_colleges.append(close_matches[0])
    return extracted_colleges

def compare_colleges(college1, college2):
    college1_data = df[df['College name'].str.lower() == college1].iloc[0]
    college2_data = df[df['College name'].str.lower() == college2].iloc[0]

    comparison_result = f"Comparison between {college1_data['College name']} and {college2_data['College name']}:\n\n"
    comparison_result += f"Course Fee: {college1_data['Course fee']} vs {college2_data['Course fee']}\n"
    comparison_result += f"Hostel Fee: {college1_data['Hostelfee']} vs {college2_data['Hostelfee']}\n"
    comparison_result += f"Courses Offered: {college1_data['Coursed offred']} vs {college2_data['Coursed offred']}\n"
    comparison_result += f"Placement: {college1_data['Placement']} vs {college2_data['Placement']}\n"
    comparison_result += f"Admission Criteria: {college1_data['Admition criteria']} vs {college2_data['Admition criteria']}\n"

    return comparison_result

def extract_course_name(query):
    courses = df['Coursed offred'].str.lower().unique()
    for course in courses:
        if course in query.lower():
            return course
    return None

def extract_numeric_fee(fee_string):
    numbers = re.findall(r'\d+', fee_string.replace(',', ''))
    if numbers:
        return int(numbers[0])
    return None

def extract_fee_range(query):
    match = re.search(r'(\d+)\s*to\s*(\d+)', query)
    if match:
        return int(match.group(1)), int(match.group(2))
    return None, None

def determine_info_type(query):
    query = query.lower()
    if 'admission criteria' in query or 'admission' in query:
        return 'admission'
    elif 'duration' in query or 'course duration' in query:
        return 'duration'
    elif 'entrance exam' in query or 'exam' in query:
        return 'exam'
    elif 'fee' in query and 'range' in query:
        return 'fee_range'
    else:
        return 'general'

def chatbot(query):
    known_cities = df['City'].str.lower().unique()
    known_states = df['State'].str.lower().unique()
    
    college_names = extract_college_names(query)
    course_name = extract_course_name(query)
    min_fee, max_fee = extract_fee_range(query)
    info_type = determine_info_type(query)
    
    result = ""

    if len(college_names) == 2:
        result = compare_colleges(college_names[0], college_names[1])
    
    elif course_name and info_type == 'duration':
        course_info = df[df['Coursed offred'].str.lower().str.contains(course_name)]
        if not course_info.empty:
            for index, row in course_info.iterrows():
                result += f"The duration of {course_name.capitalize()} at {row['College name']} is {row['Coursed duretion']}.\n"
        else:
            result = f"No details found for the course {course_name.capitalize()}."

    elif len(college_names) == 1:
        college_name = college_names[0]
        college_data = df[df['College name'].str.lower() == college_name].iloc[0]

        if info_type == 'admission':
            result = f"Admission Criteria for {college_data['College name']}:\n"
            result += f"Admission Criteria: {college_data['Admition criteria']}\n"
            result += f"Entrance Exam: {college_data['Entrance Exam']}\n"
        elif info_type == 'duration':
            result = f"Course Duration for {college_data['College name']}:\n"
            result += f"Course Duration: {college_data['Coursed duretion']}\n"
        elif info_type == 'exam':
            result = f"Entrance Exams for {college_data['College name']}:\n"
            result += f"Entrance Exam: {college_data['Entrance Exam']}\n"
        else:
            result = f"Details for {college_data['College name']}:\n"
            result += f"College Name: {college_data['College name']}\n"
            result += f"Established: {college_data['Established']}\n"
            result += f"Affiliation: {college_data['Affliation']}\n"
            result += f"Location: {college_data['Location']}\n"
            result += f"Courses Offered: {college_data['Coursed offred']}\n"
            result += f"Course Duration: {college_data['Coursed duretion']}\n"
            result += f"Admission Criteria: {college_data['Admition criteria']}\n"
            result += f"Entrance Exam: {college_data['Entrance Exam']}\n"
            result += f"Hostel Availability: {college_data['Hostel avilibiliry']}\n"
            result += f"Course fee: {college_data['Course fee']}\n"
            result += f"Hostel Fee: {college_data['Hostelfee']}\n"
            result += f"Placement: {college_data['Placement']}\n"
            result += f"Facilities: {college_data['Facilities']}\n"
            result += f"What college provide to society: {college_data['What college provide to society']}\n"
            result += f"Contact Information: {college_data['Contact information']}\n"
            result += f"Website: {college_data['Website']}\n"

    elif info_type == 'fee_range':
        fee_range_colleges = df[(df['Course fee'] != 'N/A')]
        fee_range_colleges = fee_range_colleges[
            fee_range_colleges['Course fee'].apply(
                lambda x: min_fee <= extract_numeric_fee(x) <= max_fee if extract_numeric_fee(x) is not None else False
            )
        ]
        
        if not fee_range_colleges.empty:
            result = f"Colleges with course fee between {min_fee} and {max_fee}:\n"
            for index, row in fee_range_colleges.iterrows():
                result += f"College Name: {row['College name']}\n"
                result += f"Location: {row['Location']}\n"
                result += f"Courses Offered: {row['Coursed offred']}\n"
                result += f"Course fee: {row['Course fee']}\n"
                result += "\n"
        else:
            result = f"No colleges found within the fee range of {min_fee} to {max_fee}."

    elif course_name:
        course_colleges = df[df['Coursed offred'].str.lower().str.contains(course_name)]
        if not course_colleges.empty:
            result = f"Colleges offering {course_name.capitalize()}:\n"
            for index, row in course_colleges.iterrows():
                result += f"College Name: {row['College name']}\n"
                result += f"Location: {row['Location']}\n"
                result += f"Course Duration: {row['Coursed duretion']}\n"
                result += f"Course Fee: {row['Course fee']}\n"
                result += "\n"
        else:
            result = f"No colleges found offering the course {course_name.capitalize()}."

    else:
        result = "Sorry, I couldn't understand the query. Could you please rephrase it?"

    return result

# Streamlit app
st.title("College Information Chatbot")

user_query = st.text_input("Ask about college information:")

if user_query:
    result = chatbot(user_query)
    st.write(result)