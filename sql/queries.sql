USE startup_ecosystem;


-- 1. Yearly Funding Analysis

SELECT
    year,
    SUM(amount_in_usd) AS total_funding,
    COUNT(*) AS total_deals,
    AVG(amount_in_usd) AS average_deal_size
FROM startup_funding_final
WHERE year IS NOT NULL
GROUP BY year
ORDER BY year;


-- 2. City Funding Analysis

SELECT
    CASE
        WHEN LOWER(city__location) LIKE '%bangalore%' THEN 'Bengaluru'
        WHEN LOWER(city__location) LIKE '%bengaluru%' THEN 'Bengaluru'
        WHEN LOWER(city__location) LIKE '%hyderabad%' THEN 'Hyderabad'
        WHEN LOWER(city__location) LIKE '%chennai%' THEN 'Chennai'
        WHEN LOWER(city__location) LIKE '%new delhi%' THEN 'New Delhi'
        WHEN LOWER(city__location) LIKE '%delhi%' THEN 'Delhi'
        WHEN LOWER(city__location) LIKE '%mumbai%' THEN 'Mumbai'
        ELSE city__location
    END AS city,
    SUM(amount_in_usd) AS total_funding,
    COUNT(*) AS total_deals,
    AVG(amount_in_usd) AS average_funding
FROM startup_funding_final
WHERE city__location IS NOT NULL
  AND city__location <> 'Unknown'
  AND LOWER(city__location) <> 'xc'
GROUP BY city
ORDER BY total_funding DESC;


-- 3. Sector Funding Analysis

SELECT
    sector_category AS sector,
    SUM(amount_in_usd) AS total_funding,
    COUNT(*) AS total_deals,
    AVG(amount_in_usd) AS average_deal_size
FROM startup_funding_final
WHERE sector_category IS NOT NULL
  AND sector_category <> 'Unknown'
GROUP BY sector_category
ORDER BY total_funding DESC;


-- 4. Funding Concentration

SELECT
    sector_category AS sector,
    SUM(amount_in_usd) AS total_funding,
    ROUND(
        SUM(amount_in_usd) * 100 /
        (SELECT SUM(amount_in_usd)
         FROM startup_funding_final
         WHERE amount_in_usd IS NOT NULL),
        2
    ) AS funding_percentage
FROM startup_funding_final
WHERE sector_category IS NOT NULL
  AND sector_category <> 'Unknown'
  AND amount_in_usd IS NOT NULL
GROUP BY sector_category
ORDER BY total_funding DESC;


-- 5. Year-over-Year Funding Growth

SELECT
    y1.year,
    y1.total_funding,
    y2.total_funding AS previous_year_funding,
    ROUND(
        (y1.total_funding - y2.total_funding)
        * 100 / y2.total_funding,
        2
    ) AS yoy_growth_percent
FROM
    (
        SELECT
            year,
            SUM(amount_in_usd) AS total_funding
        FROM startup_funding_final
        WHERE year IS NOT NULL
        GROUP BY year
    ) y1
LEFT JOIN
    (
        SELECT
            year,
            SUM(amount_in_usd) AS total_funding
        FROM startup_funding_final
        WHERE year IS NOT NULL
        GROUP BY year
    ) y2
ON y1.year = y2.year + 1
ORDER BY y1.year;


-- 6. Sector Deal-Size Volatility

SELECT
    sector_category AS sector,
    COUNT(DISTINCT year) AS years_present,
    SUM(amount_in_usd) AS total_funding,
    AVG(amount_in_usd) AS average_deal_size,
    STDDEV(amount_in_usd) AS funding_volatility
FROM startup_funding_final
WHERE sector_category IS NOT NULL
  AND sector_category <> 'Unknown'
  AND amount_in_usd IS NOT NULL
GROUP BY sector_category
ORDER BY funding_volatility DESC;