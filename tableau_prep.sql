-- View 1: Flattened Cohort Retention Matrix
CREATE OR REPLACE VIEW v_tableau_cohort_retention AS
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
)
SELECT 
    f.cohort_month,
    EXTRACT(MONTH FROM AGE(s.activity_month, f.cohort_month)) + 
    EXTRACT(YEAR FROM AGE(s.activity_month, f.cohort_month)) * 12 AS months_since_first_loan,
    COUNT(DISTINCT s.borrower_id) as active_users
FROM first_loans f
LEFT JOIN subsequent_loans s ON f.borrower_id = s.borrower_id
GROUP BY 1, 2;

-- View 2: Borrower Demographics, RFM Segment & LTV
CREATE OR REPLACE VIEW v_tableau_borrower_ltv AS
SELECT 
    d.borrower_id,
    d.age,
    d.location,
    d.income_bracket,
    r.segment AS rfm_segment,
    SUM(l.funded_amount) AS lifetime_ltv
FROM borrowers_demographics d
JOIN rfm_segments r ON d.borrower_id = r.borrower_id
JOIN loans l ON d.borrower_id = l.borrower_id
GROUP BY 
    d.borrower_id,
    d.age,
    d.location,
    d.income_bracket,
    r.segment
HAVING SUM(l.funded_amount) > 0 AND SUM(l.funded_amount) < 50000;
