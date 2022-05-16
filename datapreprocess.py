from asyncio.windows_events import NULL
import pandas as pd
import json
import csv

# 使用 Python JSON 模块载入数据
with open('E:/blockdata/data-5.json', 'r') as f:
    data = json.loads(f.read())
#csv_file = open("D:/Documents/test1.csv", "w")   #转换后的文件名和文件类型
# 展平数据
df_nested_list = pd.json_normalize(
    data,
    record_path =['transaction_info'],
    meta=['block_number','gas_limit','gas_used','base_fee_per_gas',"difficulty","timestamp","tx"]
)
#df_nested_list.to_csv('D:/Documents/blockdata/test1.csv', index=False)
#means = df_nested_list.groupby('block_number').mean()
df_nested_list['gas_price'] = df_nested_list['gas_price'].apply(lambda x: int(x, 16))
df_nested_list['max_fee_per_gas'] = df_nested_list['max_fee_per_gas'].replace('','0')
df_nested_list['max_fee_per_gas'] = df_nested_list['max_fee_per_gas'].apply(lambda x: int(x, 16)) 
df_nested_list['max_priority_fee_per_gas'] = df_nested_list['max_priority_fee_per_gas'].replace('','0')
df_nested_list['max_priority_fee_per_gas'] = df_nested_list['max_priority_fee_per_gas'].apply(lambda x: int(x, 16))
df_nested_list['gas_limit'] = df_nested_list['gas_limit'].apply(lambda x: int(x, 16))
df_nested_list['gas_used'] = df_nested_list['gas_used'].apply(lambda x: int(x, 16))
df_nested_list['difficulty'] = df_nested_list['difficulty'].apply(lambda x: int(x, 16))
df_nested_list['timestamp'] = df_nested_list['timestamp'].apply(lambda x: int(x, 16))
df_nested_list['base_fee_per_gas'] = df_nested_list['base_fee_per_gas'].replace('','0')
df_nested_list['base_fee_per_gas'] = df_nested_list['base_fee_per_gas'].apply(lambda x: int(x, 16))

df_nested_list['avg_mf'] = df_nested_list.groupby('block_number')['max_fee_per_gas'].transform('mean')
df_nested_list['avg_mp'] = df_nested_list.groupby('block_number')['max_priority_fee_per_gas'].transform('mean')
df_nested_list['avg_gp'] = df_nested_list.groupby('block_number')['gas_price'].transform('mean')
df_nested_list['middlle_gp'] = df_nested_list.groupby('block_number')['gas_price'].transform('median')
df_nested_list=df_nested_list.drop(['gas_price','max_fee_per_gas','max_priority_fee_per_gas'],axis=1)
df_nested_list.duplicated()
df_nested_list = df_nested_list.drop_duplicates()
df_nested_list['avg_mf'] = df_nested_list['avg_mf'].div(1000000000)
#csv_df['gas_limit'] = csv_df['gas_limit'].div(1000000000)
#csv_df['gas_used'] = csv_df['gas_used'].div(1000000000)
df_nested_list['base_fee_per_gas'] = df_nested_list['base_fee_per_gas'].div(1000000000)
df_nested_list['avg_mp'] = df_nested_list['avg_mp'].div(1000000000)
df_nested_list['avg_gp'] = df_nested_list['avg_gp'].div(1000000000)
df_nested_list['middlle_gp'] = df_nested_list['middlle_gp'].div(1000000000)
print(df_nested_list)
df_nested_list.to_csv('D:/Documents/blockdata/7583457.csv', index=False)