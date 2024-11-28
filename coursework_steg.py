# coursework

def encode_text(text):
    """Encodes text into a binary string."""
    binary_text = ''.join(format(ord(char), '08b') for char in text)
    return binary_text

def modify_pixel(byte, bit):
    """Modifies the least significant bit (LSB) of a byte."""
    if bit == '1':
        return byte | 1  # Set the LSB to 1
    else:
        return byte & ~1  # Set the LSB to 0

def encode_image(image_path, text):
    """Encodes text into a BMP image file."""
    try:
        # Convert the text into binary
        binary_text = encode_text(text)
        binary_text_length = len(binary_text)

        # Open the image file in binary read mode
        with open(image_path, "rb") as file:
            image_data = bytearray(file.read())

        # BMP files store pixel data starting at byte 54 (after the header)
        pixel_data_start = 54
        index = 0

        for i in range(pixel_data_start, len(image_data)):
            if index < binary_text_length:
                # Modify the LSB of each byte to embed the binary message
                image_data[i] = modify_pixel(image_data[i], binary_text[index])
                index += 1
            else:
                break

        # Save the modified image
        output_file = image_path.replace(".bmp", "_stego.bmp")
        with open(output_file, "wb") as file:
            file.write(image_data)

        print(f"Message encoded successfully into {output_file}.")

    except FileNotFoundError:
        print(f"Error: File '{image_path}' not found. Please check the path and try again.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def decode_image(image_path):
    """Decodes text from a BMP image file."""
    try:
        # Open the image file in binary read mode
        with open(image_path, "rb") as file:
            image_data = bytearray(file.read())

        # BMP files store pixel data starting at byte 54
        pixel_data_start = 54

        # Extract binary data from the LSBs of the pixel bytes
        binary_text = ""
        for i in range(pixel_data_start, len(image_data)):
            binary_text += str(image_data[i] & 1)

        # Convert binary data back into text
        decoded_text = ""
        for i in range(0, len(binary_text), 8):
            byte = binary_text[i:i+8]
            decoded_text += chr(int(byte, 2))

            # Stop decoding if null character (end of message) is found
            if decoded_text.endswith('\x00'):
                decoded_text = decoded_text[:-1]  # Remove the null character
                break

        return decoded_text

    except FileNotFoundError:
        print(f"Error: File '{image_path}' not found. Please check the path and try again.")
        return ""
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return ""

if __name__ == "__main__":
    x = input("Choose an option:\n1: Encode\n2: Decode\n")

    if x == "1":
        # Input BMP file path
        image_path = input("Enter the path to your BMP image file (e.g., original_image.bmp): ").strip()

        # Input secret message
        text = input("Enter the secret message you want to encode: ").strip() + "\x00"  # Add a null character to mark the end

        # Encode the message
        encode_image(image_path, text)
    elif x == "2":
        # Input BMP file path for decoding
        image_path = input("Enter the path to the stego BMP image file (e.g., original_image_stego.bmp): ").strip()

        # Decode the message
        decoded_text = decode_image(image_path)
        print(f"Decoded text: {decoded_text}")
    else:
        print("Invalid option. Please choose either 1 or 2.")
