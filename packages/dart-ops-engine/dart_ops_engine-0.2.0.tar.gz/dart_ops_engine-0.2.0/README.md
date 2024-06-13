## 一个可以被Dart dart_ops_engine执行的Python脚本引擎

具体用法

```python
from typing import Any, Dict
from dart_ops_engine import DartOpsEngine
from action_run import ActionRun
from env import Env

class TestActionRun(ActionRun):
    def run(self, env: Env, request: Dict[str, Any]) -> Dict[str, Any]:
        return {}

if __name__ == '__main__':
    engine = DartOpsEngine(description='Dart Ops Engine')
    engine.addAction('test', TestActionRun())
    engine.run()
```