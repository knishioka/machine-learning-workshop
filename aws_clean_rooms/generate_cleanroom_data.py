import csv
import random
from collections import defaultdict
from datetime import date, timedelta

from faker import Faker


# users.csvの生成
fake = Faker("ja_JP")
data = []
for i in range(30):
    name = fake.name()
    email = fake.email()
    age_group = random.randint(2, 5) * 10
    address_code = random.randint(1, 47)
    data.append([name, email, age_group, address_code])

with open("users.csv", mode="w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["name", "email", "age_group", "address_code"])
    for d in data:
        writer.writerow(d)


users = [d[1] for d in data]

# ads_impressions.csvの生成
ads_impressions = []
impression_date_dict = defaultdict(set)  # 各emailアドレスに対して、既出の日付を記録する辞書
for i in range(1000):
    email = random.choice(users)
    campaign_id = random.randint(1, 10)
    num_impressions = random.randint(2, 100)
    num_clicks = random.randint(1, num_impressions - 1)
    while True:
        # 既出の日付でないランダムな日付を生成
        impression_date = date(2023, 1, 1) + timedelta(days=random.randint(0, 364))
        if impression_date not in impression_date_dict[email]:
            impression_date_dict[email].add(impression_date)
            break
    ads_impressions.append(
        [email, campaign_id, num_impressions, num_clicks, impression_date]
    )
with open("ads_impressions.csv", mode="w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(
        ["email", "campaign_id", "num_impressions", "num_clicks", "impression_date"]
    )
    for d in ads_impressions:
        writer.writerow(d)

# campaigns.csvの生成
campaigns = [[i, f"Campaign {i}"] for i in range(1, 11)]
with open("campaigns.csv", mode="w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["campaign_id", "campaign_name"])
    for c in campaigns:
        writer.writerow(c)

# provider_users.csvの作成
with open("provider_users.csv", mode="w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["email", "annual_income"])
    for user in users:
        writer.writerow([user, random.randint(4, 9) * 100])
