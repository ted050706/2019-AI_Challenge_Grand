### 讀JSON檔
import json

FilePath = 'QDSQA_textq.json'    # 可能需要完整檔案路徑
with open(FilePath, "r", encoding="utf-8") as f:
    J_data = json.load(f)


### 取值比對
K = J_data.keys()    # 取得 dict 的 key
LK = list(K)    # 將 dict_keys 資料類型轉存成 list

J_D = J_data    ## 令 dict 資料備份
for N in range(len(J_data)):
    P_ID = LK[N]    # 取出key (文本編號)
    QA_PAIRS = J_data[P_ID]['qa_pairs']    # 根據key取出項目 "qa_pairs"
    
    QA_P = []    # 令新的 QA_PAIRS
    for M in range(len(QA_PAIRS)):
        QUERY_ID = QA_PAIRS[M]['query_id']    # 依序取出項目 "query_id"
        
        if QUERY_ID[0:-2] == P_ID:    # 若 QUERY_ID 去掉末兩碼後與 P_ID 相同，代表位置正確
            QA_P.append(QA_PAIRS[M])    ## 累計正確的 QA_PAIRS
    
    J_D[P_ID]['qa_pairs'] = QA_P    # 對應的 "qa_pairs" 以正確的 QA_PAIRS 取代


### 存檔
import json

jsdumps = json.dumps(J_D, ensure_ascii=False)
filePath = 'fixed_QDSQA_textq.json'    # 可能需要完整檔案路徑
outfile = open(filePath, 'w', encoding='utf-8')
outfile.write(jsdumps)
outfile.close()