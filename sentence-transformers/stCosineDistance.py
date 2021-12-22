import itertools
import torch
from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('all-MiniLM-L6-v2')
    
def getSentences(file_path):
	text_content = open(file_path , "r")
	text_string = text_content.read().replace("\n", " ")
	text_content.close()

	characters_to_remove = [",",";","'s", "@", "&","*", 
    "(",")","#","!","%","=","+","-","_",":", '"',"'"]

	for item in characters_to_remove:
		text_string = text_string.replace(item,"")
	characters_to_replace = ["?"]

	for item in characters_to_replace:
		text_string = text_string.replace(item,".")
	sentences = text_string.split(".")
	j = 0

	for sentence in sentences:
		if len(sentence) < 1:
			continue

		elif sentence[0] == " ":
			sentence = sentence[1:]
			sentences[j] = sentence
			j += 1

		else:
			sentences[j] = sentence
			j += 1
	sentences = sentences[0:j]
	return(sentences)

def getAvgCosine(filepath):
# sentences to encode
	sentences = [getSentences(filepath)]
    
# Two lists of sentences
	sentences1 = sentences[0][0:-1]
	sentences2 = sentences[0][1:]

	#Compute embedding for both lists
	embeddings1 = model.encode(sentences1, convert_to_tensor=True)
	embeddings2 = model.encode(sentences2, convert_to_tensor=True)

	#Compute cosine-similarits and average them into one cosine_score
	cosine_score = torch.mean(util.pytorch_cos_sim(embeddings1, embeddings2)).item()

	# output average cosine score
	return cosine_score

# print(getAvgCosine(r"C:\Users\14242\OneDrive\desktop\p-interact workspace\outputs\story_output1637381427.383707.txt"))
