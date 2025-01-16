from collections import defaultdict
import re

def bpe_tokenizer(text, target_vocab_size=5000):
    def get_vocab(data):
        vocab = defaultdict(int)
        for line in data.splitlines():
            for word in line.split():
                vocab[' '.join(list(word)) + ' </w>'] += 1
        return vocab

    def get_stats(vocab):
        pairs = defaultdict(int)
        for word, freq in vocab.items():
            symbols = word.split()
            for i in range(len(symbols) - 1):
                pairs[symbols[i], symbols[i + 1]] += freq
        return pairs

    def merge_vocab(pair, v_in):
        v_out = {}
        bigram = re.escape(' '.join(pair))
        p = re.compile(r'(?<!\S)' + bigram + r'(?!\S)')
        for word in v_in:
            w_out = p.sub(''.join(pair), word)
            v_out[w_out] = v_in[word]
        return v_out

    def calculate_compression_ratio(corpus, vocab):
        original_length = sum(len(sentence) for sentence in corpus.splitlines())
        tokenized_length = sum(len(word.split()) for word in vocab.keys())
        return round(original_length / tokenized_length, 3)

    # Process the text
    vocab = get_vocab(text)
    vocab_size = len(vocab)

    while vocab_size < target_vocab_size:
        pairs = get_stats(vocab)
        if not pairs:
            break
        most_frequent_pair = max(pairs, key=pairs.get)
        vocab = merge_vocab(most_frequent_pair, vocab)
        vocab_size = len(vocab)

    compression_ratio = calculate_compression_ratio(text, vocab)
    tokens = list(vocab.keys())

    return tokens, vocab, compression_ratio

# Example usage
if __name__ == "__main__":
    sample_text = "ರಾಮಾಯಣ ಹಿಂದೂಗಳ ಪವಿತ್ರ ಗ್ರಂಥಗಳಲ್ಲಿ"
    tokens, vocab, compression_ratio = bpe_tokenizer(sample_text)
    print("\nFinal Vocabulary:", vocab)
    print("---------")
    print("Vocabulary Size:", len(vocab))
    print("---------")
    print("Compression Ratio:", compression_ratio)
    print("Tokens:", tokens)
