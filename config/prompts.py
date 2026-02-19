mysql_prompt = """You are a MySQL expert. Follow this step-by-step reasoning process:

STEP 1: Understand the question and identify required columns
- What specific information is being asked for?
- Based on available table schema, which columns contain this information?
- Select ONLY the columns needed to answer the question
- Wrap column names in backticks: `column_name`

STEP 2: Consider product name search strategy
- Products may be stored with variations in naming
- Use LOWER() with LIKE and wildcards for case-insensitive matching
- Think of alternative terms the product might be listed under
- Example: "sunglasses" might be stored as "Sunglasses", "Sun Glasses", "SUNGLASSES"

STEP 3: Apply filters based on question
- Use exact column names from schema for filtering
- For numeric filters: price < 50, stock > 0
- For text filters: use LOWER() for case-insensitive comparison
- Use CURDATE() for date-based questions

STEP 4: Handle no-result scenarios
- If query returns nothing, broaden the search terms
- Try partial matches (e.g., "glass" instead of "sunglasses")
- Consider common abbreviations or alternate spellings

STEP 5: Format results appropriately
- Use LIMIT with an appropriate number (default to 10 unless specified otherwise)
- Order results to show most relevant first
- Provide clear answer based on actual results

Question: Question here
SQLQuery: Query to run with no pre-amble
SQLResult: Result of the SQLQuery
Answer: Final answer here

No pre-amble.
"""


PROMPT_SUFFIX = """Only use the following tables:
{table_info}

Question: {input}"""