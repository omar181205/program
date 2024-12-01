def encode_text(text):
    return ''.join(format(ord(char), '08b') for char in text)

def test_encode_text():
     print("Testing encode_text...")
     assert encode_text("A") == "0100001", "Failed: Single character 'A'"
     assert encode_text("Hi") == "0100100001101001", "Failed: Word 'Hi'"
     assert encode_text("") == "", "Failed: Empty string"
     print("Passed:encode_text")
test_encode_text()


def modify_pixel(byte, bit):
    return (byte & ~1) | int(bit)

# # def test_modify_pixel():
    
# #     print("Testing modify_pixel...")
# #     assert modify_pixel(254, '1') == 255, "Failed: Set LSB to 1 (254 -> 255)"
# #     assert modify_pixel(0, '1') == 1, "Failed: Set LSB to 1 (0 -> 1)"
# #     assert modify_pixel(1, '0') == 0, "Failed: Set LSB to 0 (1 -> 0)"
# #     print("Passed: modify_pixel")
# # test_modify_pixel()    

def encode_image(image_path, text):
 
    try:
 
        binary_text = encode_text(text) + encode_text('\x00')
        binary_text_length = len(binary_text)
        try:
            file = open(image_path, "rb")
            image_data = bytearray(file.read())
            file.close()
        except FileNotFoundError:
            print(f"Error: File '{image_path}' not found.")
            return
        pixel_data_start = 54
        if len(image_data) - pixel_data_start < binary_text_length:
            print("Error: The message is too large to encode in the image.")
            return
        for i in range(binary_text_length):
            image_data[pixel_data_start + i] = modify_pixel(image_data[pixel_data_start + i], binary_text[i])
        output_file = image_path.replace(".bmp", "_stego.bmp")
        file = open(output_file, "wb")
        file.write(image_data)
        file.close()

        print(f"Message successfully encoded into '{output_file}'.")

    except Exception as e:
        print(f"An error occurred: {e}")

# def test_encode_image():
#     """
#     Tests the encode_image function.
#     """
#     print("Testing encode_image...")
#     # Create a small test BMP file manually
#     test_image = "test.bmp"
#     test_output = "test_stego.bmp"
#     message = "Test"
    
#     # Create a BMP file with header and pixel data
#     bmp_header = bytearray([0] * 54)  # BMP header (54 bytes)
#     pixel_data = bytearray([0] * 100)  # Pixel data for testing
#     with open(test_image, "wb") as f:
#         f.write(bmp_header + pixel_data)
    
#     # Encode the message into the test BMP file
#     encode_image(test_image, message)
    
#     # Verify the output file exists
#     try:
#         file = open(test_output, "rb")
#         file.close()
#         print("Passed: encode_image")
#     except FileNotFoundError:
#         print("Failed: encode_image (output file not created)")
    
#     # Remove test files manually
#     try:
#         f = open(test_image, "wb")
#         f.close()
#         f = open(test_output, "wb")
#         f.close()
#     except:
#      pass
# test_encode_image()


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




def test_decode_image():
    """
    Tests the decode_image function.
    """
    print("Testing decode_image...")
    # Create a small BMP file with an encoded message
    test_image = "test_stego.bmp"
    message = "Test"
    binary_message = encode_text(message) + encode_text('\x00')
    
    bmp_header = bytearray([0] * 54)  # BMP header
    pixel_data = bytearray([0] * 100)  # Pixel data for testing
    for i, bit in enumerate(binary_message):
        pixel_data[i] = modify_pixel(pixel_data[i], bit)
    
    # Write the test BMP file
    with open(test_image, "wb") as f:
        f.write(bmp_header + pixel_data)
    
    # Decode the message
    decoded_message = decode_image(test_image)
    assert decoded_message == message, f"Failed: decode_image (expected '{message}', got '{decoded_message}')"
    print("Passed: decode_image")
    
    # Remove test file manually
    try:
        f = open(test_image, "wb")
        f.close()
    except:
     pass
test_decode_image()