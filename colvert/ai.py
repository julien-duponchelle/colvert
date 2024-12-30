import os

os.environ["LITELLM_LOCAL_MODEL_COST_MAP"] = (
    "True"  # Prevent litellm to fetch the data from internet
)

import litellm  # noqa: E402

from .database import Database  # noqa: E402
from .settings import Settings  # noqa: E402


class AIError(Exception):
    pass


async def _completion(prompt) -> str | None:
    settings = Settings()
    try:
        response = await litellm.acompletion(
            model=settings.get("ai", "model"),
            messages=[{"role": "user", "content": prompt}],
            stream=False,
            api_key=settings.get("ai", "api_key"),
        )
    except litellm.exceptions.AuthenticationError as e:
        raise AIError("AI Error: Authentication Error") from e
    except litellm.exceptions.APIConnectionError as e:
        raise AIError("AI Error: Connection Error") from e
    except litellm.exceptions.BudgetExceededError as e:
        raise AIError("AI Error: Budget exceeded") from e
    except litellm.exceptions.ContextWindowExceededError as e:
        raise AIError("AI Error: Context window exceeded") from e
    except litellm.exceptions.RateLimitError as e:
        raise AIError("AI Error: Rate limit exceeded") from e
    except litellm.exceptions.APIError as e:
        raise AIError("AI Error: API Error") from e
    except Exception as e:
        raise AIError(f"AI Error: {e}") from e
    return response.choices[0].message.content  # type: ignore


async def prompt_to_sql(db: Database, prompt):
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
    text = await _completion(prompt)
    if text is None:
        return "Error: No response from the AI model."
    elif "```sql" in text:
        sql = text.split("```sql")[1].strip()
        sql = sql.replace("```", "")
        return sql
    else:
        return text
        

async def sql_to_prompt(sql):
    prompt = "Transform the following SQL query to a prompt for an AI model:\n" + sql
    text = await _completion(prompt)
    if text:
        return text.strip('"')
    else:
        return "Error: No response from the AI model."


async def test_model():
    """
    Test the connection to the AI model
    """
    return await _completion("Reply with a joke that the connection to model work")
