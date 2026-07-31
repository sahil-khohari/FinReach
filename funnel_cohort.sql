-- Query 1: Funnel Conversion Query
WITH funnel_counts AS (
    SELECT
        SUM(CASE WHEN event_type = 'signup' THEN 1 ELSE 0 END) as signup_count,
        SUM(CASE WHEN event_type = 'browse' THEN 1 ELSE 0 END) as browse_count,
        SUM(CASE WHEN event_type = 'apply' THEN 1 ELSE 0 END) as apply_count,
        SUM(CASE WHEN event_type = 'funded' THEN 1 ELSE 0 END) as funded_count,
        SUM(CASE WHEN event_type = 'repaid' THEN 1 ELSE 0 END) as repaid_count,
        SUM(CASE WHEN event_type = 'repeat_apply' THEN 1 ELSE 0 END) as repeat_apply_count
    FROM event_log
)
SELECT
    signup_count,
    browse_count,
    ROUND(browse_count * 100.0 / NULLIF(signup_count, 0), 2) as signup_to_browse_pct,
    apply_count,
    ROUND(apply_count * 100.0 / NULLIF(browse_count, 0), 2) as browse_to_apply_pct,
    funded_count,
    ROUND(funded_count * 100.0 / NULLIF(apply_count, 0), 2) as apply_to_funded_pct,
    repaid_count,
    ROUND(repaid_count * 100.0 / NULLIF(funded_count, 0), 2) as funded_to_repaid_pct,
    repeat_apply_count,
    ROUND(repeat_apply_count * 100.0 / NULLIF(repaid_count, 0), 2) as repaid_to_repeat_pct
FROM funnel_counts;

-- Query 2: Monthly Cohort Retention Query
WITH first_loans AS (
    SELECT 
        borrower_id,
        DATE_TRUNC('month', MIN(event_timestamp)) as cohort_month
    FROM event_log
    WHERE event_type = 'funded'
    GROUP BY borrower_id
),
subsequent_loans AS (
    SELECT 
        e.borrower_id,
        DATE_TRUNC('month', e.event_timestamp) as activity_month
    FROM event_log e
    WHERE e.event_type = 'repeat_apply'
),
cohort_size AS (
    SELECT 
        cohort_month,
        COUNT(DISTINCT borrower_id) as total_users
    FROM first_loans
    GROUP BY cohort_month
),
retention AS (
    SELECT 
        f.cohort_month,
        EXTRACT(MONTH FROM AGE(s.activity_month, f.cohort_month)) + 
        EXTRACT(YEAR FROM AGE(s.activity_month, f.cohort_month)) * 12 AS month_number,
        COUNT(DISTINCT s.borrower_id) as retained_users
    FROM first_loans f
    JOIN subsequent_loans s ON f.borrower_id = s.borrower_id
    WHERE s.activity_month > f.cohort_month
    GROUP BY f.cohort_month, month_number
)
SELECT 
    r.cohort_month,
    cs.total_users,
    r.month_number,
    r.retained_users,
    ROUND(r.retained_users * 100.0 / cs.total_users, 2) as retention_rate_pct
FROM retention r
JOIN cohort_size cs ON r.cohort_month = cs.cohort_month
ORDER BY r.cohort_month, r.month_number;
