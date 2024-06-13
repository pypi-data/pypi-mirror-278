import os
import random
import json
import numpy as np
import torch
from torch.utils.data import DataLoader,Dataset
import torch.nn.functional as F
import requests
from nltk import word_tokenize, download
from nltk.stem.porter import PorterStemmer

download('punkt')

if not os.path.exists("stable.pt"):
    f = open("stable.pt","wb")
    resp = requests.get("https://raw.githubusercontent.com/alexjszamora78/recursos/main/stable.pt","wb")
    for i in resp.iter_content(1024*1024):
        f.write(i)
    f.close()

def tokenize_data(text_data:str):
    return word_tokenize(text=text_data, language='spanish')
def stem(word:str):
    stemmer = PorterStemmer()
    return stemmer.stem(word=word.lower())
def bag_of_words(list_text:list, all_words:list) -> np.ndarray:
    words = [stem(word) for word in list_text]
    bag = np.zeros(len(all_words), dtype=np.float32)
    for idx, w in enumerate(all_words):
        if w in words:
            bag[idx] = 1.0
    return bag

class ChatDataset(Dataset):
    def __init__(self, x_data, y_data):
        self.x_data = x_data
        self.y_data = y_data
    def __len__(self):
        return len(self.x_data)
    def __getitem__(self, idx):
        return self.x_data[idx], self.y_data[idx]

class Model(torch.nn.Module):
    def __init__(self, input_size:int, output_size:int):
        super().__init__()
        self.layer_1 = torch.nn.Linear(in_features=input_size, out_features=output_size*3)
        self.layer_2 = torch.nn.Linear(in_features=output_size*3, out_features=output_size*2)
        self.layer_3 = torch.nn.Linear(in_features=output_size*2, out_features=output_size)
    def forward(self, x:torch.Tensor) -> torch.Tensor:
        out = F.relu(self.layer_1(x))
        out = F.relu(self.layer_2(out))
        out = self.layer_3(out)
        return out

class Train:
    def __init__(self,json_file):
        self.model_path:str = 'stable.pt'
        self.model = None
        self.optimizer = None
        self.num_epoch = 200
        self.data:dict = {}
        self.json_file = json_file
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    def _init_optimizer(self, lr_rate:float=0.001) -> torch.optim.Adam:
        return torch.optim.Adam(params=self.model.parameters(), lr=lr_rate)
    def _load_data(self) -> None:
        with open(self.json_file, 'r') as file:
            json_data = json.load(file)
        self.data = json_data
    def _save_model(self, input_size:int, output_size:int, all_words:list, tags:list) -> None:
        data:dict = {
            'input_size': input_size,
            'output_size': output_size,
            'all_words': all_words,
            'tags': tags,
            'model_state': self.model.state_dict()
        }
        torch.save(data, self.model_path)
        print('Saved model...')
    def _dataloader(
                        self, 
                        x_data:torch.Tensor, 
                        y_data:torch.Tensor, 
                        shuffle:bool=False,
                        batch_size:int=64
                    ) -> DataLoader:
        dataset = ChatDataset(x_data=x_data, y_data=y_data)
        return DataLoader(
                            dataset=dataset, 
                            batch_size=batch_size,
                            shuffle=shuffle
                        )
    def _compute_batch_loss(self, x:torch.Tensor, y:torch.Tensor) -> torch.Tensor:
        out = self.model(x).to(self.device)
        loss_func = torch.nn.CrossEntropyLoss()
        loss_g = loss_func(out, y)
        return loss_g
    def _train(self, dataloader:DataLoader):
        print('Iniciando entrenamiento.')
        for epoch in range(1, self.num_epoch):
            for iter, (x, y) in enumerate(dataloader):
                x = x.to(self.device)
                y = y.to(self.device)
                self.optimizer.zero_grad()
                loss_var = self._compute_batch_loss(x=x, y=y)
                loss_var.backward()
                self.optimizer.step()
            if epoch % 10 == 0:
                print(f'Epoch: {epoch}/{self.num_epoch}, loss: {loss_var.item():.4f}')
        print(f'Final loss, loss: {loss_var.item():.4f}')
    def _init(self):
        self._load_data()
        all_words:list = []
        tags:list = []
        x_Y:list = []
        ignore:list = [
                        '?', ':', '.', ',', '!','*', 
                        '–', '—', '’', '“', '”',
                        '¡¡¡', '«', '®', '»', '¿',
                        '!', '%', '(', ')', '*', '+','%'
                    ]
        for intent in self.data:
            tag = intent['tag']
            tags.append(tag)
            for pattern in intent['patterns']:
                word = tokenize_data(text_data=pattern)
                all_words.extend(word)
                x_Y.append((word, tag))
        all_words:list = [
            stem(w) for w in all_words
            if w not in ignore
        ]
        all_words = sorted(set(all_words))
        tags = sorted(set(tags))
        x_train:list = []
        y_train:list = []
        print('Preparando datos')
        for (pattern_list, tag) in x_Y:
            bag = bag_of_words(list_text=pattern_list, all_words=all_words)
            x_train.append(bag)
            label = tags.index(tag)
            y_train.append(label)
        input_size = len(x_train[0])
        output_size = len(tags)
        self.model = Model(input_size=input_size, output_size=output_size)
        print(self.model)
        self.optimizer = self._init_optimizer()
        x_train = np.array(x_train)
        y_train = np.array(y_train)
        dataloader_train = self._dataloader(x_data=x_train, y_data=y_train)
        self._train(dataloader=dataloader_train)
        self._save_model(
                            input_size=input_size, 
                            output_size=output_size, 
                            all_words=all_words,
                            tags=tags
                        )
    def run(self):
        self._init()

def ChatBot(file):
    train = Train(file)
    if not os.path.exists(train.model_path):
        print('Entrenando modelo')
        train.run()
    data = torch.load(train.model_path)
    input_size = data["input_size"]
    output_size = data["output_size"]
    all_words = data['all_words']
    tags = data['tags']
    model_state = data["model_state"]
    train._load_data()
    intents = train.data
    model = Model(input_size=input_size, output_size=output_size).to(train.device)
    model.load_state_dict(model_state)
    model.eval()
    bot_name = "Chatbot"
    while True:
        sentence = input("You: ")
        if sentence == "quit":
            break
        sentence = tokenize_data(sentence)
        X = bag_of_words(sentence, all_words)
        X = X.reshape(1, X.shape[0])
        X = torch.from_numpy(X).to(train.device)
        output = model(X)
        _, predicted = torch.max(output, dim=1)
        tag = tags[predicted.item()]
        probs = torch.softmax(output, dim=1)
        prob = probs[0][predicted.item()]
        if prob.item() > 0.70:
            for intent in intents:
                if tag == intent["tag"]:
                    rpt = random.choice(intent['responses'])
                    print(f"\n{bot_name}: {rpt}\n")
        else:
            print(f"\n{bot_name}: Podrias darme un poco mas de detalles para entender mejor...")