# -*- coding: utf-8 -*-
"""Untitled231.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1xqlNG7Ufs6PEoVL4vgt3tymto1KTUnup

بارگذاری دیتاست FIFA 23 از فایل CSV به یک DataFrame با استفاده از Pandas
"""

import pandas as pd

# بارگذاری داده‌ها
df = pd.read_csv('/content/CLEAN_FIFA23_official_data.csv')

"""# نمایش 10 ردیف اول و 5 ردیف آخر دیتاست با استفاده از متدهای head() و tail()


"""

# نمایش 10 ردیف اول
print("First 10 rows:")
print(df.head(10))

# نمایش 5 ردیف آخر
print("Last 5 rows:")
print(df.tail(5))

"""# نمایش ابعاد دیتاست (تعداد ردیف‌ها و ستون‌ها) با استفاده از ویژگی shape"""

print(df.shape)

"""# نمایش آمار توصیفی (میانگین، مینیمم، ماکزیمم و غیره) ستون‌های عددی با متد describe()"""

print(df.describe())

"""# نمایش نام ستون‌ها و نوع داده‌های آن‌ها با استفاده از ویژگی dtypes"""

print(df.dtypes)

"""# جمع مقادیر گمشده در هر ستون با ترکیب متدهای isnull() و sum()"""

print(df.isnull().sum())

"""# محاسبه درصد مقادیر گمشده برای هر ستون و حذف ستون‌هایی با بیش از 50 درصد داده گمشده"""

missing_percentage = df.isnull().mean() * 100
df = df.loc[:, missing_percentage <= 50]

"""# پر کردن مقادیر گمشده ستون Club با مقدار "Free Agent" با استفاده از fillna()"""

df['Club'] = df['Club'].fillna('Free Agent')

"""# محاسبه   Height و پر کردن مقادیر گمشده با آن با استفاده از median() و fillna()"""

if 'Height' in df.columns:
    median_height = df['Height'].median()
    df['Height'] = df['Height'].fillna(median_height)
    print({median_height})
else:
    print(df.columns)

"""# حذف بازیکنان تکراری بر اساس ستون ID با استفاده از drop_duplicates()"""

df = df.drop_duplicates(subset='ID')

"""# انتخاب بازیکنانی با امتیاز کلی (Overall) بیشتر از 85 با فیلتر شرطی"""

top_players = df[df['Overall'] > 85]
print(top_players[['Name', 'Overall', 'Club']])

"""# فیلتر کردن بازیکنان آرژانتینی با پست مهاجم (FW) با شرط ترکیبی"""

argentina_forwards = df[(df['Nationality'] == 'Argentina') & (df['Position'].isin(['FW', 'ST', 'CF']))]
print(argentina_forwards[['Name', 'Club', 'Overall']])

"""# انتخاب بازیکنان با سن 18 تا 21 سال و پتانسیل بیشتر از 85 با استفاده از between()"""

young_talents = df[(df['Age'].between(18, 21)) & (df['Potential'] > 85)]
print(young_talents[['Name', 'Age', 'Potential']])

"""# انتخاب 20 بازیکن برتر بر اساس Overall با استفاده از nlargest()"""

top_20_players = df.nlargest(20, 'Overall')[['Name', 'Age', 'Club', 'Overall']]
print(top_20_players)

"""#انتخاب بازیکنانی با دستمزد بیش از 200 هزار یورو"""

high_earners = df[df['Wage(£)'] > 200000]
print(high_earners[['Name', 'Wage(£)', 'Club']])

"""# محاسبه میانگین امتیاز کلی (Overall) بر اساس ملیت با groupby()"""

avg_overall_by_nationality = df.groupby('Nationality')['Overall'].mean().sort_values(ascending=False)
print(avg_overall_by_nationality)

"""# یافتن بازیکن با بالاترین دستمزد در هر تیم با groupby() و idxmax()"""

highest_paid_by_club = df.groupby('Club').apply(lambda x: x.loc[x['Wage(£)'].idxmax()][['Name', 'Wage(£)']])
print(highest_paid_by_club)

"""# محاسبه میانگین سنی بازیکنان بر اساس موقعیت با groupby() و گرد کردن به عدد صحیح"""

avg_age_by_position = df.groupby('Position')['Age'].mean().astype(int)
print(avg_age_by_position)

"""# محاسبه میانه امتیاز کلی (Overall) برای هر تیم با groupby() و median()"""

median_overall_by_club = df.groupby('Club')['Overall'].median().sort_values(ascending=False)
print(median_overall_by_club)

"""# یافتن جوان‌ترین بازیکن در هر ملیت با groupby() و idxmin()"""

youngest_by_nationality = df.groupby('Nationality').apply(lambda x: x.loc[x['Age'].idxmin()][['Name', 'Age']])
print(youngest_by_nationality)

"""# محاسبه شاخص توده بدنی (BMI) با استفاده از وزن (کیلوگرم) و قد (سانتی‌متر)
# BMI
"""

df['BMI'] = df['Weight(lbs.)'] / ((df['Height(cm.)'] / 100) ** 2)
print(df[['Name', 'Height(cm.)', 'Weight(lbs.)', 'BMI']].head())

"""# تعریف تابع برای دسته‌بندی امتیاز کلی به Low، Medium و High و اعمال آن با apply()"""

def categorize_overall(overall):
    if overall < 70:
        return 'Low'
    elif 70 <= overall <= 80:
        return 'Medium'
    else:
        return 'High'

df['Overall_Category'] = df['Overall'].apply(categorize_overall)
print(df[['Name', 'Overall', 'Overall_Category']].head())

"""# تقسیم بازیکنان به 5 گروه با اندازه برابر بر اساس دستمزد با pd.cut()"""

df['Wage_Group'] = pd.cut(df['Weight(lbs.)'], bins=5, labels=['Very Low', 'Low', 'Medium', 'High', 'Very High'])
print("Wage Group added. First few rows:")
print(df[['Name', 'Weight(lbs.)', 'Wage_Group']].head())

"""# تعریف گروه‌های سنی و محاسبه میانگین پتانسیل برای هر گروه با pd.cut() و groupby()"""

bins = [0, 20, 30, 100]
labels = ['U20', '20-30', '30+']
df['Age_Group'] = pd.cut(df['Age'], bins=bins, labels=labels)
avg_potential_by_age = df.groupby('Age_Group')['Potential'].mean().round(1)
print(avg_potential_by_age)

"""#ایجاد جدول محوری برای نمایش میانگین امتیاز کلی بر اساس موقیعت"""

pivot_overall = df.pivot_table(values='Overall', index='Position', columns='Preferred Foot', aggfunc='mean').round(1)
print(pivot_overall)

"""# تقسیم ستون Name به دو ستون First Name و Last Name با str.split()"""

df[['First Name', 'Last Name']] = df['Name'].str.split(' ', n=1, expand=True)
print(df[['Name', 'First Name', 'Last Name']].head())

"""# انتخاب دروازه‌بان‌ها و اضافه کردن ستون  به دیتاست اصلی"""

goalkeepers = df[df['Position'] == 'GK'].copy()
df['Is_Goalkeeper'] = df['Position'] == 'GK'
print(df[['Name', 'Position', 'Is_Goalkeeper']].head(30))

"""# ایجاد جدول برای شمارش بازیکنان بر اساس ملیت و تیم با pd.crosstab()"""

nationality_club_counts = pd.crosstab(df['Nationality'], df['Club'])
print(nationality_club_counts)

"""# ایجاد جدول  و تبدیل آن به فرمت چندسطحی و بازگشت به حالت اولیه"""

club_position_counts = pd.crosstab(df['Club'], df['Position'])
stacked = club_position_counts.stack()
unstacked = stacked.unstack()
print(stacked.head())
print(unstacked.head())

"""# ترکیب دو زیرمجموعه از بازیکنان انگلستان و اسپانیا با pd.concat()"""

england_players = df[df['Nationality'] == 'England']
spain_players = df[df['Nationality'] == 'Spain']
combined_players = pd.concat([england_players, spain_players])
print(combined_players[['Name', 'Nationality', 'Club']].head(10))

"""# رسم هیستوگرام امتیاز کلی با استفاده از Seaborn و Matplotlib"""

import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(10, 6))
sns.histplot(df['Overall'], bins=20, kde=True)
plt.title('Player Overall Ratings')
plt.xlabel('Overall Rating')
plt.ylabel('Frequency')
plt.show()

"""# رسم نمودار میله‌ای برای 10 ملیت برتر بر اساس تعداد بازیکنان"""

top_nationalities = df['Nationality'].value_counts().head(10)
plt.figure(figsize=(10, 6))
sns.barplot(x=top_nationalities.values, y=top_nationalities.index)
plt.title('Top 10 Nationalities by Player Count')
plt.xlabel('Number of Players')
plt.ylabel('Nationality')
plt.show()

"""# رسم نمودار جعبه‌ای برای توزیع دستمزد بر اساس پست"""

plt.figure(figsize=(12, 6))
sns.boxplot(x='Position', y='Wage(£)', data=df)
plt.title('Wage Distribution by Position')
plt.xlabel('Position')
plt.ylabel('Wage (€)')
plt.xticks(rotation=45)
plt.show()

"""# رسم نمودار پراکندگی سن در مقابل موفیعت با رنگ‌بندی بر اساس امتیاز کلی"""

plt.figure(figsize=(10, 6))
sns.scatterplot(x='Age', y='Potential', hue='Overall', size='Overall', data=df)
plt.title('Age vs Potential Colored by Overall')
plt.xlabel('Age')
plt.ylabel('Potential')
plt.show()

"""# رسم نقشه هیپ مپ همبستگی بین Overall، Potential و Wage"""

correlation_matrix = df[['Overall', 'Potential', 'Wage(£)']].corr()
plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
plt.title('Correlation Matrix: Overall, Potential, Wage')
plt.show()