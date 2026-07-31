import pandas as pd
import numpy as np
from scipy import stats

def build_rfm_segments(df_loans):
    """
    Expects df_loans with columns: borrower_id, funded_amount, funded_date
    """
    current_date = df_loans['funded_date'].max() + pd.Timedelta(days=1)
    
    rfm = df_loans.groupby('borrower_id').agg(
        Recency=('funded_date', lambda x: (current_date - x.max()).days),
        Frequency=('funded_date', 'count'),
        Monetary=('funded_amount', 'sum')
    ).reset_index()
    
    rfm['R_Score'] = pd.qcut(rfm['Recency'].rank(method='first'), 4, labels=[4, 3, 2, 1]) # Lower recency is better
    rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 4, labels=[1, 2, 3, 4]) # Higher is better
    rfm['M_Score'] = pd.qcut(rfm['Monetary'].rank(method='first'), 4, labels=[1, 2, 3, 4])
    
    rfm['RFM_Segment'] = rfm['R_Score'].astype(str) + rfm['F_Score'].astype(str) + rfm['M_Score'].astype(str)
    
    def map_segment(row):
        score = int(row['R_Score']) + int(row['F_Score']) + int(row['M_Score'])
        if score >= 10:
            return 'Champions'
        elif score >= 7:
            return 'Loyal Customers'
        elif score >= 5:
            return 'At Risk'
        else:
            return 'Lost'
            
    rfm['Segment'] = rfm.apply(map_segment, axis=1)
    return rfm

def ab_test_funnel(control_users, control_conversions, variant_users, variant_conversions):
    """
    Performs a two-proportion Z-test.
    """
    prop_A = control_conversions / control_users
    prop_B = variant_conversions / variant_users
    
    # Pooled proportion
    p_pool = (control_conversions + variant_conversions) / (control_users + variant_users)
    
    # Standard error
    se = np.sqrt(p_pool * (1 - p_pool) * (1/control_users + 1/variant_users))
    
    # Z-statistic
    z_stat = (prop_B - prop_A) / se
    
    # P-value (one-sided for B > A)
    p_value = stats.norm.sf(z_stat)
    
    # Confidence Interval for difference (prop_B - prop_A)
    ci_low = (prop_B - prop_A) - 1.96 * se
    ci_high = (prop_B - prop_A) + 1.96 * se
    
    result_data = {
        "variant_a_conversion": round(prop_A, 4),
        "variant_b_conversion": round(prop_B, 4),
        "z_statistic": round(z_stat, 4),
        "p_value": round(p_value, 4),
        "ci_low": round(ci_low, 4),
        "ci_high": round(ci_high, 4),
        "significant": bool(p_value < 0.05),
        "message": "Statistically significant improvement in Variant B." if p_value < 0.05 else "No statistically significant difference."
    }
    
    return result_data

if __name__ == "__main__":
    # Test A/B Test
    ab_test_funnel(5000, 1000, 5000, 1150)
