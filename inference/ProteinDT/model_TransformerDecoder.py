import torch.nn as nn
from transformers import T5ForConditionalGeneration, T5Config
from transformers.modeling_outputs import BaseModelOutput
import torch
from transformers import BertModel, BertTokenizer

class T5Decoder(nn.Module):
    def __init__(self, hidden_dim, tokenizer, T5_model):
        super().__init__()
        self.num_classes = tokenizer.vocab_size

        if T5_model == "ProtT5":
            self.config = T5Config.from_pretrained("Rostlab/prot_t5_xl_uniref50", chache_dir="../data/temp_pretrained_prot_t5_xl_uniref50")
            self.T5_model = T5ForConditionalGeneration.from_pretrained("Rostlab/prot_t5_xl_uniref50")

        elif T5_model == "T5Base":
            self.config = T5Config.from_pretrained(
                "t5-base",
                chache_dir="../data/temp_t5",
                vocab_size=self.num_classes,
            )
            self.T5_model = T5ForConditionalGeneration(self.config)

        self.rep_linear = nn.Linear(hidden_dim, self.config.d_model)
        self.tokenizer = tokenizer
        return
    
    def forward(self, protein_seq_input_ids, protein_seq_attention_mask, condition):
        condition = condition.unsqueeze(1)
        if condition.size(2) != self.config.d_model:
            condition = self.rep_linear(condition)  # (B, 1, d_model)

        labels = protein_seq_input_ids  # (B, d_model)
        labels[labels == self.tokenizer.pad_token_id] = -100
        
        model_outputs = self.T5_model(encoder_outputs=(condition, ), labels=labels)
        loss = model_outputs.loss
        return loss, 0

    def inference(
        self, condition, max_seq_len, protein_seq_attention_mask,
        temperature=1.0, k=40, p=0.9, repetition_penalty=1.0, num_return_sequences=1,
        do_sample=True, num_beams=1
    ):
        if condition.dim() == 2:
            condition = condition.unsqueeze(1).float()  # (B, 1, hidden_dim)
        if condition.size(2) != self.config.d_model:
            condition = self.rep_linear(condition)

        enccoder_outputs = BaseModelOutput(last_hidden_state=condition)
        #print(enccoder_outputs.shape)
        #print(enccoder_outputs.size)
        output_ids = self.T5_model.generate(
            encoder_outputs=enccoder_outputs, 

            max_length=max_seq_len,
            temperature=temperature,
            top_k=k,
            top_p=p,
            repetition_penalty=repetition_penalty,
            num_beams=num_beams,
            do_sample=do_sample,
            num_return_sequences=num_return_sequences,
        )     
        return output_ids

    def mutate(self, condition, original_ids, masked_positions, max_seq_len,
               temperature=1.0, k=40, p=0.9, repetition_penalty=1.0, num_return_sequences=1,
               do_sample=True, num_beams=1):
        if condition.dim() == 2:
            condition = condition.unsqueeze(1).float()  # (B, 1, hidden_dim)
        if condition.size(2) != self.config.d_model:
            condition = self.rep_linear(condition)

        t5_input_ids = original_ids
        masked_positions = masked_positions[:, 1:]
        encoder_outputs = BaseModelOutput(last_hidden_state=condition)

        def tokens_to_allow_fn(batch_id, input_ids):
            # Only allow the original token at each position unless it's a masked position
            if input_ids.shape[-1] <= masked_positions.shape[-1]:
                if masked_positions[batch_id, input_ids.shape[-1]-1]:
                    return list(range(self.tokenizer.vocab_size))  # Allow all tokens if it's a masked position
                else:
                    return [t5_input_ids[batch_id, input_ids.shape[-1]-1].item()]  # Force the original token at this position
            return list(range(self.tokenizer.vocab_size))

        output_ids = self.T5_model.generate(
            input_ids=t5_input_ids,
            encoder_outputs=encoder_outputs,
            max_length=max_seq_len,
            temperature=temperature,
            top_k=k,
            top_p=p,
            repetition_penalty=repetition_penalty,
            num_beams=num_beams,
            do_sample=do_sample,
            num_return_sequences=num_return_sequences,
            prefix_allowed_tokens_fn=tokens_to_allow_fn,
            use_cache=True
        )

        return output_ids