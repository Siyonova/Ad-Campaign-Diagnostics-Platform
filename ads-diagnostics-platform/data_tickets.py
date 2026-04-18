import pandas as pd
import random

tickets = [
    "My ads are getting clicks but no conversions",
    "Why are my ads not showing?",
    "My campaign budget finished too quickly",
    "CTR dropped suddenly yesterday",
    "Impressions are high but nobody is clicking",
    "Conversions stopped tracking",
    "Ads approved but not delivering",
    "Campaign spend increased unexpectedly",
    "Why is my CPC so high?",
    "Traffic from ads decreased"
]

issues = [
    "conversion tracking failure",
    "budget exhausted",
    "low CTR",
    "poor keyword targeting",
    "bid strategy problem"
]

data = []

for i in range(1000):

    ticket_id = f"TICKET_{i+1}"

    text = random.choice(tickets)

    issue = random.choice(issues)

    data.append({
        "ticket_id": ticket_id,
        "ticket_text": text,
        "diagnosed_issue": issue
    })

df = pd.DataFrame(data)

df.to_csv("support_tickets.csv", index=False)

print("Support ticket dataset created")
print("done printing")
