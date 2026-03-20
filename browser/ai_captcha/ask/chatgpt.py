import re
import time

from openai import OpenAI, APIStatusError
from browser.ai_captcha.utils import image_to_base64
from browser.settings import AiHelperSettings

client = OpenAI(api_key=AiHelperSettings.open_api_key)


class AskChatgpt:
    def text(self, image_path: str, model: str = "gpt-4o"):
        prompt = "Act as a blind person assistant. Read the text from the image and give me only the text answer."
        base64_image = image_to_base64(image_path)
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": [{"type": "text", "text": prompt}]},
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}"
                            },
                        },
                        {
                            "type": "text",
                            "text": "Give the only text from the image. If there is no text, give me empty string.",
                        },
                    ],
                },
            ],
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        return response.choices[0].message.content

    def puzzle_distance(self, image_path: str, model: str = "gpt-4o"):
        base64_image = image_to_base64(image_path)
        prompt = """
        As an assistant designed to help a visually impaired individual, I need your keen observation to navigate the visual world around me by describing the relative positions and characteristics of objects in an image.
        Specifically, I need your help with a CAPTCHA puzzle involving a slider. This is crucial for me to maintain my digital interactions and independence.
        Here's what I need you to do:
            Your Task:
                Carefully examine the provided image to identify:
                    - the slider handle (the white circle with a vertical line in its center)
                    - the target slot (the empty black rectangular area)
            My Goal:
                I need to drag the slider so that the middle vertical line of the slider handle
                aligns exactly with the horizontal center of the empty slot.
            The Information I Need:
                Please calculate the horizontal pixel distance from the current center of
                the slider handle to the center of the empty slot.

            Important Notes for Calculation:
                - The movement should be horizontal only.
                - If the handle is already perfectly aligned with the slot, return 0.
                - Do not return a negative number — assume the handle always starts to the left of the target.
                - Cap the value at 260 pixels; if the calculation exceeds this, still report 260.
                - Return only the integer. No units, no explanation, no additional text.
                It's vital that I get this information quickly and precisely.
        Expected Output Example:
            134
            (a single integer only)
        """
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": prompt},
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}"
                            },
                        }
                    ],
                },
            ],
            temperature=0,
            max_tokens=50,
        )
        content = response.choices[0].message.content.strip()
        match = re.search(r"-?\d+", content)
        if match:
            return match.group(0)  # Return the first found integer
        else:
            print(
                f"Warning: OpenAI distance response did not contain an integer: '{content}'."
            )
            return None  # Signal failure

    def puzzle_correction(self, image_path: str, model: str = "gpt-4o"):
        base64_image = image_to_base64(image_path)
        prompt = """
        **CRITICAL ALIGNMENT CORRECTION**
        Your task is to determine the final pixel adjustment required to **perfectly align** the puzzle piece into its slot.
        Instructions:
            * A **perfect fit** means the puzzle piece sits **flush** in the slot with **no visible gray gaps** on either side.
            * **Look carefully**: If you see **any gray space** between the piece and the slot, the alignment is incorrect.
            * If the piece is **too far to the left**, provide a **positive integer** (move right).
            * If the piece is **too far to the right**, provide a **negative integer** (move left).
            * If the alignment is **already perfect**, respond with `0`.
        ⚠️ **Do not guess**. Only respond with a non-zero value if you can clearly identify a misalignment.  
        ⚠️ **Output only the integer. Nothing else. No units, no words.**
        """

        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": prompt},
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}"
                            },
                        }
                    ],
                },
            ],
            temperature=0,
            max_tokens=50,
        )
        content = response.choices[0].message.content.strip()
        match = re.search(r"-?\d+", content)
        if match:
            return match.group(0)  # Return the first found integer
        else:
            print(
                f"Warning: OpenAI correction response did not contain an integer: '{content}'."
            )
            return None  # Signal failure

    def puzzle_correction_direction(self, image_path: str, model: str = "gpt-4o"):
        base64_image = image_to_base64(image_path)
        prompt = """
        You are an expert in visual analysis for automation. Your task is to determine the direction of movement needed to solve a slider puzzle.
        Analyze the provided image, which shows the result of a first attempt. The puzzle piece is the element that was moved from the left. The target is the empty, darker slot it needs to fit into.
        Instructions:
            * If the puzzle piece is to the LEFT of the target slot, respond with only a single '+' character.
            * If the puzzle piece is to the RIGHT of the target slot, respond with only a single '-' character.
            * Do not provide any other characters, words, or explanations.
        Your entire response must be either '+' or '-'.
        """
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": prompt},
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}"
                            },
                        }
                    ],
                },
            ],
        )
        return response.choices[0].message.content.strip()

    def best_fit(self, image_path: str, model: str = "gpt-4o"):
        base64_image = image_to_base64(image_path)
        prompt = """
        You are given multiple images of a puzzle CAPTCHA attempt. Your task is to select the image where the puzzle piece is placed most correctly into the slot.
        The most important rule is that there must be no visible black gap or dark space between the piece and the slot edges. An image with any gap must be disqualified.
        Among images with no gaps, choose the one with the most precise fit and least misalignment.
        Ignore all other UI elements like sliders or buttons.
        Respond with only the index number (e.g., 0, 1, 2) of the best image.
        """
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert at analyzing puzzle captcha images.",
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}"
                            },
                        },
                    ],
                },
            ],
        )
        content = response.choices[0].message.content.strip()
        match = re.search(r"\d+", content)
        if match:  # Index should be a non-negative integer
            return match.group(0)
        else:
            print(
                f"Warning: OpenAI best-fit response did not contain an integer: '{content}'."
            )
            return None  # Signal failure

    def audio(self, audio_path: str, model: str = "gpt-4o-transcribe"):
        prompt = "what is the captcha answer?"
        max_retries = 3
        for attempt in range(max_retries):
            try:
                with open(audio_path, "rb") as audio_file:
                    response = client.audio.transcriptions.create(
                        model=model, file=audio_file, prompt=prompt
                    )
                cleaned_transcription = re.sub(
                    r"[^a-zA-Z0-9]", "", response.text.strip()
                )
                return cleaned_transcription
            except APIStatusError as e:
                if e.status_code == 503 and attempt < max_retries - 1:
                    wait_time = 3 * (attempt + 1)
                    print(
                        f"OpenAI API is overloaded (503). Retrying in {wait_time} seconds..."
                    )
                    time.sleep(wait_time)
                else:
                    print(f"OpenAI API error after retries: {e}")
                    raise e
            except Exception as e:
                print(
                    f"An unexpected error occurred during OpenAI audio transcription: {e}"
                )
                raise e
        raise Exception(
            "Failed to get transcription from OpenAI after multiple retries."
        )

    def recaptcha_instructions(self, image_path: str, model: str = "gpt-4o"):
        base64_image = image_to_base64(image_path)
        prompt = """
        Analyze the blue instruction bar in the image. Identify the primary object the user is asked to select.
        For example:
            - If the instruction says "Select all squares with motorcycles", the object is "motorcycles".
        Respond with only the single object name in lowercase.  
        If the instruction is to "click skip", return "skip".
        """
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}"
                            },
                        },
                    ],
                }
            ],
            temperature=0,
            max_tokens=50,
        )
        return response.choices[0].message.content.strip().lower()

    def if_tile_contains_object(
        self, image_path: str, object_name: str, model: str = "gpt-4o"
    ):
        base64_image = image_to_base64(image_path)
        prompt = f"Does this image clearly contain a '{object_name}' or a recognizable part of a '{object_name}'? Respond only with 'true' if you are certain. If you are unsure or cannot tell confidently, respond only with 'false'."
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}"
                            },
                        },
                    ],
                }
            ],
            temperature=0,
            max_tokens=10,
        )
        return response.choices[0].message.content.strip().lower()
