from collections import Counter
import os
import pandas as pd
import matplotlib.pyplot as plt

def count_words(text):
	words_count = {}
	skips = [",",";",":",".","'",'"']
	text = text.lower()
	for ch in skips:
		text = text.replace(ch,"")
	for word in text.split(" "):
		if word in words_count:
			words_count[word] +=1
		else:
			words_count[word]=1
	return(words_count)
	
def count_words_fast(text):
	"""
		This method makes use of Counter function to count the word frequency in given text
	"""
	skips = [",",";",":",".","'",'"']
	text = text.lower()
	for ch in skips:
		text = text.replace(ch,"")
	words_count = Counter(text.split(" "))
	return(words_count)
	
def read_book(title):
	"""
		This method gets the title of a book and returns the content as string
	"""
	with open(title,'r',encoding='utf8') as current_file:
		text = current_file.read()
		text = text.replace("\n","").replace("\r","")
	return(text)
	
def word_stats(count):
	unique_words_count = len(count)
	counts = count.values()
	return(unique_words_count, counts)
	

#E:\_____Laptop-PC\work\python-case-study\Books\English\shakespeare
def loop_files():
	book_dir = ".\Books"
	stats = pd.DataFrame(columns=("language","author","title","unique_words","word_count"))
	title_num = 1
	
	for language in os.listdir(book_dir):
		for author in os.listdir(book_dir+"\\"+language):
			for title in os.listdir(book_dir+"\\"+language+"\\"+author):
				
				inputfile = book_dir+"\\"+language+"\\"+author+"\\"+title
				#print(inputfile)
				content = read_book(inputfile)
				(words, count) = word_stats(count_words_fast(content))
				stats.loc[title_num] = language,author.capitalize(),title.replace(".txt",""),words, sum(count)
				title_num += 1
	return(stats)
				
def plot_stats(stats):
	plt.figure(figsize=(10,10))
	subset = stats[stats.language == "English"]
	plt.loglog(subset.unique_words, subset.word_count,"o", label = "English",color="blueviolet")
	
	subset = stats[stats.language == "French"]
	plt.loglog(subset.unique_words, subset.word_count,"o", label = "French",color="crimson")
	
	subset = stats[stats.language == "German"]
	plt.loglog(subset.unique_words, subset.word_count,"o", label = "German",color="forestgreen")
	
	subset = stats[stats.language == "Portuguese"]
	plt.loglog(subset.unique_words, subset.word_count,"o", label = "Portuguese",color="orange")
	plt.legend()
	plt.xlabel("word count")
	plt.ylabel("unique words")
	#plt.show()
	plt.savefig("lang_words_stat.pdf")
				
table = loop_files()
plot_stats(table)

counted_text = count_words_fast(text)

data = pd.DataFrame({
    "word": list(counted_text.keys()),
    "count": list(counted_text.values())
})
data['length']= data.apply(lambda row: len(row.word), axis=1)
#data["length"] = data["word"].apply(len) --simplest way
data['frequency']=''
data['frequency'][data['count'] > 10] = 'frequent'
data['frequency'][data['count'] <= 10] = 'infrequent'
data['frequency'][data['count'] == 1] = 'unique'


