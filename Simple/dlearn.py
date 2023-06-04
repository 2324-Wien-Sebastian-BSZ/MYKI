import numpy as np
from tensorflow.keras.layers import Embedding
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, LSTM, Dense


# Datensatz mit Begrüßungen und dazugehörigen Antworten
# greetings = ['Hallo', 'Hi', 'Guten Tag', 'Guten Morgen', 'Guten Abend']
# responses = ['Hallo!', 'Hi!', 'Guten Tag!', 'Guten Morgen!', 'Guten Abend!']
greetings = [
    'Hallo',
    'Hi',
    'Guten Tag',
    'Guten Morgen',
    'Guten Abend',
    'Wie geht es dir?',
    'Schönen Tag noch',
    'Servus',
    'Moin',
    'Grüß Gott',
    'Hey',
    'Hallo zusammen',
    'Na, wie geht es?',
    'Schön dich zu sehen',
    'Wie steht\'s?',
]

responses = [
    'Hallo!',
    'Hi!',
    'Guten Tag!',
    'Guten Morgen!',
    'Guten Abend!',
    'Mir geht es gut, danke!',
    'Ebenfalls einen schönen Tag!',
    'Servus!',
    'Moin!',
    'Grüß Gott!',
    'Hey!',
    'Hallo zusammen!',
    'Mir geht es gut, danke!',
    'Schön dich zu sehen!',
    'Alles bestens!',
]



# Vokabular erstellen
vocab = set(['<start>', '<end>'])
for greeting in greetings:
    vocab.update(greeting.lower().split())
for response in responses:
    vocab.update(response.lower().split())

# Vokabular erstellen
# vocab = set()
# for greeting in greetings:
#     vocab.update(greeting.lower().split())
# for response in responses:
#     vocab.update(response.lower().split())

# Wörter zu Indizes und Indizes zu Wörtern abbilden
word2idx = {word: idx + 1 for idx, word in enumerate(vocab)}
idx2word = {idx: word for word, idx in word2idx.items()}

# Maximale Länge der Eingabe- und Ausgabesequenzen bestimmen
max_input_length = max(len(greeting.lower().split()) for greeting in greetings)
max_output_length = max(len(response.lower().split()) for response in responses)

# Eingabe- und Ausgabesequenzen erstellen
encoder_input_data = np.zeros((len(greetings), max_input_length), dtype='float32')
decoder_input_data = np.zeros((len(greetings), max_output_length), dtype='float32')
decoder_target_data = np.zeros((len(greetings), max_output_length, len(vocab) + 1), dtype='float32')

for i, (greeting, response) in enumerate(zip(greetings, responses)):
    for t, word in enumerate(greeting.lower().split()):
        encoder_input_data[i, t] = word2idx[word]
    for t, word in enumerate(response.lower().split()):
        decoder_input_data[i, t] = word2idx[word]
        if t > 0:
            decoder_target_data[i, t - 1, word2idx[word]] = 1.0

# Hyperparameter
latent_dim = 256

# Encoder
encoder_inputs = Input(shape=(None,))
encoder_embedding = Embedding(len(vocab) + 1, latent_dim)(encoder_inputs)
encoder_lstm = LSTM(latent_dim, return_state=True)
encoder_outputs, state_h, state_c = encoder_lstm(encoder_embedding)
encoder_states = [state_h, state_c]

# Decoder
decoder_inputs = Input(shape=(None,))
decoder_embedding = Embedding(len(vocab) + 1, latent_dim)(decoder_inputs)
decoder_lstm = LSTM(latent_dim, return_sequences=True, return_state=True)
decoder_outputs, _, _ = decoder_lstm(decoder_embedding, initial_state=encoder_states)
decoder_dense = Dense(len(vocab) + 1, activation='softmax')
decoder_outputs = decoder_dense(decoder_outputs)

# Modell erstellen
model = Model([encoder_inputs, decoder_inputs], decoder_outputs)
model.compile(optimizer='rmsprop', loss='categorical_crossentropy')

# Modell trainieren
model.fit([encoder_input_data, decoder_input_data], decoder_target_data, batch_size=1, epochs=50)

# Funktion zum Generieren einer Antwort
def generate_response(input_text):
    input_seq = np.zeros((1, max_input_length), dtype='float32')
    for t, word in enumerate(input_text.lower().split()):
        input_seq[0, t] = word2idx[word]
    states_value = encoder_model.predict(input_seq)
    target_seq = np.zeros((1, 1), dtype='float32')
    target_seq[0, 0] = word2idx['<start>']
    stop_condition = False
    generated_response = ''
    while not stop_condition:
        output_tokens, h, c = decoder_model.predict([target_seq] + states_value)
        sampled_token_index = np.argmax(output_tokens[0, -1, :])
        sampled_word = idx2word[sampled_token_index]
        generated_response += ' ' + sampled_word
        if sampled_word == '<end>' or len(generated_response.split()) > max_output_length:
            stop_condition = True
        target_seq = np.zeros((1, 1))
        target_seq[0, 0] = sampled_token_index
        states_value = [h, c]
    return generated_response

# Encoder-Modell erstellen
encoder_model = Model(encoder_inputs, encoder_states)

# Decoder-Modell erstellen
decoder_state_input_h = Input(shape=(latent_dim,))
decoder_state_input_c = Input(shape=(latent_dim,))
decoder_states_inputs = [decoder_state_input_h, decoder_state_input_c]
decoder_outputs, state_h, state_c = decoder_lstm(decoder_embedding, initial_state=decoder_states_inputs)
decoder_states = [state_h, state_c]
decoder_outputs = decoder_dense(decoder_outputs)
decoder_model = Model([decoder_inputs] + decoder_states_inputs, [decoder_outputs] + decoder_states)

# Beispielinteraktion
input_text = 'Hallo'
response = generate_response(input_text)
print('Eingabe:', input_text)
print('Antwort:', response)
