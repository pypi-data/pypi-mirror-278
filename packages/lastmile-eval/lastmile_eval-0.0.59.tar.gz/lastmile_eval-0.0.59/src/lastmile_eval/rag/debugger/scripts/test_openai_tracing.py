import os
import openai
from opentelemetry import trace as trace_api

from lastmile_eval.rag.debugger.api.tracing import LastMileTracer
from lastmile_eval.rag.debugger.tracing import openai as openai_tracing
from lastmile_eval.rag.debugger.tracing.decorators import traced
from lastmile_eval.rag.debugger.tracing.sdk import get_lastmile_tracer

import openai

import dotenv

dotenv.load_dotenv(os.path.expanduser("~/Documents/.env"))


tracer: LastMileTracer = get_lastmile_tracer(
    tracer_name="my-tracer",
    initial_params={"motivation_quote": "I love staring into the sun"},
    # output_filepath="/Users/jonathan/Projects/eval/tracing_v1.out",
    # output_filepath=OUTPUT_FILE_PATH,
)


@traced(tracer)
#         tracer.start_as_current_span(
#     "root-span"  # Span finishes automatically when retrieval_function ends
# )
def openai_function():  # pylint: disable=missing-function-docstring
    client = openai_tracing.wrap(openai.OpenAI(), tracer)
    # client = openai.OpenAI()

    @traced(tracer)
    def some_llm_function(body):
        result = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": body}],
            temperature=0.5,
        )
        content = result.choices[0].message.content
        return content

    question = "What is the meaning of life?"
    response = some_llm_function(question)
    print("RESPONSE:\n", response)


if __name__ == "__main__":
    openai_function()
