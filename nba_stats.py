import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# 1. Load Data
po = pd.read_csv('Data/team_stats_advanced_po.csv')

# 2. Preparation
po['Style_Index'] = (1 - po['AST_PCT']) * 100
po['Win_Pct'] = (po['W'] / po['GP']) * 100
df_plot = po[po['GP'] >= 4].copy().dropna(subset=['Style_Index', 'Win_Pct'])

# 3. Identify Champions
champions = df_plot.loc[df_plot.groupby('SEASON')['W'].idxmax()].copy()
champions['Label_Year'] = champions['SEASON'].apply(lambda x: int(x[:4]) + 1)

# 4. SELECTIVE LABELS: Keeping only the most iconic "Style" representatives
notable_champs = {
    2017: "2017 Warriors",
    2014: "2014 Spurs",
    2012: "2012 Heat",
    2002: "2002 Lakers",
    2023: "2023 Nuggets"
}

# High-ISO Non-Champions to Label
special_highlights = [
    ('Houston Rockets', '2017-18', '2018 Rockets'),
    ('Oklahoma City Thunder', '2017-18', '2018 Thunder'),
    ('Dallas Mavericks', '2005-06', '2006 Mavs')
]

# 5. Calculate Stats
correlation, p_value = stats.pearsonr(df_plot['Style_Index'], df_plot['Win_Pct'])

# 6. Create Visualization
plt.figure(figsize=(14, 10))
sns.set_style("whitegrid")

# Background: All teams
sns.scatterplot(data=df_plot, x='Style_Index', y='Win_Pct', alpha=0.15, color='gray', s=40)

# Regression Line
sns.regplot(data=df_plot, x='Style_Index', y='Win_Pct', scatter=False, color='red', line_kws={"ls":"--", "lw":2})

# Plot ALL Champions as gold dots
plt.scatter(champions['Style_Index'], champions['Win_Pct'], color='#FFD700', edgecolor='black', s=100, label='NBA Champions', zorder=4)

# Label the SELECTED Champions
for i, row in champions.iterrows():
    year = int(row['Label_Year'])
    if year in notable_champs:
        plt.text(row['Style_Index'], row['Win_Pct'] + 2.5, notable_champs[year], 
                 fontsize=10, ha='center', fontweight='bold', color='black', zorder=5,
                 bbox=dict(facecolor='white', alpha=0.8, edgecolor='gold', boxstyle='round,pad=0.2'))

# Highlight and Label SPECIAL ISO Teams
for team, season, label in special_highlights:
    subset = df_plot[(df_plot['TEAM_NAME'] == team) & (df_plot['SEASON'] == season)]
    if not subset.empty:
        x, y = subset['Style_Index'].values[0], subset['Win_Pct'].values[0]
        plt.scatter(x, y, color='cyan', edgecolor='black', s=150, zorder=6)
        plt.text(x, y - 4, label, fontsize=10, ha='center', fontweight='bold', color='darkblue',
                 bbox=dict(facecolor='white', alpha=0.8, edgecolor='cyan', boxstyle='round,pad=0.2'))

# Formatting
plt.title("The Style Spectrum: Passing Teams vs. Isolation Teams (1997-2023)", fontsize=18, pad=25, fontweight='bold')
plt.xlabel("Style Index (Lower = Passing | Higher = Isolation) -->", fontsize=13)
plt.ylabel("Playoff Win Percentage", fontsize=13)
plt.ylim(-10, 115)
plt.legend(loc='lower left')

plt.savefig('NBA_style_comparison.png', dpi=300, bbox_inches='tight')
plt.show()