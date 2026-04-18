import pandas as pd
import numpy as np
import random

# dataset size
N = 50000

regions = ["US", "UAE", "India", "UK", "Germany", "Singapore"]
devices = ["mobile", "desktop", "tablet"]
statuses = ["active", "paused"]

data = []

for i in range(N):

    campaign_id = f"CMP_{i+1}"

    impressions = np.random.randint(1000, 100000)

    ctr = np.random.uniform(0.005, 0.08)
    clicks = int(impressions * ctr)

    conversion_rate = np.random.uniform(0.01, 0.12)
    conversions = int(clicks * conversion_rate)

    cpc = np.random.uniform(0.2, 3.0)
    spend = clicks * cpc

    budget = np.random.randint(200, 5000)

    quality_score = np.random.randint(1, 11)

    region = random.choice(regions)
    device = random.choice(devices)
    status = random.choice(statuses)

    data.append([
        campaign_id,
        impressions,
        clicks,
        conversions,
        round(spend,2),
        budget,
        quality_score,
        region,
        device,
        status
    ])

df = pd.DataFrame(data, columns=[
    "campaign_id",
    "impressions",
    "clicks",
    "conversions",
    "spend",
    "budget",
    "quality_score",
    "region",
    "device",
    "status"
])


# Inject realistic issues

# Low CTR campaigns
low_ctr_indices = np.random.choice(df.index, int(N*0.05), replace=False)
df.loc[low_ctr_indices, "clicks"] = (df.loc[low_ctr_indices,"impressions"] * 0.003).astype(int)

# Conversion tracking broken
zero_conversion_indices = np.random.choice(df.index, int(N*0.04), replace=False)
df.loc[zero_conversion_indices, "conversions"] = 0

# Budget exhausted
budget_exhausted_indices = np.random.choice(df.index, int(N*0.03), replace=False)
df.loc[budget_exhausted_indices, "spend"] = df.loc[budget_exhausted_indices, "budget"]


# Save dataset
df.to_csv("campaigns_dataset.csv", index=False)

print("Dataset generated successfully")
print(df.head())
print(df.foot())
