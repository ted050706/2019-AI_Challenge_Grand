## 讀取官方 json 檔
import json

# Reading data back
with open("FGC_release_B.json", "r", encoding="utf-8") as f:
    data_list = json.load(f)

# Reading data back
with open("FGC_release_B_answers.json", "r", encoding="utf-8") as f:
    data_answers_list = json.load(f)

# 只保留基礎題 Question
data_base = []
for i in range(len(data_list)):
	for data in data_list[i]['QUESTIONS']:
		#if data['QTYPE'] == '基礎題':
		data_base.extend([data])
	data_list[i]['QUESTIONS'] = data_base
	data_base = []

# 只保留基礎題 Answer
data_ans_base = []
for i in range(len(data_answers_list)):
	#if data_answers_list[i]['QTYPE'] == '基礎題':
	data_ans_base.extend([data_answers_list[i]])

d_list = data_list
d_ans_list = data_ans_base

# 轉換為Drop
Data = {}
J = 0
count = 1
#Answer_Start = 0
for i in range(len(d_list)):
	Passage = ""	# Drop之 'passage'
	Qa_pairs = []	# Drop之 'qa_pairs'

	if len(d_list[i]['QUESTIONS'])!=0:	# 判斷是否含有Question
		ans_count = 1
		for j in range(len(d_list[i]['QUESTIONS'])):	# 計算 d_list 每橫排的 "QUESTIONS" 數量
			if '是否' in d_list[i]["QUESTIONS"][j]['QTEXT']:	#只取 '是非題'
				# 建立Drop之 'answers': [{'number', 'unit'}, ...]
				Answer = {}
				if d_ans_list[J+j]['ANSWER']!='':	#	判斷Answer是不是空字串
					if d_ans_list[J+j]['ANSWER'] == '是':	# 如果為"是"，則1
						ans = "1"	
					else:	# 如果為"否"，則0
						ans = "0"	 
				else:		# answer沒有時(如:申論題)
					ans = ""	# ans為空
				Answer = {'number':"",'unit':"",'yesno':ans,'spans':[]}

				#if Answer_Start!=0: 	B_sample問題...
				# 建立Drop之 'qa_pairs': [{'question', 'answer', 'query_id'}, ...]
				Question = d_list[i]["QUESTIONS"][j]['QTEXT']	# Drop之 'question'
				ID = str(count).zfill(6)+'-'+str(ans_count)	# Drop之 'id'
				QA = { 'question':Question,'answer':Answer,'query_id':ID }
				Qa_pairs.extend([QA])
				ans_count = ans_count+1
		J=J+(j+1)	# 累加index

		if len(Qa_pairs)!=0:	#	判斷有無問答與題目
			# 建立SQuAD之 'paragraphs': [{'context','qas'}, ...]
			context = d_list[i]['DTEXT']
			title = 'nfl_'+str(count).zfill(4)
			Data[title] = {'passage':context,'qa_pairs':Qa_pairs}
			count+=1

data = { 'data':Data }
#print('data:',data)

ret = json.dumps(data,ensure_ascii=False)

# 將SQuAD寫入檔案
with open('sample_SQuAD_v3.json', 'w',encoding='utf-8') as outfile:
    outfile.write(ret)
    print('write finish')