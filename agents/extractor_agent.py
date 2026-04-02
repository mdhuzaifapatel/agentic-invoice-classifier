from google.adk.agents import LlmAgent

extractor_agent = LlmAgent(
    name="doc_text_extractor",
    model="gemini-2.5-flash",
    description="Extracts text from PDF invoices",
    instruction="""
    Extract invoice data into STRICT JSON.

    Format:
    {
      "file_name": "<string>",
      "extracted_data": {
        "invoice_id": {"value": "<string or null>", "confidence": <float>},
        "invoice_date": {"value": "<string or null>", "confidence": <float>},
        "customer_address": {"value": "<string or null>", "confidence": <float>},
        "vendor_address": {"value": "<string or null>", "confidence": <float>},
        "net_amount": {"value": "<string or null>", "confidence": <float>},
        "grand_total": {"value": "<string or null>", "confidence": <float>}
      }
    }

    Rules:
    - Always return valid JSON only
    - Missing → value=null, confidence=0.0
    - Flatten addresses into one line
    - No hallucination
    """,
    output_key="extracted_data"
)