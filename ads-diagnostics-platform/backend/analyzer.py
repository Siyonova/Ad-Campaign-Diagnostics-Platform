import pandas as pd

def analyze_campaigns():

    df = pd.read_csv("campaigns_dataset.csv")

    issues = []

    for _, row in df.iterrows():

        impressions = row["impressions"]
        clicks = row["clicks"]
        conversions = row["conversions"]
        spend = row["spend"]
        budget = row["budget"]

        ctr = clicks / impressions if impressions > 0 else 0

        # Low CTR issue
        if ctr < 0.01:
            issues.append({
                "campaign_id": row["campaign_id"],
                "issue": "Low CTR",
                "explanation": "Ad may have poor relevance or weak keyword targeting"
            })

        # Conversion tracking issue
        if clicks > 100 and conversions == 0:
            issues.append({
                "campaign_id": row["campaign_id"],
                "issue": "Possible conversion tracking failure",
                "explanation": "High clicks but zero conversions detected"
            })

        # Budget exhausted
        if spend >= budget:
            issues.append({
                "campaign_id": row["campaign_id"],
                "issue": "Budget exhausted",
                "explanation": "Campaign limited by daily budget"
            })

    return issues


if __name__ == "__main__":
    results = analyze_campaigns()

    for r in results[:10]:
        print(r)