# Laning API SDK

### 外部调用
- 例如，想要获取字典信息
```python
from laningapi import Dictionary, TransportExternal

# 新建外部访问对象
te = TransportExternal()
te.init("http://mock/auth/application/get_token", "tester", "p@ssw0rd")

dict_api = Dictionary(baseurl="http://mock/", transport=te)  # 传入具体的模块
data = dict_api.get_dict_info(name="dict_name")
```

### Install From GitLab

```bash
pip install laningapi==0.0.8 \
--index-url http://__token__:wjwuNxycaKS6xeWJ4Y-1@git.dev.laningtech.net/api/v4/projects/623/packages/pypi/simple \
--trusted-host git.dev.laningtech.net
```
