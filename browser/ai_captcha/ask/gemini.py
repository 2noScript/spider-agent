import re

from google import genai
from google.genai import types

from browser.ai_captcha.utils import image_to_base64
from browser.settings import AiHelperSettings

client = genai.Client(api_key=AiHelperSettings.google_api_key)


class AskGemini:
    def text(self, image_path: str, model: str = "gemini-2.5-pro"):
        base64_image = image_to_base64(image_path)
        prompt = "Act as a blind person assistant. Read the text from the image and give me only the text answer."
        response = client.models.generate_content(
            model=model,
            contents=[
                {
                    "role": "user",
                    "parts": [
                        {"text": prompt},
                        {
                            "inline_data": {
                                "mime_type": "image/png",
                                "data": base64_image,
                            }
                        },
                    ],
                }
            ],
        )
        return response.text.strip()

    def puzzle_distance_(self, image_path: str, model: str = "gemini-2.5-pro"):
        base64_image = image_to_base64(image_path)
        prompt = """
        Analyze the image and determine the correct slider movement needed to solve the puzzle CAPTCHA.

        Instructions:
            * The goal is to drag the slider **so that the center line of the three-line slider handle** 
            (the vertical bar in the middle of the white circle) aligns **exactly with the horizontal center of the black slot**.
            * The alignment is considered correct only if the **middle vertical line of the handle** 
            is in **perfect vertical alignment** with the **center of the empty slot**.
            * Calculate the **horizontal pixel distance** from the current center of the handle to the center of the empty slot.
            * Movement should be **horizontal only**.
            * Return the number of **pixels to move the slider to the right** to reach perfect alignment.
            * **If the handle is already perfectly aligned with the slot, return 0.**
            * **Do not return a negative number** — assume the handle always starts to the **left** of the target.
            * **Cap the value at 260** if it exceeds this maximum range.
            * **Return only the integer**. No units. No explanation.

        **Expected output:** A single integer (e.g., `134`)
        """

        response = client.models.generate_content(
            model=model,
            contents=[
                {
                    "role": "user",
                    "parts": [
                        {"text": prompt},
                        {
                            "inline_data": {
                                "mime_type": "image/png",
                                "data": base64_image,
                            }
                        },
                    ],
                }
            ],
        )
        return response.text

    def puzzle_correction(self, image_path: str, model: str = "gemini-2.5-pro"):
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

        response = client.models.generate_content(
            model=model,
            contents=[
                {
                    "role": "user",
                    "parts": [
                        {"text": prompt},
                        {
                            "inline_data": {
                                "mime_type": "image/png",
                                "data": base64_image,
                            }
                        },
                    ],
                }
            ],
        )
        return response.text

    def puzzle_correction_direction(
        self, image_path: str, model: str = "gemini-2.5-pro"
    ):
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
        response = client.models.generate_content(
            model=model,
            contents=[
                {
                    "role": "user",
                    "parts": [
                        {"text": prompt},
                        {
                            "inline_data": {
                                "mime_type": "image/png",
                                "data": base64_image,
                            }
                        },
                    ],
                }
            ],
        )
        return response.text.strip()

    def best_fit(self, image_path: str, model: str = "gemini-2.5-pro"):
        base64_image = image_to_base64(image_path)
        prompt = """
        You are given multiple images of a puzzle CAPTCHA attempt. Your task is to select the image where the puzzle piece is placed most correctly into the slot.
        Rules:
            * There must be **no visible black gap or dark space** between the piece and the slot edges. Any image with a gap must be disqualified.
            * Among images with no gaps, choose the one with the **most precise fit** and **least misalignment**.
            * Ignore all other UI elements like sliders or buttons.
        Respond with **only the index number** (e.g., 0, 1, 2) of the best image.
        """

        response = client.models.generate_content(
            model=model,
            contents=[
                {
                    "role": "user",
                    "parts": [
                        {"text": prompt},
                        {
                            "inline_data": {
                                "mime_type": "image/png",
                                "data": base64_image,
                            }
                        },
                    ],
                }
            ],
        )
        return response.text.strip()

    def audio(self, audio_path: str, model: str = "gemini-2.5-pro"):

        sys_instr = (
            "The audio is in American English. Type only the letters/numbers you hear clearly. "
            "Ignore background noise. Enter characters in exact order."
        )

        with open(audio_path, "rb") as f:
            audio_bytes = f.read()

        response = client.models.generate_content(
            model=model,
            config=types.GenerateContentConfig(system_instruction=sys_instr),
            contents=[
                types.Part.from_bytes(data=audio_bytes, mime_type="audio/mpeg"),
                "Transcribe the captcha from this audio file. Output only the characters.",
            ],
        )

        raw_text = response.text if response.text else ""
        cleaned_transcription = re.sub(r"[^a-zA-Z0-9]", "", raw_text.strip())

        return cleaned_transcription

    def recaptcha_instructions(self, image_path, model="gemini-2.5-pro"):

        base64_image = image_to_base64(image_path)

        prompt = (
            "Analyze the blue instruction bar in the image. Identify the primary object. "
            "Respond with only the single object name in lowercase (e.g. 'bus', 'hydrant'). "
            "If the instruction is to 'click skip', return 'skip'."
        )

        response = client.models.generate_content(
            model=model,
            contents=[
                {"inline_data": {"mime_type": "image/png", "data": base64_image}},
                {"text": prompt},
            ],
        )

        result = response.text.strip().lower()
        result = re.sub(r"[^a-z]", "", result)
        return result

    def if_tile_contains(
        self, image_path: str, object_name: str, model="gemini-2.5-pro"
    ):
        base64_image = image_to_base64(image_path)

        prompt = (
            f"Does this image clearly contain a '{object_name}' or a recognizable part of it? "
            "Answer 'true' only if you are certain. Otherwise, answer 'false'. "
            "Output only the word 'true' or 'false'."
        )

        try:
            response = client.models.generate_content(
                model=model,
                contents=[
                    {"inline_data": {"mime_type": "image/png", "data": base64_image}},
                    {"text": prompt},
                ],
            )

            result = re.sub(r"[^a-z]", "", response.text.strip().lower())

            return result == "true"

        except Exception as e:
            print(f"Error analyzing tile: {e}")
            return False
