# Streaming Naive Bayes and TFIDF

Using mapreduce method to implement the streaming Nive Bayes Method and TFIDF.

The codes are written for a linux pip 
(e.g. For file NBTrain/NBTest.py:)

      cat file_name.txt | python NBTrain.py | python NBTest.py > predict.txt
          


### predict.txt contains the result of prediction in the following format:

[True1, True2, True3] [tab] Predicted Label [tab] log probability

for example:<br>
['C11', 'C42', 'CCAT', 'E41', 'ECAT', 'GCAT', 'GJOB']	GCAT	-3966.812 <br>
['C21', 'CCAT']	CCAT	-1206.765 <br>
['M14', 'M141', 'M142', 'M143', 'MCAT']	MCAT	-5108.084 <br>

### top10.txt contains the result of the top 10 popular words in each class:

[Class] [tab] [Word] [tab] [Counts]

For example, for the class 'Activity':<br>
Activity	the	6748<br>
Activity	of	3096<br>
Activity	and	2972<br>

### final_TFIDF.txt contains the TFIDF result in the following format:

D =[doc_id] [tab] W = [word] [tab] [TFIDF]

For example:<br>
D=d2	W=American	0.001019<br>
D=d2	W=Americans	0.000277<br>
D=d2	W=Americas	0.00194<br>
