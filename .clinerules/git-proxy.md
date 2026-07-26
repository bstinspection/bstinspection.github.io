# Git 推送代理规则

## 远端仓库
`https://github.com/bstinspection/bstinspection.github.io.git`

## 推送流程
1. 先配置 7890 端口代理，执行推送
2. 若推送失败，清除代理后直连重试
3. 若任一方式成功，清除代理配置

```bash
git config --local http.proxy http://localhost:7890
git config --local https.proxy http://localhost:7890
git push
# 若失败，清代理直连重试
git config --local --unset http.proxy
git config --local --unset https.proxy
git push
```

## 成功后清理
推送成功后务必清除代理，避免影响其他 Git 操作：
```bash
git config --local --unset http.proxy
git config --local --unset https.proxy
```
