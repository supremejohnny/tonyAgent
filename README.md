# tonyAgent的目标是实现一个最小的学习型coding agent。

————————————————————————————

### week1：
第一阶段只关注5个核心概念：
state,loop,tool calling, evaluation, retry。
不做能力实现，而是做出一个可运行、可观察、可调式的最小闭环。

#### 2026年5月21日-进展  
创建了`run.py`,并且创建了最简单的业务逻辑：  
user_prompt -> analyze -> getting related contexts -> draft a code -> eval code (if not valid go back to analyze/draft) -> give final result  

从而得到了初步的框架。

#### 2026年5月23日-进展  
精进了state初步设计，添加了`retry` , `status`字段以维护agent的retry逻辑。  
同时在state的定义中添加了每个字段的含义以及存放内容。  
定义evaluation的初步结构为:  
```python
"evalution":
{
    "valid": bool,  # validity
    "reason": str   # the failure reason
}
```
至此，第一步state设定完成。

#### 2026年5月23日-codex进展  
添加了`test_run.py`，这是一个用`if/elif`构造的 mock LLM 测试脚本。  
它的作用不是生成真实代码，而是把`intent -> context -> draft_code -> evaluation -> retry -> final_output`这一条状态流转完整跑通，方便观察每个 state 字段在不同阶段如何变化。  
在这个示例里，第一次草稿代码会故意缺少`divide`方法，因此`evaluation["valid"]`会先返回`False`，并把失败原因写入`evaluation["reason"]`。  
随后`retry()`会读取这个 reason，把它放回 context 继续下一轮生成；第二轮补齐`divide`和除零保护后，流程会收敛到 success。  
这样后续你在做真正的 LLM 接入前，就已经有一个可运行、可解释、可验证的最小闭环样例。  
