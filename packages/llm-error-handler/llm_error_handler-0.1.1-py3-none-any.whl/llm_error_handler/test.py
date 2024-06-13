from error_handling import llm_error_handler

@llm_error_handler
def divide(a: int, b: int):
    return a / b

if __name__ == "__main__":
    divide(10, 0)