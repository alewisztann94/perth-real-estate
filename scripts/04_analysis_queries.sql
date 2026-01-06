-- ============================================================================
-- PERTH REAL ESTATE ANALYSIS QUERIES
-- ============================================================================

-- ----------------------------------------------------------------------------
-- PRICE ANALYSIS
-- ----------------------------------------------------------------------------

-- Median and average price by suburb (top 20 by volume)
WITH suburb_stats AS (
    SELECT 
        suburb,
        COUNT(*) as sales_count,
        ROUND(AVG(price), 0) as avg_price
    FROM properties
    GROUP BY suburb
),
suburb_medians AS (
    SELECT 
        suburb,
        ROUND(price, 0) as median_price
    FROM (
        SELECT 
            suburb,
            price,
            ROW_NUMBER() OVER (PARTITION BY suburb ORDER BY price) as rn,
            COUNT(*) OVER (PARTITION BY suburb) as cnt
        FROM properties
    )
    WHERE rn = (cnt + 1) / 2
)
SELECT 
    s.suburb,
    s.sales_count,
    s.avg_price,
    m.median_price
FROM suburb_stats s
JOIN suburb_medians m ON s.suburb = m.suburb
ORDER BY s.sales_count DESC
LIMIT 20;



-- Price distribution (bands)
SELECT 
    CASE 
        WHEN price < 300000 THEN '0-300K'
        WHEN price < 500000 THEN '300-500K'
        WHEN price < 750000 THEN '500-750K'
        WHEN price < 1000000 THEN '750K-1M'
        WHEN price < 1500000 THEN '1-1.5M'
        WHEN price < 2000000 THEN '1.5-2M'
        ELSE '2M+'
    END as price_band,
    COUNT(*) as property_count,
    ROUND( COUNT(*) * 100.0 / (SELECT COUNT(*) FROM properties)  , 1) as percentage --ensure conversion to float
FROM properties
GROUP BY 1
ORDER BY MIN(price);


-- ----------------------------------------------------------------------------
-- GEOGRAPHIC ANALYSIS
-- ----------------------------------------------------------------------------

-- Price vs distance to CBD (bands)
-- convert to kilometres (cbd_dist in metres)
SELECT 
    CASE 
        WHEN cbd_dist/1000 < 5 THEN '0-5km'
        WHEN cbd_dist/1000 < 10 THEN '5-10km'
        WHEN cbd_dist/1000 < 15 THEN '10-15km'
        WHEN cbd_dist/1000 < 20 THEN '15-20km'
        WHEN cbd_dist/1000 < 30 THEN '20-30km'
        ELSE '30km+'
    END as distance_band,
    COUNT(*) as property_count,
    ROUND(AVG(price), 0) as avg_price
FROM properties
GROUP BY 1
ORDER BY MIN(cbd_dist);


-- Top 10 most expensive suburbs (min 20 sales)
SELECT 
    suburb,
    COUNT(*) as sales_count,
    ROUND(AVG(price), 0) as avg_price
FROM properties
GROUP BY suburb
HAVING COUNT(*) >= 20
ORDER BY avg_price DESC
LIMIT 10;


-- Top 10 least expensive suburbs (min 20 sales)
SELECT 
    suburb,
    COUNT(*) as sales_count,
    ROUND(AVG(price), 0) as avg_price
FROM properties
GROUP BY suburb
HAVING COUNT(*) >= 20
ORDER BY avg_price ASC
LIMIT 10;


-- ----------------------------------------------------------------------------
-- TEMPORAL ANALYSIS (2021 vs 2024)
-- ----------------------------------------------------------------------------

-- Overall price change 2021 vs 2024
SELECT 
    source,
    COUNT(*) as sales_count,
    ROUND(AVG(price), 0) as avg_price
FROM properties
GROUP BY source;


-- Suburbs with biggest price growth (min 10 sales each year)
WITH suburb_years AS (
    SELECT 
        suburb,
        source,
        COUNT(*) as sales_count,
        AVG(price) as avg_price
    FROM properties
    GROUP BY suburb, source
    HAVING COUNT(*) >= 10
)
SELECT 
    s21.suburb,
    s21.sales_count as sales_2021,
    s24.sales_count as sales_2024,
    ROUND(s21.avg_price, 0) as avg_2021,
    ROUND(s24.avg_price, 0) as avg_2024,
    ROUND((s24.avg_price - s21.avg_price) / s21.avg_price * 100, 1) as pct_change
FROM suburb_years s21
JOIN suburb_years s24 
    ON s21.suburb = s24.suburb
WHERE s21.source = '2021_dataset'
    AND s24.source = '2024_dataset'
ORDER BY pct_change DESC
LIMIT 15;


-- ----------------------------------------------------------------------------
-- PROPERTY CHARACTERISTICS
-- ----------------------------------------------------------------------------

-- Price by bedroom count
SELECT 
    bedrooms,
    COUNT(*) as property_count,
    ROUND(AVG(price), 0) as avg_price,
    ROUND(AVG(land_area), 0) as avg_land_size
FROM properties
WHERE bedrooms BETWEEN 1 AND 6
GROUP BY bedrooms
ORDER BY bedrooms;


-- Land size vs price correlation (bands)
SELECT 
    CASE 
        WHEN land_area < 300 THEN '0-300sqm'
        WHEN land_area < 500 THEN '300-500sqm'
        WHEN land_area < 700 THEN '500-700sqm'
        WHEN land_area < 1000 THEN '700-1000sqm'
        ELSE '1000sqm+'
    END as land_band,
    COUNT(*) as property_count,
    ROUND(AVG(price), 0) as avg_price
FROM properties
WHERE land_area > 0
GROUP BY 1
ORDER BY MIN(land_area);