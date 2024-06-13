import numpy as np
from scipy import stats
import statsmodels.api as sm
from statsmodels.stats.multicomp import pairwise_tukeyhsd

def check_normality_and_choose_test(df, y_variable, x_group):
    # Check normality for the entire dataset
    normality_p = stats.shapiro(df[y_variable])[1]
    normal = normality_p > 0.05
    unique_groups = df[x_group].unique()
    num_groups = len(unique_groups)
    
    if normal:
        if num_groups > 2:
            test_used = 'ANOVA'
        else:
            test_used = 't-test'
    else:
        test_used = 'Mann-Whitney U test'
    
    # Print normality test result
    print(f"Normality test p-value for the entire dataset (Shapiro): {normality_p}")
    print(f"Data follows normal distribution: {'Yes' if normal else 'No'}")
    
    return test_used, normal, num_groups

def perform_statistical_test(df, y_variable, x_group, test_used, group1=None, group2=None):
    if test_used == 'ANOVA':
        model = sm.formula.ols(f'{y_variable} ~ C({x_group})', data=df).fit()
        anova_table = sm.stats.anova_lm(model, typ=2)
        p = anova_table["PR(>F)"][0]
        U = None
    else:
        data1 = df[y_variable][df[x_group] == group1]
        data2 = df[y_variable][df[x_group] == group2]
        if test_used == 't-test':
            U, p = stats.ttest_ind(data1, data2, alternative='two-sided')
        else:
            U, p = stats.mannwhitneyu(data1, data2, alternative='two-sided')
    
    return U, p

def add_significance_bars(df, x_group, y_variable, labels, axs, fontsize):
    # Check normality and choose the test
    test_used, normal, num_groups = check_normality_and_choose_test(df, y_variable, x_group)
    
    if test_used == 'ANOVA':
        # Perform ANOVA
        model = sm.formula.ols(f'{y_variable} ~ C({x_group})', data=df).fit()
        anova_table = sm.stats.anova_lm(model, typ=2)
        p = anova_table["PR(>F)"][0]
        print(f"ANOVA: p-val: {p}")
        
        if p < 0.05:
            # If ANOVA is significant, perform Tukey's test
            tukey_results = pairwise_tukeyhsd(df[y_variable], df[x_group])
            print(tukey_results)
            
            # tukey_results.plot_simultaneous(ax=axs, ylabel=x_group, xlabel=y_variable, fontsize=fontsize)
            ls = list(range(1, len(labels) + 1))
            # combinations = [(ls[x], ls[y]) for x in range(0, len(ls)-1) for y in range(x+1,len(ls)-1)]
            # a little trick to match the combinations from tukey_results
            combinations = []
            for x in range(0, len(ls)):
                for y in range(x+1,len(ls)):
                    combinations.append((ls[x], ls[y]))
            significant_combinations = [[comb, p] for comb,p in zip(combinations,tukey_results.pvalues)]
            plot_sbars(axs,significant_combinations,fontsize)
            return
       
    else:
    # For pairwise comparisons
        ls = list(range(1, len(labels) + 1))
        combinations = [(ls[x], ls[x + y]) for y in reversed(ls) for x in range((len(ls) - y))]
        significant_combinations = []
        
        for combination in combinations:

            # Perform statistical test
            U, p = perform_statistical_test(df, y_variable, x_group, test_used, labels[combination[0] - 1], labels[combination[1] - 1])
            # Adjust p-values
            p_adj = p * len(combinations)
            print("{} vs {} | {}: {} | padj: {:<2}  p-val: {:<10}".format(
                labels[combination[0] - 1],
                labels[combination[1] - 1],
                test_used,
                "Significant" if p_adj < 0.05 else "Not Significant",
                p_adj,
                p
            ))

            if p_adj < 0.05:
                significant_combinations.append([combination, p_adj])
            else:
                significant_combinations.append([combination, p_adj])
        
        plot_sbars(axs,significant_combinations,fontsize)

        return

def plot_sbars(axs,significant_combinations,fontsize):
    bottom, top = axs.get_ylim()
    y_range = top - bottom
    for i, significant_combination in enumerate(significant_combinations):
        x1 = significant_combination[0][0]
        x2 = significant_combination[0][1]
        level = len(significant_combinations) - i
        bar_height = (y_range * 0.4 * level) + top 
        bar_tips = bar_height - (y_range * 0.02)

        p = significant_combination[1]
       
        if p < 0.001:
            sig_symbol = '***'
        elif p < 0.01:
            sig_symbol = '**'
        elif p < 0.05:
            sig_symbol = '*'
        else:
            sig_symbol = "ns"
        text_height = bar_height + (y_range * 0.01)
        if p < 0.05:
            axs.text((x1 + x2) * 0.5, text_height, sig_symbol, ha='center', va='bottom', c='k', weight='bold', fontsize=fontsize/1.15)
            axs.plot(
                [x1, x1, x2, x2],
                [bar_tips, bar_height, bar_height, bar_tips], lw=2, c='k'
            )

# Example usage (assuming you have a DataFrame `df` with appropriate data):
# fig, ax = plt.subplots()
# add_significance_bars(df, 'group_column', 'value_column', ['A', 'B', 'C'], ax, 12)
# plt.show()


# def add_significance_bars(df, x_group, y_variable, labels, axs, fontsize):
#     ls = list(range(1, len(labels) + 1))
#     combinations = [(ls[x], ls[x + y]) for y in reversed(ls) for x in range((len(ls) - y))]
#     significant_combinations = []
    
#     for combination in combinations:
#         data1 = df[y_variable][df[x_group] == labels[combination[0] - 1]]
#         data2 = df[y_variable][df[x_group] == labels[combination[1] - 1]]
#         U, p = stats.ttest_ind(data1, data2, alternative='two-sided')

#         p_adj = p * len(combinations)
#         print("{} {} x {} {:<30} padj: {:<2}  p-val: {:<10}".format(
#             labels[combination[0] - 1],
#             np.mean(data1),
#             labels[combination[1] - 1],
#             np.mean(data1),
#             p_adj,
#             p
#         ))

#         if p_adj < 0.05:
#             significant_combinations.append([combination, p_adj])
#         else:
#             significant_combinations.append([combination, p_adj])
    

#     bottom, top = axs.get_ylim()
#     y_range = top - bottom
#     for i, significant_combination in enumerate(significant_combinations):
#         x1 = significant_combination[0][0]
#         x2 = significant_combination[0][1]
#         level = len(significant_combinations) - i
#         bar_height = (y_range * 0.4 * level) + top 
#         bar_tips = bar_height - (y_range * 0.02)

#         p = significant_combination[1]
#         if p < 0.001:
#             sig_symbol = '***'
#         elif p < 0.01:
#             sig_symbol = '**'
#         elif p < 0.05:
#             sig_symbol = '*'
#         else:
#             sig_symbol = "ns"
#         text_height = bar_height + (y_range * 0.01)
#         if p<0.05:
#             axs.text((x1 + x2) * 0.5, text_height, sig_symbol, ha='center', va='bottom', c='k', weight='bold',fontsize=fontsize/1.15)
#             axs.plot(
#                 [x1, x1, x2, x2],
#                 [bar_tips, bar_height, bar_height, bar_tips], lw=2, c='k'
#             )