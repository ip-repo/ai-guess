import socket
import json
import sys
import signal
import helpers

class Guess:
    """
    A class to manage and initialize a guessing operation with a specific ticket and model.

    Args:
        ticket (str): The unique identifier or credential for the operation.
        model (str): The model to be used for processing or analysis.
        host (str, optional): The hostname or IP address of the server. Defaults to 'localhost'.
        port (int, optional): The port number to connect to the server. Defaults to 11434.

    Attributes:
        host (str): The hostname or IP address of the server.
        port (int): The port number to connect to the server.
        ticket (str): The unique identifier or credential for the operation.
        sig: Signal handler for interrupt signals (e.g., SIGINT).
    """
    def __init__(self, ticket: str, model :str, host: str='localhost', port: int=11434) -> None:
        self.host = host
        self.port = port
        self.ticket = ticket
        self.sig = signal.signal(signal.SIGINT, helpers.signal_handler)
        self.parse_ticket()
        self.prepare_request_data()

    def prepare_request_data(self):
        """
        Prepares the data and constructs an HTTP POST request for a chat API.
            - Reads the system message from the `sys_message.txt` file in the "info" directory.
            - Reads the model name from the `model.txt` file in the "info" directory.
            - Formats the retrieved data into a JSON structure containing:
                - The model name.
                - A system message.
                - A user message including parsed ticket information.
                - A flag for streaming responses.
            - Converts the JSON data into a string format.
            - Constructs an HTTP POST request with appropriate headers, the data's length, and the JSON payload.
            - Sends the constructed HTTP request to the API via the `ollama_request` method.

        Args:
            None

        Returns:
            None
        """
        
        SYSTEM_MESSAGE = open(f"{self.install_directory}info\\sys_message.txt","r").read().strip()
        MODEL = open(f"{self.install_directory}info\\model.txt","r").read().strip()
        data = {
            "model": f"{MODEL}",
            "messages": [
                {
                    "role": "system",
                    "content": f"{SYSTEM_MESSAGE}"
                },
                {
                    "role": "user",
                    "content": f"file info: {self.ticket_parsed}"
                }
            ],
            "stream": True
        }
        data_json = json.dumps(data)

        # Create the POST request
        request = (
            "POST /api/chat HTTP/1.1\r\n"
            "Host: {}\r\n"
            "Content-Type: application/json\r\n"
            "Content-Length: {}\r\n"
            "\r\n"
            "{}"
        ).format(self.host, len(data_json), data_json)
        self.ollama_request(request)
    
    def ollama_request(self, request):
        """
        Sends a request to a specified host and port using a TCP socket connection,
        receives a JSON response, and processes the message content. Handles any 
        potential exceptions that may occur during the communication process.
        Print the cumulative message content extracted from the server's response.

        Parameters:
        - request : The request message to be sent to the server.
        """
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.connect((self.host, self.port))
            client_socket.send(request.encode())
            res = ""
            try:
                print("#" *helpers.get_terminal_width())
                while True:
                    response = client_socket.recv(4096)
                    if not response:
                        break

                    response = response.decode()
                    if "HTTP/1.1 200 OK" in response:
                        continue

                    response_lines = response.split('\r\n')[1]
                    json_str = response_lines
                    response_dict = json.loads(json_str)
                    res  += response_dict["message"]["content"]
                    print(response_dict["message"]["content"])

                    if response_dict["done"]:
                        
                        break
            finally:

                print("#" *helpers.get_terminal_width())
                client_socket.close()

        except Exception as e:
            print("#" *helpers.get_terminal_width())
            print(f"An error occurred: {e}")
            print("#" *helpers.get_terminal_width())
            client_socket.close()
       
    def parse_ticket(self) ->None:
        """
        Parses the ticket string into a structured dictionary and formats its contents for display.
        - Splits the ticket string into components using the "|" delimiter.
        - Creates a dictionary (`d`) to map the parsed data into key-value pairs, including:
            - Path: The file path.
            - File Type: The type of the file (e.g., directory, regular file).
            - File Size(bytes): The size of the file in bytes.
            - Mode: The file's permissions or mode.
            - Last Modified: The formatted last modification time (combines two ticket components).
        - Determines the installation directory based on the ticket data.
        - Prints the parsed ticket data, surrounded by a visual separator.
        - Stores the structured ticket data in `self.ticket` and generates a formatted string
        representation in `self.ticket_parsed`.

        Args:
            None

        Returns:
            None
        """
        self.ticket = self.ticket.split("|")
        d = {"Path" : self.ticket[1],
            "File Type" : self.ticket[2],
            "File Size(bytes)" : self.ticket[3],
            "Mode" : self.ticket[4],
            "Last Modified" : self.ticket[6] + "-" + self.ticket[5],

            
        }
        self.install_directory = "\\\\".join(self.ticket[7].split("\\")[:-2]) + "\\\\"
       
        print("#" *helpers.get_terminal_width())
        self.ticket = d
        self.ticket_parsed = ""
        for key in self.ticket.keys():
            print(f"{key}: {self.ticket[key]}")
            self.ticket_parsed +=f"{key}: {self.ticket[key]}" + "\n"
        print("#" *helpers.get_terminal_width())
       
    

if __name__ == "__main__":
    print("#" *helpers.get_terminal_width())
    guess_obj = Guess(ticket=sys.argv[1], model="llama3.2:1b")
    print("#" *helpers.get_terminal_width())
   
