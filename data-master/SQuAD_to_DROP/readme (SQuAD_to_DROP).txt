用 SQuAD_to_DROP.py 將原始檔案 SQuAD 格式 轉成 DROP 格式


SQuAD 格式架構 (ver 1.3)
{'version', 'data'}
            'data':[{'title', 'id', 'paragraphs'}, {t,i,p}, ...]
                                    'paragraphs':[{'context', 'id', 'qas'}, {c,i,q}, ...]
                                                                    'qas':[{'id', 'question', 'answers'}, {i,q,a}, ....]                                                                 
                                                                                              'answers':[{'id','text','answer_start'}] 

DROP 格式架構
{'p_id', 'p_id', ...}
 'p_id':{'passage', 'qa_pairs'}
                    'qa_pairs': [{'question','answer','query_id'}, {q,a,q_i}, ...]
                                             'answer': {'number','unit','yesno','spans'}



輸出 .json 檔後，格式化整理內容以方便檢視：
https://jingyan.baidu.com/article/f3e34a12a140cbf5ea653553.html