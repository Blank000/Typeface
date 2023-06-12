# All Utils functions will be here
import secrets
import random



def generate_invoice_url():
    '''
    Assuming PDF docs are generated using some templates and stored on cloud storage
    Mocking the function to return a random URL
    '''
    return "https://www.typefacestorage/" + secrets.token_hex(6) + ".pdf"

def generate_content():
    '''
    Assuming contents are created and some business logic is in place
    Mocking the function to return a randomly generated feature usage
    '''
    number_of_words_used = random.randint(1, 5)
    number_of_images_used = random.randint(1, 5)
    return (number_of_words_used, number_of_images_used)