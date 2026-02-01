import spacy
import speech_recognition as sr
import pyttsx3


def text_to_speech(text):
    """
    Convert text to speech.
    """
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def speech_to_text():
    """
    Convert speech to text using the microphone.
    """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening... Please speak your query.")
        text_to_speech("Listening... Please speak your query.")

        try:
            audio = recognizer.listen(source, timeout=5)
            query = recognizer.recognize_google(audio)
            print(f"You said: {query}")
            return query

        except sr.UnknownValueError:
            text_to_speech("Sorry, I did not understand that.")
            return None

        except sr.RequestError:
            text_to_speech(
                "Sorry, there was an issue with the speech recognition service."
            )
            return None

        except sr.WaitTimeoutError:
            text_to_speech("No input detected. Please try again.")
            return None


def extract_locations(query, node_names):
    """
    Extract starting and ending locations from the user's natural language query.
    """
    nlp = spacy.load("en_core_web_sm")
    extracted_locations = []

    # Match node names in the query
    for name in node_names.values():
        if name.lower() in query.lower():
            extracted_locations.append(name)

    # Extract start and end locations
    if len(extracted_locations) >= 2:
        start, end = extracted_locations[:2]  # First two locations
        start_key = next(
            key for key, value in node_names.items()
            if value.lower() == start.lower()
        )
        end_key = next(
            key for key, value in node_names.items()
            if value.lower() == end.lower()
        )
        return start_key, end_key

    return None, None


def find_all_paths(graph, start, end, path=[]):
    """
    Find all paths from the start node to the end node in a graph.
    """
    path = path + [start]

    if start == end:
        return [path]

    if start not in graph:
        return []

    paths = []
    for node in graph[start]:
        if node not in path:
            new_paths = find_all_paths(graph, node, end, path)
            for p in new_paths:
                paths.append(p)

    return paths


def print_all_paths(start, end, graph, node_names):
    paths = find_all_paths(graph, start, end)

    if not paths:
        message = "No path found."
        print(message)
        text_to_speech(message)
        return

    for i, path in enumerate(paths, start=1):
        readable_path = " -> ".join(node_names[node] for node in path)
        print(f"Path {i}: {readable_path}")
        text_to_speech(f"Path {i}: {readable_path}")


def main():
    graph = {
        "A": {"B": 2, "C": 3},
        "B": {"A": 2, "E": 1},
        "C": {"A": 3, "M": 5},
        "D": {"E": 6, "W": 3},
        "E": {"B": 1, "D": 6, "F": 2, "G": 2},
        "F": {"E": 2, "H": 3, "I": 5, "J": 4, "K": 6, "L": 2},
        "G": {"E": 2},
        "H": {"F": 3},
        "I": {"F": 5},
        "J": {"F": 4},
        "K": {"F": 6},
        "L": {"F": 2},
        "M": {"C": 5, "N": 2},
        "N": {"M": 2, "O": 3},
        "O": {"N": 3, "P": 2},
        "P": {"O": 2, "Q": 4},
        "Q": {"P": 4, "R": 3, "S": 5, "T": 6},
        "R": {"Q": 3},
        "S": {"Q": 5},
        "T": {"Q": 6, "U": 4},
        "U": {"T": 4, "V": 3},
        "V": {"U": 3},
        "W": {"D": 3, "X": 2},
        "X": {"W": 2},
    }

    node_names = {
        "A": "Main gate",
        "B": "Tuck Shop",
        "C": "Tennis Court",
        "D": "LC Lawn",
        "E": "Parking Area 1",
        "F": "Hostel Area",
        "G": "Student Affairs Office",
        "H": "FM Radio Room",
        "I": "Law Department",
        "J": "Computer Arts Department",
        "K": "Susan B Reading Room",
        "L": "Educational Department",
        "M": "Admission Block",
        "N": "Admission Offices",
        "O": "Cafeteria",
        "P": "Gate 5",
        "Q": "Sports & Gym Block",
        "R": "Science Block",
        "S": "CS Department",
        "T": "IT Department",
        "U": "Masjid",
        "V": "Library",
        "W": "Auditorium",
        "X": "Girls Hostel",
    }

    query = speech_to_text()
    if not query:
        return

    start, end = extract_locations(query, node_names)
    if not start or not end:
        message = "Could not understand the locations. Please try again."
        print(message)
        text_to_speech(message)
        return

    print_all_paths(start, end, graph, node_names)


if __name__ == "__main__":
    main()
