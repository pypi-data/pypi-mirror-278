import time
#from anoteai import Anote
from core import Anote


if __name__ == "__main__":
    api_key = '7b26299c19fc4d367c413ea9782f28d8'

# 1. Upload all documents from Anote Documentation and Dataroom to DB
# 2. Ask Model Via Chat Call to Generate 10 Quiz Questions about Anote
# 3. Ask Model to Generate 10 Answers to These Quiz Questions
# 4. Assign Each Person on the Team to Answer Each of the 10 Quiz Question By Hand
# 5. Take Human Answers and Model Answers, Format it as a list of Dict to put into Eval
# 6. Evaluate the Answers of Each Human to Give them a score on how much they know about Anote
