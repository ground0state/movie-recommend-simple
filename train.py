import json
from collections import defaultdict

import pandas as pd
from surprise import SVD, Dataset, Reader


def filter_top_k_recommend_by_user(predictions, k=-1):
    recommend_by_user = defaultdict(list)
    for uid, iid, rate in predictions:
        recommend_by_user[str(uid)].append([str(iid), float(rate)])

    recommend_by_user_sorted = dict()
    for uid in recommend_by_user.keys():
        recommend_items = recommend_by_user[uid]
        recommend_items = sorted(
            recommend_items,
            key=lambda x: x[1],
            reverse=True)[:k]
        recommend_by_user_sorted[uid] = [elem[0] for elem in recommend_items]
    return recommend_by_user_sorted


# SVDアルゴリズムでレーティングを訓練する
# カラムはuser_id item_id rating timestamp とする
# user_id item_id はオートでキャストされるよう
train_file_path = "ml-100k/ua.base"
train_reader = Reader(line_format="user item rating timestamp", sep="\t")
trainset = Dataset.load_from_file(
    train_file_path, reader=train_reader)

pred_file_path = "ml-100k/ua.test"
pred_df = pd.read_csv(
    pred_file_path,
    names=["uid", "iid", "rating", "timestamp"],
    sep="\t")

algo = SVD(n_epochs=1000, random_state=0)
algo.fit(trainset.build_full_trainset())

# 訓練データには含まれない(user_id, item_id)の組に対して予測を行う
predictions = []
for _, row in pred_df.iterrows():
    # predict メソッドの引数はstr
    _, _, _, rating, _ = algo.predict(str(row.uid), str(row.iid))
    predictions.append(
        [row.uid, row.iid, rating]
    )

# 各ユーザーごとに上位k件のアイテムを取得
# {"uid": ["iid", rating], ...}
result_dict = filter_top_k_recommend_by_user(predictions, k=5)


with open("recommend_by_user.json", "w", encoding="utf-8") as f:
    json.dump(result_dict, f, indent=2)
