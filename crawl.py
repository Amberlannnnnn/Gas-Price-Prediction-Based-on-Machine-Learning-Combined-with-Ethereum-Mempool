import urllib3
import json
import time

start_block_num = 14440608
total_crawl_num = 100000
num_per_file = 10000
file_num = 0
cnt = 0
fnt = 0 
tx = -1

http = urllib3.PoolManager()


headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'
}
proxy = urllib3.ProxyManager('http://127.0.0.1:7890', headers={'connection': 'keep-alive'})
result = list()
while cnt < total_crawl_num:
    # with open('data.json', 'w+', encoding='UTF8', newline='') as f:
    
    # row_headers = ['block number', 'gas limit', 'gas used', 'base fee per gas', 'transaction list length', 'transaction info']
    cur_block_num = start_block_num + cnt
    print("processing the block, number is: " + str(cur_block_num))
    try:
        res = proxy.request("GET", \
            "http://api-cn.etherscan.com/api?module=proxy&action=eth_getBlockByNumber&tag="+str(hex(cur_block_num))+"&boolean=true&apikey=HDW6GIS8EGCP8XKKKFQEEFV1JMSIGRCEZC")
        raw_data = res.data.decode("UTF-8")
        cresult = json.loads(raw_data)["result"]
    except:
        #print(raw_data)
        print("why")
        time.sleep(6)
        continue
    
    print("success")
    tran_list = cresult["transactions"]
    cur_item = dict()

    cur_item.update({
        'block_number': cur_block_num,
        'gas_limit': cresult.get("gasLimit", ""),
        'gas_used': cresult.get("gasUsed", ""),
        'base_fee_per_gas': cresult.get("baseFeePerGas", ""),
        'difficulty':cresult.get("difficulty",""),
        'timestamp':cresult.get("timestamp","")
    })
    #print(cresult)
    cur_item_trans_list = list()
    # 处理交易列表
    for item in tran_list:
        cur_item_trans_list.append({
            'gas_price': item.get("gasPrice", ""),
            'max_fee_per_gas': item.get("maxFeePerGas", ""), 
            'max_priority_fee_per_gas': item.get("maxPriorityFeePerGas", "")
        })
        tx += 1
    #print(tx)
    cur_item.update({
        'tx': tx,
        'transaction_info': cur_item_trans_list
    })
    result.append(cur_item)
    cnt += 1
    fnt += 1
    tx = 0
    # time.sleep(1)

    if fnt == num_per_file:
        file_num += 1
        with open(f'./data-{file_num}.json', 'w+') as f:
            f.write(json.dumps(result))
        fnt = 0
        result = list()
    
#if cnt == total_crawl_num:
#    file_num += 1
#    with open(f'./crawl/data-{file_num}.json', 'w+') as f:
#        f.write(json.dumps(result))