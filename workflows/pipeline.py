import uuid
import json
from google.genai.types import Content, Part

from runner import create_runner
from agents.classifier_agent import classifier_agent
from agents.extractor_agent import extractor_agent
from config import APP_NAME, USER_ID

class Pipeline:
    def __init__(self, gcs_service):
        self.gcs = gcs_service

    async def process_pdf(self, pdf):
        session_id = str(uuid.uuid4())

        # ---- CLASSIFICATION ----
        classifier_runner = create_runner(classifier_agent)

        await classifier_runner.session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id=session_id
        )
        
        content = Content(parts=[
            Part.from_bytes(data=pdf["data"], mime_type="application/pdf"),
            Part.from_text(text="Classify this document as TAX or INVOICE")
        ])

        async for _ in classifier_runner.run_async(
            user_id=USER_ID,
            session_id=session_id,
            new_message=content
        ):
            pass

        session = await classifier_runner.session_service.get_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id=session_id
        )

        classification = session.state.get("classification", "INVOICE").upper()
        if classification not in ["TAX", "INVOICE"]:
            print(f"⚠️ Warning: Model output is unexpected, defaulting to 'INVOICE'")
            classification = "INVOICE"
        
        # Debugging classification output
        print(f"Classification Result: {classification}")

        # If unexpected classification, log the whole session output for analysis
        if classification != "TAX" and classification != "INVOICE":
            print("⚠️ Unexpected classification, inspecting raw session output:")
            print(session.state)

        pdf_path = self.gcs.upload_file(
            pdf["data"], classification, pdf["filename"]
        )

        # ---- EXTRACTION ----
        extractor_runner = create_runner(extractor_agent)

        # await extractor_runner.session_service.create_session(
        #     app_name=APP_NAME,
        #     user_id=USER_ID,
        #     session_id=session_id
        # )

        content = Content(parts=[
            Part.from_bytes(data=pdf["data"], mime_type="application/pdf"),
            Part.from_text(text=f"""
                Extract invoice data from this PDF.

                File name: {pdf['filename']}

                Follow STRICT JSON format as instructed.
                Return ONLY JSON.
                """)
        ])

        async for _ in extractor_runner.run_async(
            user_id=USER_ID,
            session_id=session_id,
            new_message=content
        ):
            pass

        session = await extractor_runner.session_service.get_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id=session_id
        )

        extracted = session.state.get("extracted_data")

        def clean_llm_json(output: str):
            if not output:
                return ""

            output = output.strip()

            # Remove ```json and ```
            if output.startswith("```"):
                output = output.replace("```json", "")
                output = output.replace("```", "")

            return output.strip()

        if isinstance(extracted, str):
            try:
                cleaned = clean_llm_json(extracted)
                extracted = json.loads(cleaned)
            except Exception as e:
                print("JSON parsing failed:", e)
                print("RAW OUTPUT:", extracted)
                extracted = {}

        extracted["file_name"] = pdf["filename"]

        json_path = self.gcs.upload_json(extracted, pdf["filename"])

        return {
            "file": pdf["filename"],
            "classification": classification,
            "pdf_path": pdf_path,
            "json_path": json_path,
            "data": extracted
        }