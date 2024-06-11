def score_pathways(p1, client, data):
    import pandas as pd
    from io import StringIO
    import re
    # 初始化一个空的DataFrame，用于存储所有通路的结果
    all_scores = pd.DataFrame(columns=['Pathway', 'Gene', 'Score'])

    # 循环遍历通路
    for i in range(len(data)):
        p2 = data.iloc[i, 0]  # 获取第i个通路
        p3 = data.iloc[i, 2:1542].dropna().tolist()  # 获取第i个通路的基因列表

        # 设置问题
        prompt = f"""请对通路{p2}中基因重要性进行打分，从0到10进行打分，0分是最不重要的，10分是最重要的：以下基因是{', '.join(p3)}。返回的结果只有第一列为hsa号，第二列为基因名，第三列为评分，每行一个条目，用制表符分隔。"""

        # 获取对话模型的响应
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="gpt-4o",  # 使用的模型是"gpt-4o"
        )
        text = chat_completion.choices[0].message.content

        # 解析响应并构建DataFrame
        lines = text.strip().split('\n')
        rows = []
        for line in lines:
            if line.strip():
                parts = line.split()
                if len(parts) >= 4:
                    row_data = parts[0], parts[2], parts[3]
                    rows.append(row_data)
                elif len(parts) == 3:
                    rows.append(parts)

        # 将行转换为DataFrame
        df = pd.DataFrame(rows, columns=['Pathway', 'Gene', 'Score'])

        # 更新Pathway列
        df['Pathway'] = p2

        # 将当前通路的评分结果添加到all_scores中
        all_scores = all_scores.append(df, ignore_index=True)

    return all_scores
