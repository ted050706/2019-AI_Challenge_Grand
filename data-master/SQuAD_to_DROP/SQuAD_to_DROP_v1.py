## SQuAD 格式架構 (ver 1.3)
# {'version', 'data'}
#             'data':[{'title', 'id', 'paragraphs'}, {t,i,p}, ...]
#                                     'paragraphs':[{'context', 'id', 'qas'}, {c,i,q}, ...]
#                                                                     'qas':[{'id', 'question', 'answers'}, {i,q,a}, ....]                                                                 
#                                                                                               'answers':[{'id','text','answer_start'}] 

## DROP 格式架構
# {'p_id', 'p_id', ...}
#  'p_id':{'passage', 'qa_pairs'}
#                     'qa_pairs': [{'question','answer','query_id'}, {q,a,q_i}, ...]
#                                              'answer': {'number','unit','yesno','spans'}


### 讀取 JSON 檔
import json

FilePath = 'DRCD_dev.json'    # 可能需要完整檔案路徑
with open(FilePath, "r", encoding="utf-8") as f:
    Data = json.load(f)


DR_P_ID_list = []    ### 令一個列表暫存 DROP 格式之 'p_id'，方便之後合成 dict 
DR_PQ_list = []    ### 令一個列表暫存 DROP 格式之 {'passage', 'qa_pairs'}，方便之後合成 dict

SQ_DATA = Data['data']    # 取出 SQuAD 格式之 'data'
for a in range( len(SQ_DATA) ):
    
    SQ_PARAGRAPHS = SQ_DATA[a]['paragraphs']    # 取出 SQuAD 格式之 'paragraphs'
    for b in range( len(SQ_PARAGRAPHS) ):

        ### 取出 SQuAD 格式 'paragraphs' 之 'id'；轉存為 DROP 格式之 'p_id'
        SQ_P_ID = SQ_PARAGRAPHS[b]['id']
        DR_P_ID_list.extend([SQ_P_ID])
        
        # 取出 SQuAD 格式之 'context'；轉存為 DROP 格式之 'passage'
        SQ_CONTEXT = SQ_PARAGRAPHS[b]['context']    
        DR_PASSAGE = SQ_CONTEXT    
        
        DR_QA_PAIRS = []    ## 令 DROP 格式之 'qa_pairs'
        SQ_QAS = SQ_PARAGRAPHS[b]['qas']    # 取出 SQuAD 格式之 'qas'
        for c in range( len(SQ_QAS) ):

            # 取出 SQuAD 格式之 'question'；轉存為 DROP 格式之 'question'
            SQ_QUESTION = SQ_QAS[c]['question']
            DR_QUESTION = SQ_QUESTION


            ## 組成 DROP 格式之 'answer': {'number','unit','yesno','spans'}
            DR_NUMBER = ''
            DR_UNIT = ''
            DR_YESNO = ''
            DR_SPANS = []

            # 取出 SQuAD 格式之 'text'；轉存為 DROP 格式之 'spans'
            SQ_ANSWERS = SQ_QAS[c]['answers'] 
            SQ_TEXT = SQ_ANSWERS[0]['text']    
            DR_SPANS.append(SQ_TEXT)    
            
            DR_ANSWER = {'number':DR_NUMBER, 'unit':DR_UNIT, 'yesno':DR_YESNO, 'spans':DR_SPANS}

            # 取出 SQuAD 格式 'QAS' 之 'id'；轉存為 DROP 格式之 'query_id'
            SQ_Q_ID = SQ_QAS[c]['id']
            DR_QUERY_ID = SQ_Q_ID


            ## 組成 DROP 格式之 'qa_pairs': [{'question','answer','query_id'}, {q,a,q_i}, ...]
            DR_QA_PAIRS.extend([{ 'question':DR_QUESTION, 'answer':DR_ANSWER ,'query_id':DR_QUERY_ID }])

        ### 組成 DROP 格式之 {'passage', 'qa_pairs'}
        DR_PQ_list.extend([{ 'passage':DR_PASSAGE, 'qa_pairs':DR_QA_PAIRS }])

###　合成 DROP 格式之 ｛'p_id':{'passage', 'qa_pairs'}, 'p_id', ...}
DR_Data = dict( dict(zip( DR_P_ID_list, DR_PQ_list )) )


### 存成 JSON 檔
import json

jsdumps = json.dumps(DR_Data, ensure_ascii=False)
outfile = open('SQuAD_to_DROP_v1.json', 'w', encoding='utf-8')
outfile.write(jsdumps)
outfile.close()