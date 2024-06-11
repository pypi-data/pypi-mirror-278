import random

def create_dictionary_of_keys():
    max_number = random.randint(150, 300)
    prime_numbers = []
    symbols = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z', 'x', 'c', 'v', 'b', 'n', 'm']

    for i in range(2, max_number):
        z = 0
            
        for j in range(2, i):
            if i % j == 0:
                z = 1
                break

        if z == 0:
            prime_numbers.append(i)
        
    dictionary_of_keys = {"layer 0" : {symbols[0] : random.choice(prime_numbers)}, "layer 1" : {}}
        
    del symbols[0]
    
    layer = 1
    id_previous_layer = 0 # Its function is to select the upstream element that must be added two other elements
    counter = 0 # Its function is to ensure that only two elements are assigned to the upstream element.
    i = 1 # Its function is to ensure that an empty layer is not created

    for symbol in symbols:        
        random_number = random.choice(prime_numbers)
        value_1_upstream = list(dictionary_of_keys[f'layer {id_previous_layer}'].values())[id_previous_layer] 

        dictionary_of_keys[f'layer {layer}'][symbol] = value_1_upstream * random_number

        if len(list(dictionary_of_keys[f'layer {layer}'].values())) == 2 ** layer:
            # a new layer is created
            
            if len(symbols) == i: # prevents an empty layer from being created
                break

            layer += 1
            id_previous_layer = 0
            dictionary_of_keys[f'layer {layer}'] = {}
        else: 
            # checks if the upstream element needs to be changed
            
            if counter == 2:
                id_previous_layer += 1
                counter = 0

            else:
                counter += 1

        i += 1
        
    return dictionary_of_keys

def encode(text: list[str], dictionary_of_keys):
    encode_text = []
    
    for line in text:
        for i in range(len(dictionary_of_keys)):
            layer = dictionary_of_keys[f"layer {i}"]
                
            for key, value in layer.items():
                line = line.replace(key, str(value))

        encode_text.append(line)

    return encode_text

def decode(text: list[str], dictionary_of_keys):
    decode_text = []
    
    for line in text:
        for i in range(len(dictionary_of_keys)):
            layer = dictionary_of_keys[f"layer {i}"]
            # Ordenamos las claves del diccionario por la longitud de sus valores en orden descendente
            sorted_keys = sorted(layer.keys(), key=lambda k: len(str(layer[k])), reverse=True)
                
            for key in sorted_keys:
                value = str(layer[key])
                line = line.replace(value, key)

        decode_text.append(line)

    return decode_text
