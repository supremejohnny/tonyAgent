def run(user_request:str):
    state = {
        "user_request": user_request,
        "intent": None,
        "context": None,
        "code_result": None,
        "evaluation": None,
        "final_output": None
    }
    print("Step 1: analyze intent")
    state["intent"] = analyze_intent(state)

    print("Step2: get context")
    state["context"] = get_context(state)

    print("Step 3: draft code")
    state["draft_code"] = draft_code(state)

    print("Step 4: evaluate")
    state["evaluation"] = evaluate(state)

    if state["evaluation"]["valid"]:
        state["final_output"] = state["code_result"]

    return state



def analyze_intent(state):
    pass

def get_context(state):
    pass

def draft_code(state):
    pass

def evaluate(state):
    pass