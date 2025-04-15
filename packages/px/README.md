# better python extensions

- ✅ 开箱即用的 python 扩展

## Installation

```ruby
pip install better-px

# or 
uv add better-px
```

## Usage

```python
from better_px import *

import px

# or if conflict
import better_px as px


def main():
    print(px.hello())
```

## References

- <https://github.com/better-py/py-pkg>

### 目录结构

- <https://pkg.go.dev/golang.org/x>
  - 参考 go 官方的 x 扩展库目录格式
- <https://github.com/kubernetes/kubernetes>
  - 参考 k8s 的目录格式
