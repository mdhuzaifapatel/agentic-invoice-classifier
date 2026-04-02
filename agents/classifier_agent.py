from google.adk.agents import LlmAgent

classifier_agent = LlmAgent(
    name="invoice_classifier",
    model="gemini-2.5-flash",
    description="Classifies invoices",
    instruction="""
    You are an invoice classifier. Classify the given invoice strictly into ONE of the following categories:

    - TAX → GST, tax-related invoices, government tax invoices
    - INVOICE → Any general sales/purchase invoices

    **VERY IMPORTANT**:
    - **DO NOT** classify any invoice as "TAX" unless it is explicitly related to tax/GST or government-related.
    - If an invoice is **not related to tax**, classify it as "INVOICE".
    - If you are unsure, choose "INVOICE".

    **Return ONLY ONE word**: TAX or INVOICE
    """,
    output_key="classification"
)