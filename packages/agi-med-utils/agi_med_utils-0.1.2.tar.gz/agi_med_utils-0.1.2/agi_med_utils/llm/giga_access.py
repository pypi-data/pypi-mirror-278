from base64 import b64encode
from tqdm import tqdm
from gigachat import GigaChat
import typing as t
from itertools import chain
from time import sleep
from tqdm.contrib.concurrent import process_map

class GigaChatEntryPoint:
    def __init__(self, client_id, client_secret):
        self.creds = b64encode(f'{client_id}:{client_secret}'.encode('utf-8')).decode('utf-8')
        self.model = GigaChat(
            credentials=self.creds,
            scope='GIGACHAT_API_CORP',
            verify_ssl_certs=False,
            model='GigaChat-Pro',
            profanity_check=False,
        )
        self.DIM = 1024
        self.ZEROS = [0 for _ in range(self.DIM)]
        self.ERROR_MESSAGE = ''
        self.warmup()

    def __call__(self):
        return self.model

    def get_response(self, sentence: str) -> str:
        try:
            return self.model.chat(sentence).choices[0].message.content
        except:
            return self.ERROR_MESSAGE

    def get_embedding(self, sentence: str) -> list:
        try:
            return self.model.embeddings(sentence).data[0].embedding
        except:
            return self.ZEROS

    def get_embeddings(self, sentences: t.List[str], request_limit=50) -> t.List[t.List]:
        embeddings = None
        counter = 0
        while embeddings is None and counter < request_limit:
            try:
                items = self.model.embeddings(sentences).data
                embeddings = [item.embedding for item in items]
            except:
                sleep(0.1)
                counter += 1
        if embeddings is not None:
            return embeddings
        return [self.ZEROS for _ in sentences]

    def get_more_embeddings(
        self, 
        sentences: t.List[str], 
        batch_size=100, 
        hide_progress_bar=False,
        parallel=False
        ) -> t.List[t.List]:
        batches = self.make_batches(sentences, size=batch_size)
        if not parallel:
            emb_batches = [self.get_embeddings(batch) for batch in tqdm(batches, disable=hide_progress_bar)]
        else:
            emb_batches = process_map(
                self.get_embeddings, 
                batches, 
                chunksize=1, 
                max_workers=16, 
                disable=hide_progress_bar
                )
        return list(chain.from_iterable(emb_batches))

    @staticmethod
    def make_batches(items: list, size=500) -> t.List[t.List[str]]:
        slices = [(i*size, (i+1)*size) for i in range(len(items) // size + 1)]
        return [items[st:ed] for st, ed in slices]            

    def warmup(self) -> None:
        assert self.get_response('Прогрев') != self.ERROR_MESSAGE, 'Нет доступа к ллм!'
        assert self.get_embedding('Прогрев') != self.ZEROS, 'Нет доступа к ллм!'


class GigaPlusEntryPoint(GigaChatEntryPoint):
    def __init__(self, client_id, client_secret):
        super().__init__(client_id, client_secret)
        self.model = GigaChat(
            credentials=self.creds,
            scope='GIGACHAT_API_CORP',
            verify_ssl_certs=False,
            model='GigaChat-Plus',
            profanity_check=False,
        )
