import pandas as pd

# 定義三個資料庫和三個參數
datas = ['ran', 'loc', 'cyc']
results = ['page_faults', 'interrupts', 'disk_writes']

# 用來存放比較結果的數據
comparison_data = []

# 開始進行比較
for x in datas:
    # 讀取 FIFO 和 LRU 的 CSV 文件
    df_fifo = pd.read_csv(f'fifodata/fifo{x}.csv')
    df_myal = pd.read_csv(f'myaldata/myal{x}.csv')
    
    # 計算 FIFO 和 LRU 的總成本（interrupts + disk_writes）
    df_fifo['cost'] = df_fifo['interrupts'] + df_fifo['disk_writes']
    df_myal['cost'] = df_myal['interrupts'] + df_myal['disk_writes']
    
    # 建立一個空的字典來存放比較結果
    comparison_dict = {
        'frame_sizes': df_fifo['frame_sizes'],  # 框架大小
        f'{x}_page_fault': [],  # 頁面錯誤比較
        f'{x}_cost': []  # 成本比較
    }
    
    # 比較 FIFO 和 LRU 的結果
    for i in range(len(df_fifo)):
        # 比較頁面錯誤：如果 LRU 比 FIFO 好（少），設為 1，否則 0
        if df_myal['page_faults'][i] < df_fifo['page_faults'][i]:
            comparison_dict[f'{x}_page_fault'].append(1)
        else:
            comparison_dict[f'{x}_page_fault'].append(0)
        
        # 比較總成本：如果 LRU 的成本比 FIFO 低，設為 1，否則 0
        if df_myal['cost'][i] < df_fifo['cost'][i]:
            comparison_dict[f'{x}_cost'].append(1)
        else:
            comparison_dict[f'{x}_cost'].append(0)
    
    # 把結果加入到比較數據列表中
    comparison_data.append(pd.DataFrame(comparison_dict))

# 合併三個資料庫的比較結果
final_df = pd.concat(comparison_data, axis=1)

# 確保只保留一次 frame_sizes（避免重複）
final_df = final_df.loc[:,~final_df.columns.duplicated()]
total_ones = (final_df == 1).sum().sum()
total_zeros = (final_df == 0).sum().sum()
# 查看最終結果
print(final_df)

# 儲存最終比較結果
final_df.to_csv(f'my{total_ones}:fifo{total_zeros}.csv', index=False)