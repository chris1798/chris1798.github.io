---
title: "RHEL 9 + podman-compose 安裝 Dify 完整 SOP：九個坑與實測修復"
date: 2026-10-17
description: 在 Red Hat Enterprise Linux 9 上用 podman-compose 安裝 Dify docker 版，會遇到九個 docker-compose 不會遇到的問題。本文按出現順序記錄每個症狀、根因與實測有效的修復指令，最後附驗證與回滾方法。
tags: [Dify, podman, podman-compose, RHEL9, SELinux, 容器, 自架, SOP]
---

# RHEL 9 + podman-compose 安裝 Dify 完整 SOP：九個坑與實測修復

> 實測環境：RHEL 9.8 (Plow) · podman 5.8.2 · podman-compose 1.6.0 · Dify 1.17.1 · 2026-10-17 全線啟動成功。
> 安裝位置 `/root/ai/dify/docker`，Web 入口 `http://<host>/install`。
> 想先了解 Dify 功能與選型，請看姊妹文《Dify 完整功能解析與適用場景》。

## TL;DR：五分鐘快速路徑

如果你不想看每個坑的來龍去脈，照這個順序做完就能跑：

```bash
# 0. 前置：以 root 於 /root/ai/dify/docker 操作（git clone dify 後）
cd /root/ai/dify/docker
cp docker-compose.yaml docker-compose.yaml.bak

# 1. 補上 default 網路（坑 2）
sed -i '/^networks:/a\  default:\n    driver: bridge' docker-compose.yaml

# 2. 解除短名稱限制（坑 3）
echo 'unqualified-search-registries = ["docker.io"]' \
  > /etc/containers/registries.conf.d/999-unqualified.conf

# 3. weaviate 改從 Docker Hub 拉再 retag（坑 4）
podman pull docker.io/semitechnologies/weaviate:1.39.2
podman tag docker.io/semitechnologies/weaviate:1.39.2 \
           cr.weaviate.io/semitechnologies/weaviate:1.39.2

# 4. 移除 podman-compose 不支援的 depends_on（坑 5、8）
sed -i -E '/^      (db_mysql|oceanbase|seekdb):$/{N;N;d}' docker-compose.yaml
sed -i '/^  nginx:/,/^  [a-z_]*:$/{/^    depends_on:$/d; /^      - api$/d; /^      - web$/d}' docker-compose.yaml

# 5. SELinux 標籤（坑 6、7）
semanage fcontext -a -t container_file_t "/root/ai/dify(/.*)?"
restorecon -RF /root/ai/dify

# 6. nginx DNS 解析器改成 podman gateway（坑 9；IP 看 container 內 /etc/resolv.conf）
sed -i 's/resolver 127.0.0.11/resolver 10.89.5.1/' nginx/conf.d/default.conf.template

# 7. 啟動
podman-compose up -d

# 8. 驗證
curl -s -o /dev/null -w "HTTP %{http_code}\n" http://localhost/install   # 期待 200
```

以下逐坑說明「為什麼」。每一條都是實際踩過、修復後驗證過的。

---

## 坑 1：`WARNING: unused networks: opensearch-net, milvus` — 可以忽略

**症狀**：`podman-compose up` 一開頭就噴警告。

**根因**：Dify 的 compose 檔在 top-level `networks:` 定義了 `milvus` 和 `opensearch-net`，但這兩者是**可選向量資料庫**的專用網路。你的 `.env` 裡：

```bash
VECTOR_STORE=weaviate
COMPOSE_PROFILES=${VECTOR_STORE:-weaviate},${DB_TYPE:-postgresql},collaboration
```

只有 weaviate profile 被啟用，milvus/opensearch 的服務群根本不會啟動，於是沒有任何執行中服務掛在這兩個網路上，podman-compose 就多嘴警告了。docker-compose 對同樣的事實沉默，podman-compose 話多一點而已。

**處置**：**不用做任何事**。這是九個坑裡唯一無害的。真正的问题在後面。

---

## 坑 2：`RuntimeError: missing networks: default`

**症狀**：警告之後直接崩潰，compose 完全沒啟動。

```
RuntimeError: missing networks: default
```

**根因**：Dify 1.17.x 的 compose 檔在每個服務的 `networks:` 裡**明確寫了 `- default`**，但 top-level `networks:` 區塊沒有定義 `default`。docker-compose 會隱式建立 default 網路；podman-compose 1.6.0 不會，直接丟例外。

**修復**：在 top-level `networks:` 底下插入 default 定義：

```bash
sed -i '/^networks:/a\  default:\n    driver: bridge' docker-compose.yaml
```

結果長這樣：

```yaml
networks:
  default:
    driver: bridge
  # create a network between sandbox, api and ssrf_proxy...
  ssrf_proxy_network:
    driver: bridge
    internal: true
```

---

## 坑 3：`short-name resolution enforced but cannot prompt without a TTY`

**症狀**：日誌裡反覆出現，busybox、postgres:15-alpine 等圖片拉不下來。

**根因**：RHEL 的 podman 預設**強制 unqualified search 確認**——圖片名稱沒寫 registry（如 `busybox`）時會互動詢問要從哪個 registry 拉；但 compose 背景執行沒有 TTY，詢問直接失敗。

**修復**：明確指定預設搜尋 registry：

```bash
echo 'unqualified-search-registries = ["docker.io"]' \
  > /etc/containers/registries.conf.d/999-unqualified.conf
```

---

## 坑 4：weaviate 拉取被限流 `toomanyrequests`

**症狀**：

```
reading manifest 1.39.2 in cr.weaviate.io/semitechnologies/weaviate:
toomanyrequests: You have reached your unauthenticated pull rate limit
```

**根因**：訊息裡寫著 docker.com 的限流連結，很容易誤以為是 Docker Hub 額度用光。**實際上是 `cr.weaviate.io` 這個 registry 自己的匿名限流**。可以用 registry headers 確認你的 Docker Hub 額度其實還在：

```bash
TOKEN=*** "https://auth.docker.io/token?service=registry.docker.io&scope=repository:library/nginx:pull" \
  | python3 -c "import sys,json;print(json.load(sys.stdin)['token'])")
curl -sI -H "Authorization: Bearer $TOKEN" \
  "https://registry-1.docker.io/v2/library/nginx/manifests/latest" | grep -i ratelimit
# x-ratelimit-remaining: 97  ← Docker Hub 還有額度
```

**修復**：同一個 weaviate 映像檔在 Docker Hub 也有（`semitechnologies/weaviate`），從 Hub 拉下來再 retag 成 compose 要的名字：

```bash
podman pull docker.io/semitechnologies/weaviate:1.39.2
podman tag docker.io/semitechnologies/weaviate:1.39.2 \
           cr.weaviate.io/semitechnologies/weaviate:1.39.2
```

compose 之後看到本地已有同名 image 就不會再拉。

---

## 坑 5：`KeyError: 'db_mysql'`

**症狀**：image 全部拉完、一半服務起來了，然後 podman-compose 崩潰：

```
File "podman_compose.py", line 3518, in check_dep_conditions
    deps_cd.extend(compose.container_names_by_service[d.name])
KeyError: 'db_mysql'
```

**根因**：Dify 1.17 用了 compose 新語法 `depends_on` 的 `required: false`（相依服務可缺席）：

```yaml
    depends_on:
      db_postgres:
        condition: service_healthy
        required: false
      db_mysql:
        condition: service_healthy
        required: false
```

podman-compose 1.6.0 **不支援 `required: false`**，對被 profile 停用的服務（你用的是 postgresql，`db_mysql`/`oceanbase`/`seekdb` 都沒啟用）照樣去查服務名稱，查不到就 KeyError。

**修復**：把這三個停用 DB 的 depends_on 區塊（名稱行 + condition 行 + required 行，共三行）從每個服務移除：

```bash
sed -i -E '/^      (db_mysql|oceanbase|seekdb):$/{N;N;d}' docker-compose.yaml
```

服務本體的 `db_mysql:` 定義留著沒關係——它由 `profiles: [mysql]` 控制，不會啟動。

---

## 坑 6 & 7：postgres/redis 無限重啟 `Permission denied`

**症狀**：`db_postgres` 與 `redis` 一直 `Exited (1) (starting)` 迴圈：

```
mkdir: can't create directory '/var/lib/postgresql/data/pgdata': Permission denied
find: .: Permission denied
chown: .: Permission denied
```

而 nginx/ssrf_proxy 則是：

```
cp: cannot stat '/docker-entrypoint-mount.sh': Permission denied
```

**根因**：**SELinux，不是 unix 權限**。RHEL 9 預設 Enforcing，而 bind mount 來源目錄的標籤是 `admin_home_t`（因為放在 `/root` 下）：

```
drwxr-xr-x. root root unconfined_u:object_r:admin_home_t:s0 volumes/db
```

容器程序（`container_t` domain）讀寫這種標籤的目錄會被 SELinux 直接擋下。Docker 會自動幫 bind mount 重新標籤（或你加 `:Z`），podman 預設不會，Dify 上游 compose 檔也沒有 `:Z`。

**修復**：把**整個 dify 目錄樹**標成容器內容標籤。注意不只 `volumes/`——nginx 掛的是 `./nginx/` 下的設定檔，ssrf_proxy 掛的是 `./ssrf_proxy/`，都要涵蓋：

```bash
semanage fcontext -a -t container_file_t "/root/ai/dify(/.*)?"
restorecon -RF /root/ai/dify
```

驗證標籤變了：

```bash
ls -ldZ /root/ai/dify/docker/nginx
# system_u:object_r:container_file_t:s0  ← 正確
```

> 另一個選項是把整個 Dify 搬到 `/opt/dify` 之類非 home 的位置，從源頭避開 home 目錄標籤問題；但對已裝好的環境，relabel 是最小改動。

---

## 坑 8：nginx `podman start` 噴 `container state improper`

**症狀**：其他服務都起來了，唯獨 nginx 起不來：

```
the following dependencies of container f23a76...(api) are not running:
e4b54e...(init_permissions): container state improper
```

**根因**：nginx 用了短式依賴 `depends_on: [api, web]`，podman-compose 會把它轉成 podman 原生的 `--requires` 依賴鏈。`podman start` 時 libpod **遞歸**啟動依賴：nginx → api → api 又依賴 `init_permissions`——那是一次性初始化容器，跑完就 exited，永遠不可能「running」，遞歸檢查就判定 `container state improper`。

**修復**：nginx 的依賴（api、web）在啟動 nginx 時本來就都已經在跑了，直接移除 nginx 的 depends_on 再重建：

```bash
sed -i '/^  nginx:/,/^  [a-z_]*:$/{/^    depends_on:$/d; /^      - api$/d; /^      - web$/d}' docker-compose.yaml
podman rm -f docker_nginx_1
podman-compose up -d nginx
```

---

## 坑 9：全部 Up 但 Web 502 — `resolver: 127.0.0.11:53`

**症狀**：15 個容器全部 Up、api 健康檢查通過，但 `curl http://localhost/install` 回 **502 Bad Gateway**（而且卡 30 秒）。nginx 錯誤日誌：

```
[error] recv() failed (111: Connection refused) while resolving, resolver: 127.0.0.11:53
[error] api could not be resolved (110: Operation timed out)
```

**根因**：Dify 的 nginx 設定用「執行期動態解析 upstream」寫法，需要一個 DNS resolver，而設定檔寫死了：

```nginx
resolver 127.0.0.11 valid=30s ipv6=off;
```

`127.0.0.11` 是 **Docker 內建的 embedded DNS server**——podman 網路裡根本沒有這個服務，查詢直接被拒。api 本身完全正常（直接 curl 容器 IP 回 200），死的是 nginx 的名稱解析。

**修復**：改成 podman 網路的 DNS（就是容器內 `/etc/resolv.conf` 的 nameserver，通常是網路 gateway）：

```bash
# 先確認你的 gateway IP
podman exec docker_nginx_1 cat /etc/resolv.conf
# nameserver 10.89.5.1

sed -i 's/resolver 127.0.0.11/resolver 10.89.5.1/' \
  nginx/conf.d/default.conf.template nginx/conf.d/default.conf
podman restart docker_nginx_1
```

> 注意：`10.89.5.1` 是 `docker_default` 網路的 gateway，只要不砍掉重建網路就穩定。若哪天整個網路重建過，記得重查這個 IP。

---

## 最終驗證

```bash
# 1. 容器狀態：15 個 Up，核心服務 healthy
podman ps -a --format '{{.Names}} | {{.Status}}' | grep docker_
# db_postgres/redis/sandbox/api 都應顯示 (healthy)
# init_permissions Exited (0) 是正常的（一次性任務）

# 2. HTTP 入口
curl -s -o /dev/null -w "HTTP %{http_code}\n" http://localhost/install
# HTTP 200

# 3. API 探測
curl -s http://localhost/console/api/system-features | head -c 100
# {"deployment_edition":"COMMUNITY",...}
```

然後開瀏覽器到 `http://<host>/install` 建立 admin 帳號，即完成初始設定。

## 回滾

所有修改前都留了備份：

```bash
cd /root/ai/dify/docker
cp docker-compose.yaml.bak docker-compose.yaml   # 還原 compose 修改
```

SELinux 標籤與 registries.conf 不影響其他服務，通常不需要回滾；若要移除 fcontext 規則：`semanage fcontext -d "/root/ai/dify(/.*)?"`。

## 對照表：同一份 compose 檔，Docker vs podman 行為差異

| 行為 | docker-compose | podman-compose 1.6.0 |
|---|---|---|
| 未定義的 default 網路 | 隱式建立 | **RuntimeError** |
| `depends_on` 的 `required: false` | 支援 | **KeyError 崩潰** |
| bind mount SELinux 標籤 | 自動處理 | 需手動 relabel 或 `:Z` |
| embedded DNS `127.0.0.11` | 存在 | **不存在** |
| 短名稱無 TTY | 直接當 docker.io | **要求互動確認** |
| 未使用網路 | 沉默 | 噴 WARNING（無害） |
| 依賴鏈 one-shot 容器 | 不遞歸啟動 | **遞歸檢查爆 improper** |

## 結語

Dify 官方只測 docker-compose，podman 使用者要自己吸收這些相容性差距。好消息是：**坑都是確定性的**，同一份 Dify 1.17.x + podman-compose 1.6.0 組合，照本 SOP 的七個指令跑完就是一次成功。升級 Dify 版本後若 compose 檔結構改變，記得從 `docker-compose.yaml.bak` 重新套用（或重跑 generate_docker_compose 後再打補丁）。
