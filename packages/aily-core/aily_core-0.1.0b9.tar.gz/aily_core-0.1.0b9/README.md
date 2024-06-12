# Aily Code SDK Core

## Development

开发时，需要在根目录中创建 `.env` 文件，填写如下内容：

```bash
AILY_SDK_LOCAL_DEBUG=true
AILY_SDK_CLIENT_ID=c_xxx
AILY_SDK_CLIENT_SECRET=cxxx
AILY_SDK_DOMAIN=https://ae-openapi.feishu-boe.cn/
```

然后通过 `python -m unitest` 命令通过执行单元测试来调试代码。

### Build

```bash
python -m build
```

### Upload

```bash
python -m twine upload dist/* --verbose
```
