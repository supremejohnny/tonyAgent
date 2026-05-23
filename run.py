def run(user_request:str):
    state = {
        "user_request": user_request,     # original/raw user prompt or input
        "intent": None,                   # the model's guess of user's intent through the prompt
        "context": None,                  # any required context, including texts, codes, directory ect.
        "draft_code": None,               # the first code writing, after model finishes coding, it stores here temporarily
        "evaluation": None,               # evaluate if code is 'valid', the reason and valiadity is stored
        "final_output": None,             # the FINAL output presents to user
        "status": "running",                   # current work state, running/success/failed etc.
        "retry_count": 0              # how many times have retried, avoiding endless retry
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
        state["final_output"] = state["draft_code"]
        state["status"] = "success"
    else:
        state["status"] = "failed"
        # retry logic

    return state



def analyze_intent(state):
    pass

def get_context(state):
    pass

def draft_code(state):
    pass

def evaluate(state):
    pass