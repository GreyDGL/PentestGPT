import os
import time
import uuid

import pinecone
from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Pinecone


class customVectorDB:
    """
    The custom VectorDB implementation behind pinecone to support the chatbot.

    Key features:
    (1) A combination of both local context and global context.
    (2) Data retrieval is not based on user inputs; LLM help to generate the actual retrieval with the embedding query.


    Functionalities:
    (1) Store information into the vectorDB
    (2) Retrieve information from the vectorDB

    """

    def __init__(self, project_name: str, vectordb_name: str):
        """
        Initialize the vectorDB with the project name.
        :param project_name: the unique identifier for the project. It should be the project name.
        :param file_name: the file name to be stored into the vectorDB. It must be provided for proper initialization.
        :param vectordb_name: the name of the vectorDB. It should be the name of the vectorDB to use.
        """
        # project name should not be empty
        assert project_name != ""
        self.project_name = project_name

        # load configurations
        pinecone_api_key = os.getenv("PINECONE_API_KEY", None)
        os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", None)
        # save the abs directory of the vectorDB on top of the project directory
        self.vectordb_directory = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            vectordb_name,
        )
        # create this folder if not exists
        if not os.path.exists(self.vectordb_directory):
            os.mkdir(self.vectordb_directory)

        # create a local directory to store the context for reference
        self.uuid = str(uuid.uuid4())
        self.local_context_directory = os.path.join(
            self.vectordb_directory, self.project_name + "_" + self.uuid
        )
        if not os.path.exists(self.local_context_directory):
            os.mkdir(self.local_context_directory)

        pinecone.init(api_key=pinecone_api_key, environment="gcp-starter")
        # First, check if our index already exists. If it doesn't, we create it
        if self.project_name not in pinecone.list_indexes():
            # we create a new index
            pinecone.create_index(
                name=self.project_name, metric="cosine", dimension=1536
            )
        # The OpenAI embedding model `text-embedding-ada-002 uses 1536 dimensions`
        # upload the first document
        self.vectorDB = Pinecone.from_existing_index(
            self.project_name, OpenAIEmbeddings()
        )

    def __del__(self):
        """
        TODO: Consider deleting the vectorDB. For now just keep the contents in the index.
        :return:
        """
        pass

    def _save_text(self, _text: str) -> str:
        """
        Handler function that saves everything into the temporary folder.
        :param _text:
        :return:
        """
        #  save the _text into the local context directory
        filename = str(uuid.uuid4()) + ".txt"
        # create the file and write the content
        with open(os.path.join(self.local_context_directory, filename), "w") as f:
            f.write(_text)
        return os.path.join(self.local_context_directory, filename)

    def store_file(self, filename: str, metadata: [dict] = None):
        """
        Store the file into the vectorDB. Use `Pinecone.add_texts`
        :param filename: the filename of the file to be stored.
        :param metadata: the metadata of the file to be stored. It is a list of
        :return: None
        """
        loader = TextLoader(filename)
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        texts = text_splitter.split_documents(documents)
        self.vectorDB.add_texts([t.page_content for t in texts])

    def store_text(self, content: str, metadata: [dict] = None):
        """
        Store the text into the vectorDB. Use `Pinecone.add_texts`
        :param content: the text to be stored.
        :return: None
        """
        filename = self._save_text(content)
        self.store_file(filename, metadata=metadata)

    def retrieval(self, keyword: str, metadata: [dict] = None) -> [dict]:
        """
        Retrieve the information from the vectorDB.
        :param keyword: the keyword to be retrieved.
        :param metadata: the metadata of the keyword to be retrieved.
        :return: the retrieval result.
        """

        # TODO: add retrieval for metadata mapping
        retrieval_result = self.vectorDB.similarity_search(keyword)
        # note that to get the response text, use result[i].page_content
        # print("Debug", retrieval_result[0].page_content)
        return retrieval_result

    def delete_index(self):
        """
        Delete the index from the pinecone.
        :return: None
        """
        pinecone.delete_index(name=self.project_name)
