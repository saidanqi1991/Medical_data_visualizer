import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1
df = pd.read_csv('medical_examination.csv')

# 2
df['BMI']=df['weight']/((df['height']/100)**2)
df['overweight'] = df['BMI'].apply(lambda x: 1 if x>25 else 0)
df = df.drop(columns=['BMI'])

# 3
df['cholesterol'] = df['cholesterol'].apply(lambda x: 1 if x>1 else 0)
df['gluc'] = df['gluc'].apply(lambda x: 1 if x>1 else 0)

# 4
def draw_cat_plot():
    # 5
    df_cat = pd.melt(df,
       id_vars = ['id', 'age', 'sex', 'height', 'weight', 'ap_hi', 'ap_lo', 'cardio'],
       value_vars = ['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'], 
       var_name = 'variable',
       value_name = 'value')

    # 6
    df_cat = df_cat.groupby(['cardio', 'variable', 'value']).size().reset_index(name='total')
    

    # 7
    catplot = sns.catplot(x = 'variable', y = 'total', hue = 'value', col = 'cardio', data = df_cat, kind='bar', height = 5, aspect = 1.5)

    # 8
    fig = catplot.fig

    # 9
    fig.savefig('catplot.png')
    return fig
# 10
def draw_heat_map():
    # 11 Clean the data in the df_heat variable
    df_heat = df.copy()
    to_drop = df_heat.loc[
            (df['ap_lo'] > df['ap_hi']) |
            (df['height'] < df['height'].quantile(0.025)) | (df['height'] > df['height'].quantile(0.975)) |
            (df['weight'] < df['weight'].quantile(0.025)) | (df['weight'] > df['weight'].quantile(0.975))
            ].index
    df_heat = df_heat.drop(to_drop)

    # 12
    corr = df_heat.corr()

    # 13
    mask = np.triu(np.ones_like(corr, dtype=bool))


    # 14
    fig, ax = plt.subplots()

    # 15

    sns.heatmap(corr, mask=mask, annot=True, cmap='coolwarm', fmt='.1f', square=True, ax=ax)

    # 16
    fig.savefig('heatmap.png')
    return fig
