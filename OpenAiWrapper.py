import openai
import Utils
import pandas as pd
import numpy as np
import math

class OpenAiWrapper(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(OpenAiWrapper, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        openai.api_key = Utils.openAi_api_key
        self.engine_id = None
        available = False
        engines = openai.Engine.list()
        for engine in engines.data:
            if engine.id == Utils.default_engine_id:
                self.engine_id = Utils.default_engine_id
                available = True

        if not available:
            while self.engine_id is None:
                for idx, engine in enumerate(engines.data):
                    print(F"{idx}: {engine.id}")
                val = input("Enter number of desired engine-id: ")
                try:
                    self.engine_id = engines.data[int(val)].id
                except:
                    self.engine_id = None

    # Todo: Max request size for tokens is 8192 --> split tokens accordingly and make multiple requests!
    def getEmbeddingVector(self, tokens):

        num_requests = int(math.ceil(len(tokens) / 2048))
        request_data = []
        for i in range(num_requests):
            if (i + 1) * 2048 > len(tokens):
                request_data.append(tokens[(i)*2048:])
            else:
                request_data.append(tokens[(i)*2048:(i+1)*2048])

        responses = []
        for data in request_data:
            response = openai.Embedding.create(engine=self.engine_id, input=data)
            responses.append(response)

        temp_values = []
        temp_tokens = []
        for embeddings in responses:
            for embedding in embeddings['data']:
                idx = embedding['index']
                value = embedding['embedding']
                temp_tokens.append(tokens[idx])
                temp_values.append(np.array(value))

        result = pd.DataFrame(columns=[Utils.col_embedd_token, Utils.col_embedd_values])
        result[Utils.col_embedd_token] = temp_tokens
        result[Utils.col_embedd_values] = temp_values

        result.set_index(Utils.col_embedd_token, inplace=True)
        return result