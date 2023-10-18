from transformers import AutoTokenizer
from petals import AutoDistributedModelForCausalLM

class NeuralNetworkModel:
    def __init__(self, model_name="petals-team/StableBeluga2"):
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name, use_fast=False, add_bos_token=False
        )
        self.model = AutoDistributedModelForCausalLM.from_pretrained(model_name)
        self.fake_token = self.tokenizer("^")["input_ids"][0]
    
    def inference(self, data_content):
        with self.model.inference_session(max_length=512) as sess:
            prompt = data_content
            print(prompt)
            prefix = f"Human: {prompt}\nFriendly AI:"
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
                outputs = self.tokenizer.decode([self.fake_token, outputs[0, -1].item()])[1:]
                ai_tokens.append(outputs)

                if "\n" in outputs or "</s>" in outputs:
                    break
                prefix = (
                    None  # Prefix is passed only for the 1st token of the bot's response
                )
        return ai_tokens