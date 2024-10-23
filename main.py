import os, random, time
import pandas as pd
from collections import defaultdict

# FIFO
def fifo(page_references, num_frames):
    frames = []
    page_faults = 0
    interrupts = 0
    disk_writes = 0
    dirty_bits = {}

    for page in page_references:
        if page not in frames:
            page_faults += 1
            if len(frames) < num_frames:
                frames.append(page)
            else:
                page_to_remove = frames.pop(0)
                if dirty_bits.get(page_to_remove, False):
                    disk_writes += 1
                    interrupts += 1
                frames.append(page)
        dirty_bits[page] = random.choice([True, False])

    return page_faults, interrupts, disk_writes

# Optimal
def optimal(page_references, num_frames):
    frames = []
    page_faults = 0
    interrupts = 0
    disk_writes = 0
    dirty_bits = {}
    
    # 預處理：構建每個頁面的未來使用位置列表
    future_uses = defaultdict(list)
    for i, page in enumerate(page_references):
        future_uses[page].append(i)

    for i, page in enumerate(page_references):
        # 移除當前位置
        if future_uses[page]:
            future_uses[page].pop(0)
        
        if page not in frames:
            # 頁面錯誤發生
            page_faults += 1
            if len(frames) < num_frames:
                frames.append(page)
            else:
                # Optimal 替換邏輯
                # 尋找未來最遠使用的頁面
                furthest_use = -1
                page_to_remove = None
                for frame_page in frames:
                    if future_uses[frame_page]:
                        next_use = future_uses[frame_page][0]
                    else:
                        next_use = float('inf')  # 該頁面不再被使用
                    if next_use > furthest_use:
                        furthest_use = next_use
                        page_to_remove = frame_page
                
                frames.remove(page_to_remove)
                if dirty_bits.get(page_to_remove, False):
                    disk_writes += 1
                    interrupts += 1

                frames.append(page)

        # 隨機設置當前頁面的髒位
        dirty_bits[page] = random.choice([True, False])

    return page_faults, interrupts, disk_writes

# ESC
def enhanced_second_chance(page_references, num_frames):
    frames = []
    page_faults = 0
    interrupts = 0
    disk_writes = 0
    reference_bits = {}  # 引用位
    dirty_bits = {}  # 髒位
    pointer = 0  # 指向目前要檢查的頁面

    for page in page_references:
        if page not in frames:
            page_faults += 1
            if len(frames) < num_frames:
                frames.append(page)
                reference_bits[page] = 1  # 新載入頁面引用位設為 1
            else:
                # 增強型二次機會替換邏輯
                while True:
                    page_to_check = frames[pointer]
                    if reference_bits[page_to_check] == 0:
                        # 引用位為 0，可替換
                        if dirty_bits.get(page_to_check, False):
                            disk_writes += 1
                            interrupts += 1
                        frames[pointer] = page
                        reference_bits[page] = 1  # 新頁面引用位設為 1
                        break
                    else:
                        # 引用位為 1，重設引用位，並移動指針
                        reference_bits[page_to_check] = 0
                        pointer = (pointer + 1) % num_frames

        # 隨機設置髒位
        dirty_bits[page] = random.choice([True, False])

    return page_faults, interrupts, disk_writes

# My Algorithm
def myal(page_references, num_frames, weight_lru=2, weight_dirty=3):
    frames = []  # 用來存儲當前內存框架中的頁面
    page_faults = 0  # 頁面錯誤次數
    interrupts = 0  # 中斷次數
    disk_writes = 0  # 磁碟寫入次數
    dirty_bits = {}  # 用來追蹤每個頁面的髒位
    last_used = {}  # 用來追蹤每個頁面的最近使用時間

    for current_time, page in enumerate(page_references):
        # 如果頁面不在內存框架中
        if page not in frames:
            page_faults += 1
            
            
            if len(frames) < num_frames:
                frames.append(page)
            else:
                # 基於加權成本替換的邏輯進行頁面選擇
                def weighted_cost(p):
                    # 計算替換成本：髒位和最近使用時間的權重結合
                    lru_cost = weight_lru * (current_time - last_used.get(p, 0))
                    dirty_cost = weight_dirty if dirty_bits.get(p, False) else 0
                    return lru_cost + dirty_cost

                # 找到成本最高的頁面並替換
                page_to_replace = max(frames, key=weighted_cost)
                frames.remove(page_to_replace)
                
                # 如果被替換的頁面是髒頁，則增加磁碟寫入次數
                if dirty_bits.get(page_to_replace, False):
                    disk_writes += 1
                    interrupts += 1
                
                frames.append(page)
        
        # 更新該頁面的最近使用時間
        last_used[page] = current_time

        # 隨機設置髒位
        dirty_bits[page] = random.choice([True, False])

    return page_faults, interrupts, disk_writes

# Random
def generate_random_references(length, page_range):
    return [random.randint(1, page_range) for _ in range(length)]

# Locality
def generate_locality_references(total_references, page_range, locality_ratio_range=(1/200, 1/100)):
    references = []
    remaining_references = total_references
    
    while remaining_references > 0:
        # 隨機決定本次區域參考字串的長度
        locality_length = random.randint(int(total_references * locality_ratio_range[0]), 
                                         int(total_references * locality_ratio_range[1]))
        locality_length = min(locality_length, remaining_references)  # 防止超出剩餘長度

        # 隨機選擇一個區域（頁面號的範圍較小）
        start_page = random.randint(1, page_range - 100)  # 防止區域超出總頁面範圍
        end_page = start_page + random.randint(10, 50)  # 區域頁面範圍可設置為 10 到 50 個頁面

        # 在這個區域內生成區域性參考字串
        references += [random.randint(start_page, end_page) for _ in range(locality_length)]
        
        remaining_references -= locality_length  # 更新剩餘的參考字串長度
    
    return references

# Cyclic
def generate_cyclic_references(total_references, page_range, cycle_length=50):
    references = []
    
    # 生成週期性的參考字串
    for _ in range(total_references // cycle_length):
        start_page = random.randint(1, page_range - cycle_length)
        cycle = [random.randint(start_page, start_page + cycle_length - 1) for _ in range(cycle_length)]
        references += cycle
    
    # 如果還有剩餘的參考次數，補充剩下的頁面
    remaining = total_references % cycle_length
    if remaining > 0:
        start_page = random.randint(1, page_range - cycle_length)
        references += [random.randint(start_page, start_page + cycle_length - 1) for _ in range(remaining)]
    
    return references


algorithms = {
    'fifo': fifo,
    'opt': optimal,
    'exc': enhanced_second_chance,
    'myal': myal,
}

strings = {
    'ran': generate_random_references,
    'loc': generate_locality_references, 
    'cyc': generate_cyclic_references
}

# Paras
frame_sizes = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
num_references = 120000  
page_range = 1200 

for x in range(0,4):
    # Directory
    output_dir = f"{list(algorithms.keys())[x]}data"
    os.makedirs(output_dir, exist_ok=True)
    for y in range(0,3):
        page_faults_results = []
        interrupts_results = []
        disk_writes_results = []
        
        references = strings[list(strings.keys())[y]](num_references, page_range)

        for num_frames in frame_sizes:
            page_faults, interrupts, disk_writes = algorithms[list(algorithms.keys())[x]](references, num_frames)
            page_faults_results.append(page_faults)
            interrupts_results.append(interrupts)
            disk_writes_results.append(disk_writes)

        df = pd.DataFrame({
            "frame_sizes": frame_sizes,
            "page_faults": page_faults_results,
            "interrupts": interrupts_results,
            "disk_writes": disk_writes_results
        })

        # Save Data
        df.to_csv(f"{output_dir}/{list(algorithms.keys())[x]}{list(strings.keys())[y]}.csv", index=False)
        print(f"檔案已儲存至 {output_dir}/{list(algorithms.keys())[x]}{list(strings.keys())[y]}.csv")