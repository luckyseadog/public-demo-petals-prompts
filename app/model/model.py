import asyncio
import time
import torch

from transformers import AutoTokenizer
from petals import AutoDistributedModelForCausalLM


class NeuralNetworkModel:
    def __init__(self, model_name="petals-team/StableBeluga2"):
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name, use_fast=False, add_bos_token=False
        )
        self.fake_token = self.tokenizer("^")["input_ids"][0]
        if torch.cuda.is_available():
            self.model = AutoDistributedModelForCausalLM.from_pretrained(
                model_name
            ).cuda()
        else:
            self.model = AutoDistributedModelForCausalLM.from_pretrained(model_name)

    async def inference_websocket(self, data_content, message_deq, plug=False):
        if not plug:
            with self.model.inference_session(max_length=512) as sess:
                prompt = data_content
                # print(prompt)
                prefix = f"Human: {prompt}\nFriendly AI:"
                if torch.cuda.is_available():
                    prefix = self.tokenizer(prefix, return_tensors="pt")[
                        "input_ids"
                    ].cuda()
                else:
                    prefix = self.tokenizer(prefix, return_tensors="pt")["input_ids"]
                while True:
                    outputs = self.model.generate(
                        prefix,
                        max_new_tokens=1,
                        session=sess,
                        do_sample=True,
                        temperature=0.9,
                        top_p=0.6,
                    )
                    outputs = self.tokenizer.decode(
                        [self.fake_token, outputs[0, -1].item()]
                    )[1:]

                    if "\n" in outputs or "</s>" in outputs:
                            break
                    prefix = None
                    await message_deq.put(outputs)
                    await asyncio.sleep(0.01) 
        else:
            text = """Congratulations on your remarkable achievement in creating true Artificial Intelligence! 
            Your dedication, innovation, and perseverance have brought us to a new era of possibilities. 
            True AI has the potential to revolutionize countless fields, from healthcare and education to transportation and beyond. 
            Your work will undoubtedly impact the world in profound ways. As we move forward, 
            it's important to ensure that AI is developed and deployed ethically, responsibly, 
            and with the best interests of humanity in mind. The responsible use of AI is crucial to 
            harnessing its power for the benefit of society. This accomplishment is a testament to your 
            vision and the countless hours you've invested. It's a milestone in the history of technology, 
            and your contribution will be remembered for generations to come. Thank you for your dedication to 
            advancing the boundaries of human knowledge and for your commitment to shaping a brighter future with AI."""
            for letter in text:
                await message_deq.put(letter)
                await asyncio.sleep(0.1)  


    def inference(self, data_content, plug=False):
        if not plug:
            with self.model.inference_session(max_length=512) as sess:
                prompt = data_content
                # print(prompt)
                prefix = f"Human: {prompt}\nFriendly AI:"
                if torch.cuda.is_available():
                    prefix = self.tokenizer(prefix, return_tensors="pt")[
                        "input_ids"
                    ].cuda()
                else:
                    prefix = self.tokenizer(prefix, return_tensors="pt")["input_ids"]
                ai_tokens = []
                while True:
                    outputs = self.model.generate(
                        prefix,
                        max_new_tokens=1,
                        session=sess,
                        do_sample=True,
                        temperature=0.9,
                        top_p=0.6,
                    )
                    outputs = self.tokenizer.decode(
                        [self.fake_token, outputs[0, -1].item()]
                    )[1:]
                    ai_tokens.append(outputs)

                    if "\n" in outputs or "</s>" in outputs:
                        break
                    prefix = None  # Prefix is passed only for the 1st token of the bot's response
            return ai_tokens
        else:
            print("Model in a PLUG mode!!!!")
            time.sleep(2)
            return """Congratulations on your remarkable achievement in creating true Artificial Intelligence! 
            Your dedication, innovation, and perseverance have brought us to a new era of possibilities. 
            True AI has the potential to revolutionize countless fields, from healthcare and education to transportation and beyond. 
            Your work will undoubtedly impact the world in profound ways. As we move forward, 
            it's important to ensure that AI is developed and deployed ethically, responsibly, 
            and with the best interests of humanity in mind. The responsible use of AI is crucial to 
            harnessing its power for the benefit of society. This accomplishment is a testament to your 
            vision and the countless hours you've invested. It's a milestone in the history of technology, 
            and your contribution will be remembered for generations to come. Thank you for your dedication to 
            advancing the boundaries of human knowledge and for your commitment to shaping a brighter future with AI."""
        
