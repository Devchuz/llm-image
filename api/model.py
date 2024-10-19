import base64
import mimetypes
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from fastapi import UploadFile

def classify_skin_tone(image: UploadFile) -> str:
    """
    Classifies the skin tone from an image using Claude Sonnet and LangChain.
    
    Args:
        image (UploadFile): The image file uploaded by the user.
        
    Returns:
        str: The skin tone category.
    """
    # Get the MIME type of the image
    mime_type, _ = mimetypes.guess_type(image.filename)
    
    # Ensure the file is in an accepted format
    if mime_type not in ["image/jpeg", "image/png"]:
        raise ValueError(f"The image type {mime_type} is not supported. Use JPEG or PNG.")
    
    # Read the image bytes and encode it in base64
    image_data = base64.b64encode(image.file.read()).decode("utf-8")
    
    # Instantiate the model with Claude Sonnet
    llm = ChatAnthropic(model="claude-3-5-sonnet-20240620", temperature=0)
    
    # Create the prompt focused on skin tone classification
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are an expert dermatologist. Classify the skin tone from the provided image "
                       "into one of the following categories: 'Pale white skin', 'White skin', 'Light brown skin', "
                       "'Moderate brown skin', 'Dark brown skin', 'Deep brown to black skin'. "
                       "Only respond with the corresponding category."),
            (
                "user",
                [
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:{mime_type};base64,{image_data}"},
                    }
                ],
            ),
        ]
    )
    
    # Create the chain to invoke Claude Sonnet with the prompt
    chain = prompt | llm
    
    # Execute the chain and get the response
    response = chain.invoke({"image_data": image_data})
    
    # Return only the skin tone category
    return response.content
