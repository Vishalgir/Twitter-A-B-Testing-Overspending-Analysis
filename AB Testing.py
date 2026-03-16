#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#1.	How many campaigns have overspent of greater than 1% of their budget in the control group? In the treatment group?


# In[1]:


import pandas as pd


# In[2]:


df = pd.read_csv('Twitter A_B testing.csv')


# In[3]:


df.head(), df.columns.tolist()


# In[4]:


df.shape


# In[5]:


df["overspend_pct"] = ((df["campaign_spend"] - df["campaign_budget"]) / df["campaign_budget"]) * 100
overspent_df = df[df["overspend_pct"] > 1]


# In[6]:


overspent_counts = overspent_df["treatment"].value_counts().rename(index={False: "Control Group", True: "Treatment Group"})

overspent_counts


# In[ ]:


#2.	Was the new product effective at reducing overspend, and was it more or less effective depending on the company size? Put together an analysis describing how the treatment affected overspend


# In[7]:


avg_overspend_by_treatment = df.groupby("treatment")["overspend_pct"].mean()


# In[8]:


avg_overspend_by_size = df.groupby(["treatment", "company_size"])["overspend_pct"].mean().reset_index()

avg_overspend_by_treatment, avg_overspend_by_size


# In[ ]:


#3.	A product manager on the team is concerned that certain advertisers in the treatment group are entering lower budgets because they are wary of the new product. Provide some evidence to support their suspicions, or show that any differences in budgets are likely due to random fluctuations.


# In[9]:


from scipy import stats
from scipy.stats import ttest_ind


# In[10]:


df["overspend_pct"] = ((df["campaign_spend"] - df["campaign_budget"]) / df["campaign_budget"]) * 100


# In[11]:


control_budgets = df[df["treatment"] == False]["campaign_budget"]
treatment_budgets = df[df["treatment"] == True]["campaign_budget"]


# In[12]:


avg_budget_control = control_budgets.mean()
avg_budget_treatment = treatment_budgets.mean()


# In[13]:


t_stat, p_value = stats.ttest_ind(control_budgets, treatment_budgets, equal_var=False)

avg_budget_control, avg_budget_treatment, p_value


# In[ ]:


#4.	What is the average overspend percentage for campaigns in both the control and treatment groups?


# In[16]:


avg_overspend_pct = df.groupby("treatment")["overspend_pct"].mean()


# In[17]:


t_stat, p_val = stats.ttest_ind(
    df.loc[df["treatment"], "overspend_pct"],
    df.loc[~df["treatment"], "overspend_pct"],
    equal_var=False  # Welch's t-test
)

print("Average overspend percentage:\n", avg_overspend_pct)
print("\nT-test results:", {"t_stat": t_stat, "p_val": p_val})


# In[ ]:


#6. What demographic factors (e.g., industry, company size) correlate with higher overspending rates in both groups?


# In[22]:


df["overspent"] = df["campaign_spend"] > df["campaign_budget"]


# In[24]:


overspending_rate["overspending_rate"] *= 100

print(overspending_rate)


# In[27]:


#8. Is there a statistically significant difference in the percentage of budget spent between the control and treatment groups?


# In[26]:


df["pct_budget_spent"] = (df["campaign_spend"] / df["campaign_budget"]) * 100


# In[28]:


avg_pct_spent = df.groupby("treatment")["pct_budget_spent"].mean()


# In[29]:


t_stat, p_val = stats.ttest_ind(
    df.loc[df["treatment"], "pct_budget_spent"],
    df.loc[~df["treatment"], "pct_budget_spent"],
    equal_var=False  # Welch's t-test
)

print("Average % budget spent:\n", avg_pct_spent)
print("\nT-test results:", {"t_stat": t_stat, "p_val": p_val})


# In[30]:


#9. Does company size have a significant impact on the overspend percentage in both control and treatment groups?


# In[31]:


control_group = df[df["treatment"] == False]
anova_control = stats.f_oneway(
    control_group[control_group["company_size"] == "small"]["overspend_pct"],
    control_group[control_group["company_size"] == "medium"]["overspend_pct"],
    control_group[control_group["company_size"] == "large"]["overspend_pct"]
)


# In[32]:


treatment_group = df[df["treatment"] == True]
anova_treatment = stats.f_oneway(
    treatment_group[treatment_group["company_size"] == "small"]["overspend_pct"],
    treatment_group[treatment_group["company_size"] == "medium"]["overspend_pct"],
    treatment_group[treatment_group["company_size"] == "large"]["overspend_pct"]
)

anova_control.pvalue, anova_treatment.pvalue


# In[ ]:


#10. Is the variance in campaign spend significantly different between the control and treatment groups?


# In[33]:


stat, p_val = stats.levene(
    df.loc[df["treatment"], "campaign_spend"],
    df.loc[~df["treatment"], "campaign_spend"]
)

print("Levene's test results:", {"stat": stat, "p_val": p_val})


# In[34]:


if p_val < 0.05:
    print("✅ Variances are significantly different between the groups.")
else:
    print("❌ No significant difference in variances between the groups.")


# In[ ]:





# In[ ]:




