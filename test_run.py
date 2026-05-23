PROMPT = "请帮我写一个计算器的python软件"


def llm_call(step, prompt, state=None):
    state = state or {}

    if step == "analyze_intent":
        if prompt == "请帮我写一个计算器的python软件":
            return {
                "summary": "用户想要一个 Python 计算器程序",
                "task_type": "code_generation",
                "goal": "生成一个可运行的计算器脚本",
                "constraints": ["使用 Python", "包含基本加减乘除功能"],
            }
        return {
            "summary": "无法识别的请求",
            "task_type": "unknown",
            "goal": "需要更多信息",
            "constraints": [],
        }

    if step == "get_context":
        intent = state.get("intent", {})
        if intent.get("task_type") == "code_generation":
            return {
                "existing_logic": "当前工作区没有已有代码，需要从零开始。",
                "tool_manifest": [
                    {"name": "python_runner", "description": "运行 Python 代码"},
                    {"name": "pytest", "description": "执行测试"},
                ],
                "notes": "先生成草稿代码，再做评估。",
            }
        return {
            "existing_logic": "没有足够上下文。",
            "tool_manifest": [],
            "notes": "无法继续生成代码。",
        }

    if step == "draft_code":
        retry_count = state.get("retry_count", 0)
        if prompt == "请帮我写一个计算器的python软件" and retry_count == 0:
            return """def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b
"""

        if prompt == "请帮我写一个计算器的python软件" and retry_count >= 1:
            return """def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise ValueError("cannot divide by zero")
    return a / b
"""

        return "# no code generated"

    if step == "evaluate":
        draft_code = state.get("draft_code", "")

        if "def divide" not in draft_code:
            return {
                "valid": False,
                "reason": "代码缺少 divide 方法，未满足基本加减乘除要求。",
            }

        if "raise ValueError" not in draft_code:
            return {
                "valid": False,
                "reason": "divide 方法缺少除零保护。",
            }

        return {
            "valid": True,
            "reason": "代码通过当前 mock evaluation。",
        }

    return None


def analyze_intent(state):
    return llm_call("analyze_intent", state["user_request"], state)


def get_context(state):
    return llm_call("get_context", state["user_request"], state)


def draft_code(state):
    return llm_call("draft_code", state["user_request"], state)


def evaluate(state):
    return llm_call("evaluate", state["user_request"], state)


def retry(state, max_retries=2):
    while not state["evaluation"]["valid"] and state["retry_count"] < max_retries:
        state["retry_count"] += 1
        state["status"] = "retrying"
        retry_reason = state["evaluation"]["reason"]
        state["context"]["retry_reason"] = retry_reason

        print(f"Retry {state['retry_count']}: {retry_reason}")

        state["draft_code"] = draft_code(state)
        state["evaluation"] = evaluate(state)

    return state


def run(user_request: str, max_retries=2):
    state = {
        "user_request": user_request,
        "intent": None,
        "context": None,
        "draft_code": None,
        "evaluation": None,
        "final_output": None,
        "status": "running",
        "retry_count": 0,
    }

    print("Step 1: analyze intent")
    state["intent"] = analyze_intent(state)

    print("Step 2: get context")
    state["context"] = get_context(state)

    print("Step 3: draft code")
    state["draft_code"] = draft_code(state)

    print("Step 4: evaluate")
    state["evaluation"] = evaluate(state)

    if not state["evaluation"]["valid"]:
        state = retry(state, max_retries=max_retries)

    if state["evaluation"]["valid"]:
        state["final_output"] = state["draft_code"]
        state["status"] = "success"
    else:
        state["status"] = "failed"

    return state


if __name__ == "__main__":
    result = run(PROMPT)

    print("\nFinal state:")
    for key, value in result.items():
        print(f"{key}: {value}")
