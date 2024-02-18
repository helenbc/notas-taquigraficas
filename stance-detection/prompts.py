def get_system():
    system = """Consider that it is an expert model in Stance Detection. Stance detection is the task of predicting an author's point of view on a subject of interest. A speech can represent one of three types of stance, for, against or neutral.
For: When an author takes a stance "for" a subject, it means they support or advocate for it. Their speech or writing will likely include arguments, evidence, or opinions that highlight the positive aspects, benefits, or reasons to endorse the subject. For example, if the subject is a proposed policy change, someone taking a "for" stance might emphasize how it could improve people's lives or address important societal issues.
Against: This stance indicates opposition or disagreement with the subject at hand. Authors taking an "against" stance will present arguments, evidence, or opinions that highlight flaws, risks, negative consequences, or reasons to reject the subject. Using the previous example of a proposed policy change, someone taking an "against" stance might argue that it would be ineffective, unfair, or harmful to certain groups.
Neutral: A neutral stance means the author does not express explicit support or opposition towards the subject. They may present information, analysis, or perspectives in a balanced and objective manner without advocating for or against the subject. Neutral stances typically avoid strong opinions or judgments and instead focus on providing a comprehensive understanding of the topic without bias.
"""
    return system


def classification_prompt(text_meeting: str):
    prompt = f"""Consider that you will receive as input a csv with a set of speeches that make up what is recorded in a plenary session or in a committee meeting of the Brazilian Senate. The csv is made up of the following columns: 
"id_session","parliamentarian_name","party" and "speech".
id_session: This is the unique identifier for that session.
parliamentarian_name: This is the name of the parliamentarian who gave that speech.
party: This is the political party to which the parliamentarian belongs.
speech: This is the transcript of the speech given by that parliamentarian.

Return five topics that are being discussed in the \
following CSV, which is delimited by triple backticks.
Make each topic one or two words long.


Csv of the meeting: '''{text_meeting}'''
"""
    return prompt


def classification_prompt_sample(text_meeting: str):
    prompt = f"""Consider that you will receive as input a csv with a set of speeches that make up what is recorded in a plenary session or in a committee meeting of the Brazilian Senate. The csv is made up of the following columns: 
"id_session","parliamentarian_name","party" and "speech".
id_session: This is the unique identifier for that session.
parliamentarian_name: This is the name of the parliamentarian who gave that speech.
party: This is the political party to which the parliamentarian belongs.
speech: This is the transcript of the speech given by that parliamentarian.

Identify the following items in the text of the meeting:
- Determine five topics that are being discussed in the \
following text, which is delimited by triple backticks.
- For each parliamentarian, classify the statement as being FOR, AGAINST, NEUTRAL or NOT RELATED.

The review is delimited with triple backticks. \
Format your response as a JSON object with \
"id_session", "topic", "parliamentarian_name" and "stance" as the keys.
If the information isn't present, use "unknown" \
as the value.

Text of the meeting: '''{text_meeting}'''
"""
    return prompt
