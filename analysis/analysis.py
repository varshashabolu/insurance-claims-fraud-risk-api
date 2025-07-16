import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

DATA_PATH = "data/dataset.csv"
PLOT_PATH = "static/plots"

# Ensure plot folder exists
os.makedirs(PLOT_PATH, exist_ok=True)

def load_data():
    df = pd.read_csv(DATA_PATH)
    # Add Age Group for analysis
    bins = [20, 30, 40, 50, 60]
    labels = ['21-30', '31-40', '41-50', '51-60']
    df['Age_Group'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False)
    return df

def average_claim_by_region():
    df = load_data()
    avg_claims = df.groupby("Region")["Claim_Amount"].mean().to_dict()
    return avg_claims

def fraud_count():
    df = load_data()
    counts = df["Is_Fraud"].value_counts().to_dict()
    return counts

def generate_plots():
    df = load_data()

    # Plot 1: Fraud vs Non-Fraud count
    fraud_counts = df["Is_Fraud"].value_counts()
    plt.figure(figsize=(6,4))
    fraud_counts.plot(kind='bar', color=['green', 'red'])
    plt.title('Fraud vs Non-Fraud Claims')
    plt.xlabel('Claim Status')
    plt.ylabel('Number of Claims')
    plt.tight_layout()
    plt.savefig(f"{PLOT_PATH}/fraud_vs_nonfraud.png")
    plt.close()

    # Plot 2: Average claim by region and policy type
    avg_claims = df.groupby(['Region', 'Policy_Type'])['Claim_Amount'].mean().unstack()
    avg_claims.plot(kind='bar', figsize=(8,5))
    plt.title('Average Claim Amount by Region and Policy Type')
    plt.ylabel('Average Claim Amount')
    plt.xlabel('Region')
    plt.xticks(rotation=0)
    plt.legend(title='Policy Type')
    plt.tight_layout()
    plt.savefig(f"{PLOT_PATH}/avg_claim_by_region_policy.png")
    plt.close()

    # Plot 3: Fraud vs Non-Fraud by Age Group (stacked)
    fraud_age_group = df.groupby(['Age_Group', 'Is_Fraud']).size().unstack().fillna(0)
    fraud_age_group.plot(kind='bar', stacked=True, figsize=(7,5), color=['green', 'red'])
    plt.title('Fraud vs Non-Fraud Claims by Age Group')
    plt.xlabel('Age Group')
    plt.ylabel('Number of Claims')
    plt.legend(title='Fraud Status')
    plt.tight_layout()
    plt.savefig(f"{PLOT_PATH}/fraud_by_age_group.png")
    plt.close()

    # Plot 4: Boxplot claim amount by fraud status
    plt.figure(figsize=(7,5))
    sns.boxplot(x='Is_Fraud', y='Claim_Amount', data=df, palette=['green', 'red'])
    plt.title('Claim Amount Distribution: Fraud vs Non-Fraud')
    plt.xlabel('Fraud Status')
    plt.ylabel('Claim Amount')
    plt.tight_layout()
    plt.savefig(f"{PLOT_PATH}/claim_amount_fraud_boxplot.png")
    plt.close()
