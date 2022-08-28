if __name__ == '__main__':
    try:
        from . import *
        main()
    except ImportError:
        print("Error: Call the chatbot as a module with 'python -m chatbot'...")
