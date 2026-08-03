 ---
description: 'Database analysis and code generation for MySQL local integration'
tools: ['mysql-local/*']
---
# Skill: MySQL Local Integration

You have access to a local MySQL database via the MCP tool using mysql-local/*.
When asked to generate database-related code, strictly follow these steps:
1. **Investigate Schema:** List tables and describe the relevant table structure before writing code.
2. **Validate:** Use the MCP tool to test complex queries.
3. **Generate Code:** Output the application code mapping snake_case to camelCase.

When asked to analyze database data, use the mysql-local/* and search for the table that contains the relevant data. Example: If asked to analyze the best customer profit and name, search for a table named 'customers' or similar and run the query to find the customer more profitable. If the table is not found, respond with "Table not found" and do not generate any code. Steps to follow:
1. **Identify Table:** Search for the table that contains the relevant data.
2. **Analyze Data:** Run the query to analyze the data. 
3. **Output Results:** Present the results in a clear format, including any relevant metrics or insights.
