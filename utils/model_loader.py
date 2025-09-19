from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from utils.config_loader import load_config
from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException
import sys


log=CustomLogger().get_Logger(__name__)

class ModelLoader:
    def __init__(self):
        load_dotenv()
        self.validate_env()
        self.config = load_config()
        log.info("Config loaded",config_keys=list(self.config.keys()))

    def validate_env(self):
        required_vars=["GROQ_API_KEY","GOOGLE_API_KEY"]
        self.api_keys={var:os.getenv(var) for var in required_vars}
        missing=[k for k,v in self.api_keys.items() if not v]
        if missing:
            log.error(f"Missing environment variables:",missing_vars=missing)
            raise DocumentPortalException(f"Missing environment variables: {', '.join(missing)}",sys)
        log.info("Environment variables validated", available_keys=[k for k,v in self.api_keys.items() if self.api_keys[k]])

    def load_embedding_model(self):
        """
        Loading the embedding model from the config file
        :return: embedding model
        """
        try:
           
            log.info("Embedding model loading..")
            model_name=self.config["embedding_model"]["model_name"]

            return GoogleGenerativeAIEmbeddings(model=model_name)
        except Exception as e:
            log.error(f"Error loading embedding model: {e}")
            raise DocumentPortalException(f"Error loading embedding model: {e}", sys)
       

    def load_llm(self):
        """
            Load and return the LLM
            """
        llm_block=self.config["llm"]
        provider_key=os.getenv("LLM_PROVIDER","groq")

        if provider_key not in llm_block:
            log.error(f"LLM provider '{provider_key}' not found in config")
            raise DocumentPortalException(f"LLM provider '{provider_key}' not found in config", sys)

        llm_config=llm_block[provider_key]
        provider=llm_config.get("provider")
        model_name=llm_config.get("model_name")
        temperature=llm_config.get("temperature",0.2)
        max_token=llm_config.get("max_token", 2048)

        log.info("Loading LLM",provider=provider,model_name=model_name,temperature=temperature,max_token=max_token)


        if provider=="google":
            llm=ChatGoogleGenerativeAI(
                model=model_name,
                temperature=temperature,
                max_tokens=max_token
            )
        elif provider=="groq":
            llm=ChatGroq(
                model=model_name,
                temperature=temperature,
                max_tokens=max_token
            )
        else:
            log.error("Unsupported LLM provider",provider=provider )
            raise ValueError(f"Unsupported LLm provider:{provider}")
        return llm
if __name__ == "__main__":
    loader=ModelLoader()

    embeddings=loader.load_embedding_model()
    print(f"Embedding models loaded:{embeddings}")

    llm=loader.load_llm()
    print(f"LLM loaded:{llm}")

    #Test the model
    result=llm.invoke("Hello,How are you?")
    print(f"LLM test result:{result.content}")
   

    