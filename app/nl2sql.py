import json
import os

from openai import OpenAI


client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def generate_sql_from_question(question: str) -> str:
    schema_context = """
    Use only the tables population_production and harvest_production.
    Don't guess table names. Always include WHERE clauses to filter by species, year, or state if possible.
    Be SELECT-only and safe. 
    Reference only the above tables and columns.
    Include a LIMIT 100 if returning more than 100 rows.
    Never include DROP, DELETE, INSERT, or UPDATE.

    Always lowercase string literals when filtering on state and species.
    • States should use lowercase 2-letter codes like 'co', 'wy', 'mt', etc.
    • Species should be lowercase: 'elk', 'deer', or 'pronghorn'.
    """
    functions = [
        {
            "name": "generate_sql",
            "description": "Generate SQL query from natural language input.",
            "parameters": {
                "type": "object",
                "properties": {
                    "sql": {
                        "type": "string",
                        "description": (
                            "SQL query to answer the user's question. "
                            " Available tables: \n"
                            " - harvest_production(state, species, year, season, unit, adult_male, adult_female, young, total_harvest, total_hunters, percent_success, total_rec_days)\n"
                            " - population_production(state, species, herd_name, post_hunt_estimate, male_female_ratio, year, unit)\n"
                            "SQL query to answer the user's question. "
                        ),
                    }
                },
                "required": ["sql"],
            },
        }
    ]

    messages = [
        {"role": "system", "content": schema_context},
        {"role": "user", "content": question},
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            functions=functions,
            function_call={"name": "generate_sql"},
            temperature=0,
        )

        arguments = response.choices[0].message.function_call.arguments
        return json.loads(arguments).get("sql", "-- No SQL returned")
    except Exception as e:
        import traceback

        print("ERROR: OpenAI call failed.")
        traceback.print_exc()
        return "--- Error: OpenAI call failed."
