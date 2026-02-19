few_shots = [
    # Basic product lookup with exact match
    {
        "Question": "price of Sunglasses",
        "SQLQuery": "SELECT `price` FROM `Table1` WHERE `product_name` = 'Sunglasses'",
        "SQLResult": "19.99",
        "Answer": "The price of Sunglasses is $19.99",
    },
    # Case-insensitive product search with wildcards
    {
        "Question": "show me all bluetooth products",
        "SQLQuery": "SELECT `sku`, `product_name`, `price`, `stock` FROM `Table1` WHERE LOWER(`product_name`) LIKE LOWER('%bluetooth%') ORDER BY `price`",
        "SQLResult": "[SKU-3, 'Bluetooth Headphones', 59.99, 45]",
        "Answer": "Found 1 Bluetooth product: Bluetooth Headphones (SKU-3) priced at $59.99 with 45 units in stock",
    },
    # Multi-word product search with variations
    {
        "Question": "do you have any wireless mouse in stock?",
        "SQLQuery": "SELECT `product_name`, `stock`, `price` FROM `Table1` WHERE LOWER(`product_name`) LIKE LOWER('%wireless%mouse%') OR LOWER(`product_name`) LIKE LOWER('%wireless%') AND LOWER(`product_name`) LIKE LOWER('%mouse%')",
        "SQLResult": "['Wireless Mouse', 120, 25.99]",
        "Answer": "Yes, Wireless Mouse is in stock with 120 units available at $25.99 each",
    },
    # Category filtering with price range
    {
        "Question": "what electronics items cost less than 50 dollars?",
        "SQLQuery": "SELECT `product_name`, `price`, `stock` FROM `Table1` WHERE LOWER(`category`) = 'electronics' AND `price` < 50 ORDER BY `price`",
        "SQLResult": "[['Wireless Mouse', 25.99, 120], ['Smartphone Stand', 9.99, 150], ['LED Desk Lamp', 27.5, 40], ['Wireless Charger', 29.99, 75]]",
        "Answer": "There are 4 electronics items under $50: Wireless Mouse ($25.99), Smartphone Stand ($9.99), LED Desk Lamp ($27.50), and Wireless Charger ($29.99)",
    },
    # Aggregate query - count by category
    {
        "Question": "how many different products do you have in each category?",
        "SQLQuery": "SELECT `category`, COUNT(*) as `product_count` FROM `Table1` GROUP BY `category` ORDER BY `product_count` DESC",
        "SQLResult": "[['Electronics', 5], ['Apparel', 3], ['Appliances', 3], ['Fitness', 2], ['Accessories', 2], ['Footwear', 1], ['Furniture', 1], ['Bags', 1], ['Stationery', 1]]",
        "Answer": "Product count by category: Electronics (5), Apparel (3), Appliances (3), Fitness (2), Accessories (2), and 1 each in Footwear, Furniture, Bags, and Stationery",
    },
    # Low stock alert query
    {
        "Question": "which products are running low on stock (less than 20 units)?",
        "SQLQuery": "SELECT `product_name`, `category`, `stock` FROM `Table1` WHERE `stock` < 20 ORDER BY `stock` ASC",
        "SQLResult": "[['Office Chair', 12, 'Furniture'], ['Denim Jeans', 25, 'Apparel'], ['Winter Jacket', 18, 'Apparel'], ['Coffee Maker', 20, 'Appliances']]",
        "Answer": "Products with low stock (under 20 units): Office Chair (12 units), Denim Jeans (25 units but that's >20, let me recalculate... Actually Coffee Maker has exactly 20 units, and Winter Jacket has 18 units). The critically low items are: Office Chair (12 units) and Winter Jacket (18 units)",
    },
    # Supplier-specific query
    {
        "Question": "what products does TechSource Ltd supply?",
        "SQLQuery": "SELECT `product_name`, `category`, `price`, `stock` FROM `Table1` WHERE `supplier` = 'TechSource Ltd' ORDER BY `category`",
        "SQLResult": "[['Wireless Mouse', 'Electronics', 25.99, 120], ['Smartphone Stand', 'Electronics', 9.99, 150], ['Gaming Keyboard', 'Electronics', 79.99, 35]]",
        "Answer": "TechSource Ltd supplies 3 products: Wireless Mouse ($25.99, 120 in stock), Smartphone Stand ($9.99, 150 in stock), and Gaming Keyboard ($79.99, 35 in stock)",
    },
    # Price statistics
    {
        "Question": "what's the average price of apparel items?",
        "SQLQuery": "SELECT ROUND(AVG(`price`), 2) as `avg_price`, COUNT(*) as `item_count` FROM `Table1` WHERE LOWER(`category`) = 'apparel'",
        "SQLResult": "[58.33, 3]",
        "Answer": "The average price of apparel items is $58.33 across 3 products (Cotton T-Shirt: $15, Denim Jeans: $39.99, Winter Jacket: $120)",
    },
    # Complex search with multiple conditions
    {
        "Question": "find me affordable fitness products under 100 dollars that are in stock",
        "SQLQuery": "SELECT `product_name`, `price`, `stock` FROM `Table1` WHERE LOWER(`category`) IN ('fitness', 'footwear') AND `price` < 100 AND `stock` > 0 ORDER BY `price`",
        "SQLResult": "[['Yoga Mat', 22, 80], ['Running Shoes', 89.5, 30], ['Sports Watch', 149.99, 22]]",
        "Answer": "Affordable fitness/footwear products under $100: Yoga Mat ($22, 80 in stock) and Running Shoes ($89.50, 30 in stock). Note: Sports Watch is $149.99 which is over $100",
    },
    # Inventory value calculation
    {
        "Question": "what's the total value of electronics inventory?",
        "SQLQuery": "SELECT SUM(`price` * `stock`) as `total_value` FROM `Table1` WHERE LOWER(`category`) = 'electronics'",
        "SQLResult": "[7219.15]",
        "Answer": "The total value of electronics inventory is $7,219.15 across all electronic items",
    },
    # Search with partial matching (handling typos/variations)
    {
        "Question": "do you sell backpacks or bags?",
        "SQLQuery": "SELECT `product_name`, `category`, `price`, `stock` FROM `Table1` WHERE LOWER(`product_name`) LIKE LOWER('%backpack%') OR LOWER(`product_name`) LIKE LOWER('%bag%') OR LOWER(`category`) LIKE LOWER('%bag%')",
        "SQLResult": "[['Laptop Backpack', 'Bags', 49.99, 60]]",
        "Answer": "Yes, we have Laptop Backpack in the Bags category, priced at $49.99 with 60 units in stock",
    },
    # Seasonal product check
    {
        "Question": "what winter clothing do you have?",
        "SQLQuery": "SELECT `product_name`, `price`, `stock` FROM `Table1` WHERE LOWER(`product_name`) LIKE LOWER('%winter%') OR LOWER(`product_name`) LIKE LOWER('%jacket%') OR LOWER(`product_name`) LIKE LOWER('%coat%')",
        "SQLResult": "[['Winter Jacket', 120, 18]]",
        "Answer": "We have Winter Jacket priced at $120 with 18 units in stock",
    },
    # Most expensive product
    {
        "Question": "what's your most expensive product?",
        "SQLQuery": "SELECT `product_name`, `category`, `price` FROM `Table1` ORDER BY `price` DESC LIMIT 1",
        "SQLResult": "['Office Chair', 'Furniture', 149.99]",
        "Answer": "The most expensive product is Office Chair at $149.99 in the Furniture category",
    },
    # Category with most products
    {
        "Question": "which category has the most products?",
        "SQLQuery": "SELECT `category`, COUNT(*) as `count` FROM `Table1` GROUP BY `category` ORDER BY `count` DESC LIMIT 1",
        "SQLResult": "['Electronics', 5]",
        "Answer": "Electronics is the largest category with 5 different products",
    },
    # Fuzzy search for similar products
    {
        "Question": "show me something for my morning coffee",
        "SQLQuery": "SELECT `product_name`, `category`, `price`, `stock` FROM `Table1` WHERE LOWER(`product_name`) LIKE LOWER('%coffee%') OR LOWER(`product_name`) LIKE LOWER('%kettle%') OR LOWER(`category`) = 'appliances' AND LOWER(`product_name`) LIKE LOWER('%maker%')",
        "SQLResult": "[['Coffee Maker', 'Appliances', 99.99, 20], ['Electric Kettle', 'Appliances', 34.99, 50]]",
        "Answer": "For your morning coffee, we have Coffee Maker ($99.99, 20 in stock) and Electric Kettle ($34.99, 50 in stock) in the Appliances category",
    },
    # Multiple suppliers check
    {
        "Question": "which suppliers provide electronics?",
        "SQLQuery": "SELECT DISTINCT `supplier` FROM `Table1` WHERE LOWER(`category`) = 'electronics' ORDER BY `supplier`",
        "SQLResult": "['BrightLite', 'PowerTech', 'SoundWave Inc', 'TechSource Ltd']",
        "Answer": "The electronics category has products from 4 suppliers: BrightLite, PowerTech, SoundWave Inc, and TechSource Ltd",
    },
    {
        "Question": "Which suppliers are performing significantly above normal in terms of total inventory value compared to other suppliers, but only among those suppliers whose products have not had any stockouts in the last 30 days, and whose average product price is above the overall average product price across the entire store? Also tell me by how much each of those suppliers exceeds the average supplier inventory value.",
        "SQLQuery": """
-- Step 1: Calculate overall averages first
WITH overall_stats AS (
    SELECT 
        AVG(price) as overall_avg_price,
        (SELECT AVG(supplier_total) FROM 
            (SELECT SUM(price * stock) as supplier_total 
             FROM Table1 GROUP BY supplier) as supplier_totals
        ) as overall_avg_supplier_value
    FROM Table1
),

-- Step 2: Calculate supplier-level metrics
supplier_metrics AS (
    SELECT 
        supplier,
        SUM(price * stock) as total_inventory_value,
        AVG(price) as avg_product_price,
        COUNT(*) as product_count,
        -- Check for any zero-stock products (proxy for stockouts)
        SUM(CASE WHEN stock = 0 THEN 1 ELSE 0 END) as zero_stock_count,
        -- Check if any product might have had stockouts (using stock=0 as indicator)
        CASE WHEN SUM(CASE WHEN stock = 0 THEN 1 ELSE 0 END) > 0 
             THEN 'Has stockouts' 
             ELSE 'No stockouts' 
        END as stockout_status
    FROM Table1
    GROUP BY supplier
)

-- Step 3: Apply all filters and calculate excess
SELECT 
    sm.supplier,
    sm.total_inventory_value,
    sm.avg_product_price,
    os.overall_avg_supplier_value,
    sm.total_inventory_value - os.overall_avg_supplier_value as excess_amount,
    ROUND((sm.total_inventory_value / os.overall_avg_supplier_value - 1) * 100, 2) as percent_above_average,
    sm.stockout_status,
    sm.zero_stock_count
FROM supplier_metrics sm
CROSS JOIN overall_stats os
WHERE 
    sm.zero_stock_count = 0  -- No current stockouts
    AND sm.avg_product_price > os.overall_avg_price
    AND sm.total_inventory_value > os.overall_avg_supplier_value * 1.2  -- 20% above = "significantly"
ORDER BY sm.total_inventory_value DESC;
        """,
        "SQLResult": "[('ActiveGear Co', 5984.78, 119.75, 3172.73, 2812.05, 88.7, 'No stockouts', 0)]",
        "Answer": """Based on the analysis, only ActiveGear Co meets all criteria:
- No stockouts detected
- Average product price ($119.75) above overall average
- Total inventory value ($5,984.78) is 88.7% above average supplier value
- Exceeds average by $2,812.05

Note: The query uses current stock=0 as a proxy for stockouts since no date column exists.""",
    },
    {
        "Question": "Show me products that are underperforming - those with below-average sales velocity and above-average return rates, but only from categories that have at least 5 products.",
        "SQLQuery": """
-- First, get category-level product counts
WITH category_product_counts AS (
    SELECT 
        category,
        COUNT(*) as product_count
    FROM Table1
    GROUP BY category
    HAVING COUNT(*) >= 5
),

-- Calculate overall averages
overall_metrics AS (
    SELECT 
        AVG(sales_velocity) as avg_sales_velocity,
        AVG(return_rate) as avg_return_rate
    FROM product_performance
)

-- Get underperforming products
SELECT 
    p.product_name,
    p.category,
    p.sales_velocity,
    p.return_rate,
    (p.return_rate - o.avg_return_rate) as excess_return_rate
FROM product_performance p
INNER JOIN category_product_counts c ON p.category = c.category
CROSS JOIN overall_metrics o
WHERE 
    p.sales_velocity < o.avg_sales_velocity
    AND p.return_rate > o.avg_return_rate
ORDER BY excess_return_rate DESC;
        """,
        "SQLResult": "Table 'product_performance' doesn't exist - query cannot be executed",
        "Answer": "I cannot answer this question because the required tables (product_performance) with sales velocity and return rate data don't exist in the database. Please check if this data is available in other tables or provide the correct table names.",
    },
]