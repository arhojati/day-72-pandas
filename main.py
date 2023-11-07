import pandas as pd
import lxml

table_from_html = pd.read_html('https://www.payscale.com/college-salary-report/majors-that-pay-you-back/bachelors')
df = table_from_html[0].copy()
df.columns = ['Rank', 'Major', 'Type', 'EarlyCareerPay', 'MidCareerPay', 'HighMeaning']

for page_no in range(2, 33):
    table_from_html = pd.read_html(f'https://www.payscale.com/college-salary-report/majors-that-pay-you-back/bachelors/page/{page_no}')
    page_df = table_from_html[0].copy()
    page_df.columns = ['Rank', 'Major', 'Type', 'EarlyCareerPay', 'MidCareerPay', 'HighMeaning']
    df = df._append(page_df, ignore_index=True)

df = df[['Major', 'EarlyCareerPay', 'MidCareerPay']]

df.replace({"^Major:": "", "^Early Career Pay:\$": "", "^Mid-Career Pay:\$": "", ",": ""}, regex=True, inplace=True)

# Change datatype of numeric columns
df[["EarlyCareerPay", "MidCareerPay"]] = df[["EarlyCareerPay", "MidCareerPay"]].apply(pd.to_numeric)

print(df.nlargest(5, 'EarlyCareerPay'))
