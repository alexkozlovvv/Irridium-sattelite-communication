from datetime import datetime


def generate():
    # Used https://www.lipsum.com/
    message = str(datetime.now()) + " This is testing message for iridium with size of 340 symbols ### Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras non euismod leo, in cursus felis. Morbi porta lobortis nibh a aliquam. In consequat ultrices lectus, ut accumsan magna elementum ac. Nulla orci magna, accumsan sed tincidunt vitae tortor"
    print(message)
    print("MSG_SIZE = ", len(message))
    return message


if __name__ == '__main__':
    generate()
