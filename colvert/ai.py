from litellm import acompletion

from .database import Database


class AI:
    
    async def _completion(self, prompt) -> str | None:
        response = await acompletion(model="openai/gpt-4o", messages=[{"role": "user", "content": prompt}], stream=False)
        return response.choices[0].message.content # type: ignore
                               
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
        text = await self._completion(prompt)
        if text:
            sql = text.split("```sql")[1].strip()
            sql = sql.replace("```", "")
            return sql
        else:
            return "Error: No response from the AI model."
        
    
    async def sql_to_prompt(self, sql):
        prompt = "Transform the following SQL query to a prompt for an AI model:\n" + sql
        text = await self._completion(prompt)
        if text:
            return text.strip('"')
        else:
            return "Error: No response from the AI model."
    