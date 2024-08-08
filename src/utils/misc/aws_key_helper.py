def decode_aws_keys(encoded_access_key: str, encoded_secret_key: str) -> tuple:

    def custom_decode(input_str):
        decoded_chars = []
        for i, char in enumerate(input_str):
            key_c = chr((ord(char) - (i % 7) - 4) % 256)
            decoded_chars.append(key_c)
        return ''.join(decoded_chars)

    decoded_access_key = custom_decode(encoded_access_key)
    decoded_secret_key = custom_decode(encoded_secret_key)

    return decoded_access_key, decoded_secret_key