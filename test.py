def encode_text(text):  # Defines a function to convert text into binary.
    """Encodes text into a binary string."""  # Explains what the function does.
    binary_text = ''.join(format(ord(char), '08b') for char in text)  # Converts each character into an 8-bit binary string and joins them together.
    return binary_text  # Returns the binary representation of the text.


def modify_pixel(byte, bit):  # Defines a function to modify the least significant bit (LSB) of a byte.
    """Modifies the least significant bit (LSB) of a byte."""  # Explains the function's purpose.
    if bit == '1':  # Checks if the bit to be embedded is '1'.
        return byte | 1  # Sets the LSB to 1 using a bitwise OR operation.
    else:  # If the bit to embed is '0':
        return byte & ~1  # Clears the LSB (sets it to 0) using a bitwise AND with the complement of 1.


def encode_image(image_path, text):  # Defines a function to encode a message into a BMP image file.
    """Encodes text into a BMP image file."""  # Explains the function's purpose.
    try:  # Starts a try block to handle errors.
        # Convert the text into binary
        binary_text = encode_text(text)  # Converts the input text into binary format.
        binary_text_length = len(binary_text)  # Calculates and stores the length of the binary string.

        # Open the image file in binary read mode
        with open(image_path, "rb") as file:  # Opens the BMP file in binary read mode.
            image_data = bytearray(file.read())  # Reads the file and stores it as a modifiable bytearray.

        # BMP files store pixel data starting at byte 54 (after the header)
        pixel_data_start = 54  # The pixel data starts at byte 54 in a BMP file.
        index = 0  # Initializes a counter to track the position in the binary text.

        for i in range(pixel_data_start, len(image_data)):  # Loops through the pixel data starting from byte 54.
            if index < binary_text_length:  # Ensures there’s still binary data to embed.
                # Modify the LSB of each byte to embed the binary message
                image_data[i] = modify_pixel(image_data[i], binary_text[index])  # Embeds the current bit in the LSB of the current byte.
                index += 1  # Moves to the next bit in the binary text.
            else:  # Stops the loop if all binary data has been embedded.
                break

        # Save the modified image
        output_file = image_path.replace(".bmp", "_stego.bmp")  # Creates a new filename by appending "_stego" to the original.
        with open(output_file, "wb") as file:  # Opens the new file in binary write mode.
            file.write(image_data)  # Writes the modified data to the new file.

        print(f"Message encoded successfully into {output_file}.")  # Displays a success message with the output file name.

    except FileNotFoundError:  # Handles the error if the specified file is not found.
        print(f"Error: File '{image_path}' not found. Please check the path and try again.")  # Displays an error message for missing files.
    except Exception as e:  # Handles any other unexpected errors.
        print(f"An unexpected error occurred: {e}")  # Displays the error details.
