def encode_text(text): 
    # Converts the text into a string of binary numbers ( there should be 8 bits for each character)
    return ''.join(format(ord(char), '08b') for char in text)

def modify_pixel(byte, bit):
    # Modifies the least significant bit (LSB) of a byte to match the given bit
    return (byte & ~1) | int(bit)

def encode_image(image_path, text):       
    # this is the main function to hide a text message inside a BMP image
    
    try:

        binary_text = encode_text(text) + encode_text('\x00')
        # this variable converts the message to binary and adds a null character at the end as a marker
        binary_text_length = len(binary_text)
        # this variable gets the total length of the binary text

        try:
            file = open(image_path, "rb")
            # Open the image file in binary read mode
            image_data = bytearray(file.read())
            # Read the image data into a modifiable array
            file.close()
            # this variable closes the file after reading the message
        except FileNotFoundError:
            # this is incase the file didnt work
            print(f"Error: File '{image_path}' not found.")
            return
        
        pixel_data_start = 54
        # BMP files have metadata before pixel data, pixel data starts at 54 bytes

        if len(image_data) - pixel_data_start < binary_text_length:
            # Check if the image is large enough to store the message ,incase the hidden text is larger than the pixel data start the code wont run 
            print("Error: The message is too large to encode in the image.")
            return
        
        for i in range(binary_text_length):
            # this variable Loop through each bit of the binary message
            image_data[pixel_data_start + i] = modify_pixel(image_data[pixel_data_start + i], binary_text[i])
            # this variable Modifies the LSB of the image's pixel data to encode the message bit to the message we wrote
        
        output_file = image_path.replace(".bmp", "_stego.bmp")
        # this generates a new filename for the encoded image
        file = open(output_file, "wb")
        #  this opens the new file in binary write mode
        file.write(image_data)
        # Write the modified image data to the new file
        file.close()
        # Close the new file after writing

        print(f"Message successfully encoded into '{output_file}'.")
        # Notify the user that the encoding was successful

    except Exception as e:
        # Catch any other errors and display a message if needed
        print(f"An error occurred: {e}")

def decode_image(image_path):
    # Main function to retrieve a hidden text message from a BMP image
    
    try:
        # Try block to handle any unexpected errors

        try:
            file = open(image_path, "rb")
            # Open the image file in binary read mode
            image_data = bytearray(file.read())
            # Read the image data into a modifiable array
            file.close()
            # Close the file after reading
        except FileNotFoundError:
            # incase there was an error or the file doesn't exist
            print(f"Error: File '{image_path}' not found.")
            return ""
        
        pixel_data_start = 54
        # BMP files have metadata before pixel data; pixel data starts at byte 54

        binary_text = ''.join(str(image_data[i] & 1) for i in range(pixel_data_start, len(image_data)))
        # Extract the LSB of each byte in the pixel data to retrieve the binary message

        decoded_text = ""
        # set an empty string for the decoded text

        for i in range(0, len(binary_text), 8):
            # Loop through the binary message 8 bits (1 byte) at a time
            byte = binary_text[i:i+8]
            # Extract one byte (8 bits) of binary data
            if len(byte) < 8:
                break
                # Stop if there aren't enough bits for a full byte
            char = chr(int(byte, 2))
            # Convert the binary byte to a character
            if char == '\x00': 
                break
                # Stop if the null character is encountered
            decoded_text += char
            # Add the character to the decoded text

        return decoded_text
        # Return the decoded message

    except Exception as e:
        # Catch any other errors and display a message
        print(f"An error occurred: {e}")
        return ""

def main():
    # Main function to interact with the user
    print("Welcome to the bmp Steganography Tool!")
    # Greet the user
    print("1. Encode a message into an image")
    print("2. Decode a message from an image")
    # Display menu options to the user
    choice = input("Enter your choice (1 or 2): ")
    # Prompt the user to choose an option

    if choice == "1":
        # If the user chooses to encode a message
        image_path = input("Enter the path of the bmp image to encode: ")
        # Ask for the image file path
        text = input("Enter the message to encode: ")
        # Ask for the message to hide
        encode_image(image_path, text)
        # Call the function to encode the message
    elif choice == "2":
        # If the user chooses to decode a message
        image_path = input("Enter the path of the BMP image to decode: ")
        # Ask for the image file path
        decoded_message = decode_image(image_path)
        # Call the function to decode the message
        if decoded_message:
            # If a message is successfully decoded
            print("Decoded message:", decoded_message)
            # Display the message
        else:
            # If no message is found or an error occurs
            print("No message found or an error occurred.")
    else:
        # If the user enters an invalid choice
        print("Invalid choice. Please run the program again.")

if __name__ == "__main__":
    main()
    # Run the main function if the script is executed directly
