import pytesseract
import pyautogui
import time
import keyboard

from PIL import Image, ImageGrab

required_sentence = "The first to" # Question to look for (decides whether the logic for responding should run)
dirty_desired_phrase = ""
clean_desired_phrase = ""

while (True):
    time.sleep(2)
    
    
    screenshot = ImageGrab.grab(bbox=(0,550,700,1080)) ## Screenshots certain area of the screen
    screenshot.save("chat_screenshot.png") # Saves created screenshot as a file (.png)

    image = Image.open("chat_screenshot.png") # Opens the screenshoted image
    text = pytesseract.image_to_string(image) # Converts all text from image to string
    
    '''
    # TESTING START
    testing_image = Image.open("test_type.png")
    testing_text = pytesseract.image_to_string(testing_image)
    # TESTING END
    '''

    temp = -1 # Variable that counts the loop number of the array with sentence words (used for getting the desired phrase)

    if (required_sentence in text): # If the required sentence appears in the Minecraft chat
        actual_words = [text.split(" ")] # Splits the sentence we got from the screenshot into array of separated words
        
        for word in actual_words[0]: # Since it created an array within array (array with words is within another array), we need to access the actual array with words inside that outer array
            temp = temp+1 # Increase the variable each loop
            if("wins!" in word): # If the loops comes to "wins!" word, it will then lookup for the word with index lower by 1 (or more in case of multiple words) where the DESIRED PHRASE is located
                dirty_desired_phrase = (actual_words[0][temp-1]) # Gets the DESIRED PHRASE
                if ("‘" in dirty_desired_phrase and "’" in dirty_desired_phrase): # Checks if the word has both "‘" and "’" - if so, it's only 1 WORD phrase
                    break # breaks out of the loop, since we don't need the rest anymore
                elif ("‘" not in dirty_desired_phrase): # In case it's not only 1 WORD (which means it won't have both "‘" and "’")
                    dirty_desired_phrase = (actual_words[0][temp-2]) + " " + dirty_desired_phrase # We get a word before this one as well and add it to the PHRASE
                    if ("‘" in dirty_desired_phrase and "’" in dirty_desired_phrase): # If the PHRASE have both "‘" and "’" - it is 2 WORD PHRASE
                        break # breaks out of the loop, since we don't need the rest anymore
                    elif ("‘" not in dirty_desired_phrase): # If the PHRASE still don't have both "‘" and "’"
                        dirty_desired_phrase = (actual_words[0][temp-3]) + " " + dirty_desired_phrase # We get another word before that and add it to the PHRASE
                        if ("‘" in dirty_desired_phrase and "’" in dirty_desired_phrase): # If the PHRASE now have both "‘" and "’" - it is 3 WORD PHRASE
                            break # breaks out of the loop, since we don't need the rest anymore
                        elif ("‘" not in dirty_desired_phrase): # If the PHRASE still don't have both "‘" and "’"
                            dirty_desired_phrase = (actual_words[0][temp-4]) + " " + dirty_desired_phrase # We get another word before that and add it to the PHRASE (this is a limit of this program, if it is 4 WORDS PHRASE, it will be fine, if more, then it will not be correct)
                            break # breaks out of the loop, since we don't need the rest anymore
            
    else:
        print("NO QUESTION DETECTED")
    
    
    if (dirty_desired_phrase != ""):
        # Removes the "‘" and "’" from the desired word (Minecraft puts it there)
        clean_desired_phrase = dirty_desired_phrase.replace("‘", "")
        clean_desired_phrase = clean_desired_phrase.replace("’", "")
        clean_desired_phrase = clean_desired_phrase.replace("'", "")

        # Prints that it found the question
        print("Minecraft question detected!")
        print("Question: The first to type " + dirty_desired_phrase + " wins!")
        print("DESIRED WORD: " + clean_desired_phrase)

        # Disables keyboard input for a moment (to prevent typing some other shajt when we are for example walking or stuff)
        for i in range(150):
            keyboard.block_key(i)

        pyautogui.press("enter") # Presses ENTER on our keyboard (open a chat)
        pyautogui.write(clean_desired_phrase) # Types the DESIRED word
        pyautogui.press("enter") # Presses ENTER again to send that DESIRED word to MC chat
        
    if (dirty_desired_phrase != ""): # It stops the whole program (exits the While loop) once it successfully prints the DESIRED PHRASE
        break
            