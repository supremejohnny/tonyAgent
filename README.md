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