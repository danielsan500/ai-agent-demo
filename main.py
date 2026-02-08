import os, argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import SYSTEM_PROMPT
from call_function import available_functions
from call_function import call_function

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set in environment variables.")

    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    for _ in range(20):
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=messages,
            config=types.GenerateContentConfig(tools=[available_functions],
                                                system_instruction=SYSTEM_PROMPT)
        )

        if response.usage_metadata is None:
            raise RuntimeError("The response doesn't contain usage metadata")
        if args.verbose:
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)


        if not response.function_calls:
            print("Response:")
            print(response.text)
            return 0
        function_results = []
        for function_call in response.function_calls:
            
            function_call_response = call_function(function_call, args.verbose)

            if (
            not function_call_response.parts
            or not function_call_response.parts[0].function_response
            or not function_call_response.parts[0].function_response.response
            ):
                raise Exception("El response esta vacío")
            
            function_results.append(function_call_response.parts[0])
            if args.verbose:
                print(f"-> {function_call_response.parts[0].function_response.response}")
            
            
        messages.append(types.Content(role="user", parts=function_results))      
    
    print(response.text)
    print("han pasado los 20 intentos. Cerramos")
    return 1

if __name__ == "__main__":
    main()