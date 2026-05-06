from langchain_community.document_loaders import PyPDFLoader

# Change this to your actual filename
loader = PyPDFLoader("./docs/huskiesfb.pdf")
pages = loader.load()

# Print the last two pages of the PDF to see the most recent info
print("--- Checking the end of your PDF ---")
for page in pages[-2:]:
    print(page.page_content)