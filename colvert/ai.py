from openai import AsyncOpenAI

from .database import Database


class AI:
    def __init__(self):
        self._client = AsyncOpenAI()


    async def prompt_to_sql(self, db: Database, prompt):
        schema = await db.schema()
        prompt = f"""
        You are a DuckDB expert. Given an input question, create a syntactically correct DuckDB query to run.
        This is the question you are required to answer:
        {prompt}
        
        The response should be a valid DuckDB query.

        The database schema is as follows:
        {schema}

        Do not include any additional information or context.
        """
        response = await self._client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
        )
        if response.choices[0].message.content:
            text = response.choices[0].message.content        
            sql = text.split("```sql")[1].strip()
            sql = sql.replace("```", "")
            return sql
        else:
            return "Error: No response from the AI model."
        
    
    async def sql_to_prompt(self, sql):
        prompt = "Transform the following SQL query to a prompt for an AI model:\n" + sql
        response = await self._client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
        )
        if response.choices[0].message.content:
            return response.choices[0].message.content.strip('"')
        else:
            return "Error: No response from the AI model."
    