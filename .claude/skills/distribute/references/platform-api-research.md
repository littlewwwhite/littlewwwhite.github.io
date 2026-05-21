# Cross-Platform Publishing: API & CLI Research (2026-04)

## Summary Matrix

| Platform | Official API | CLI Tool | Auth | Content Format | Rate Limits | Browser Fallback |
|----------|-------------|----------|------|---------------|-------------|-----------------|
| Twitter/X | v2 API (pay-per-use) | xurl, x-cli, AutoCLI | OAuth 2.0 PKCE | 280 chars, images | $0.01/post | Not needed |
| WeChat 公众号 | Official (认证 only) | md2wechat, wechat-publisher | APP_ID + APP_SECRET | HTML (inline CSS) | ~500 calls/day | Yes (for 个人号) |
| 小红书 | None official | AutoCLI, xiaohongshu-cli | Cookie/session reuse | 800 chars + images | Undocumented | Primary method |
| Medium | Legacy API (frozen) | md2mid, cross-post-blog | Integration token | Markdown/HTML | Undocumented | Viable |
| Dev.to | Forem REST API | devto-cli, cross-post-blog | API key | Markdown + frontmatter | 10 creates/30s | Not needed |
| LinkedIn | Posts API (Marketing) | None mature | OAuth 2.0 + approval | Text/images/video | ~100/day/member | Viable |
| 知乎 | None (actively blocked) | None stable | N/A | N/A | N/A | Only viable method |
| Cross-platform | N/A | AutoCLI, cross-post-blog | Per-platform | Per-platform | Per-platform | AutoCLI uses it |

## 1. Twitter/X

### API Status
- **v2 API** is the current standard. As of Feb 2026, X switched to **pay-per-use** pricing: $0.01/post created, $0.005/post read.
- Free tier was severely cut: read-only, 1 req/24h on most endpoints. No posting on free tier.
- Legacy tiers (Basic $100/mo, Pro $5K/mo) no longer available for new signups.

### CLI Tools
| Tool | Lang | GitHub | Notes |
|------|------|--------|-------|
| **xurl** | Go | [xdevplatform/xurl](https://github.com/xdevplatform/xurl) | Official X CLI, OAuth 1.0a + 2.0 |
| **x-cli** | Node | [Infatoshi/x-cli](https://github.com/Infatoshi/x-cli) | `x-cli tweet post "text"` |
| **AutoCLI** | Rust | [nashsu/opencli-rs](https://github.com/nashsu/opencli-rs) | `opencli twitter post --text "..."`, browser session reuse |
| **twurl** | Ruby | [twitter/twurl](https://github.com/twitter/twurl) | Classic but aging, no OAuth 2.0 PKCE |

### Libraries
- **Python**: `tweepy` (v4.14+) — `client.create_tweet(text="...")`
- **Node.js**: `twitter-api-v2` ([npm](https://www.npmjs.com/package/twitter-api-v2)) — `client.v2.tweet("...")`

### Auth
- OAuth 2.0 with PKCE (recommended) or OAuth 1.0a
- Requires developer account + app credentials (consumer key/secret + access token/secret)

### Content Format
- Max 280 characters for text
- Images: upload via media endpoint, attach media_id to tweet
- No native Markdown support

### Recommendation
**AutoCLI** (already in your distribute skill) is the best fit — it reuses Chrome session so no API key costs. For programmatic fallback, `tweepy` or `twitter-api-v2` with pay-per-use at $0.01/tweet is cheap enough.

---

## 2. WeChat Official Account (微信公众号)

### API Status
- Official "发布能力" API exists for **authenticated service accounts (认证服务号)** only.
- **Critical change (July 2025)**: 个人主体账号、企业主体未认证账号 lose all publishing API permissions.
- API flow: get access_token → upload images → create draft → publish draft.
- Rate limits: ~500 API calls/day for most endpoints, access_token valid 2 hours.

### CLI Tools
| Tool | Lang | GitHub | Notes |
|------|------|--------|-------|
| **md2wechat** | Python | [md2wechat.com](https://www.md2wechat.com/) | Paid (¥129), converts MD→WeChat HTML, creates drafts |
| **wechat-publisher** | Python | [0731coderlee-sudo/wechat-publisher](https://github.com/0731coderlee-sudo/wechat-publisher) | Free, one-click MD to draft |
| **wechat-article-publisher-skill** | Python | [iamzifei/wechat-article-publisher-skill](https://github.com/iamzifei/wechat-article-publisher-skill) | Claude Skill for WeChat publishing |
| **WeChatMediaPlatformAutomation** | Python | [LinusLing/WeChatMediaPlatformAutomation](https://github.com/LinusLing/WeChatMediaPlatformAutomation) | CLI with -t title, -c content, --preview |
| **weflow** | Python | [twwch/weflow](https://github.com/twwch/weflow) | Full pipeline: crawl → AI summarize → publish |

### MCP Servers
- WeChat Publisher MCP on LobeHub — works with Claude Desktop / Cursor

### Auth
- APP_ID + APP_SECRET from 公众号后台
- IP whitelist required for server-to-server calls
- access_token refresh every 2 hours

### Content Format
- **HTML with inline CSS only** — WeChat strips `<style>` tags and external CSS
- Images must be uploaded to WeChat's media servers first (returns media_id)
- No Markdown rendering — must convert MD → HTML with inline styles
- Max article length: ~20,000 characters

### Key Limitation
If your 公众号 is a 个人号 (personal account), as of July 2025 you **cannot use the API at all**. You must either:
1. Upgrade to 认证服务号 (requires enterprise entity)
2. Use browser automation (Playwright/Puppeteer) or 爱贝壳 extension

### Recommendation
If 认证号: use `wechat-publisher` or `md2wechat` for API publishing.
If 个人号: **browser automation is the only path** — use 爱贝壳内容同步助手 or AutoCLI with Playwright.

---

## 3. Xiaohongshu (小红书)

### API Status
- **No official public API** for content publishing.
- Reverse-engineered APIs exist but require `x-s` / `x-s-common` / `x-t` signature generation.
- Platform actively detects automation; accounts may be flagged as "suspected AI-generated."

### CLI Tools
| Tool | Lang | GitHub | Notes |
|------|------|--------|-------|
| **AutoCLI** | Rust | [nashsu/opencli-rs](https://github.com/nashsu/opencli-rs) | `opencli xiaohongshu publish ...`, browser session reuse |
| **xiaohongshu-cli** | TS | [jackwener/xiaohongshu-cli](https://github.com/jackwener/xiaohongshu-cli) | Search, read, interact via reverse-engineered API |
| **Autoxhs** | Python | [Gikiman/Autoxhs](https://github.com/Gikiman/Autoxhs) | AI-powered auto-generation + publishing |

### MCP Servers
- **xiaohongshu-mcp** ([LobeHub](https://lobehub.com/mcp/yyh211-xiaohongshu)) — Playwright-based, automated login + posting
- **xhs-mcp** (FrancoSbaffi) — Playwright-based publish
- **RedNote MCP** (MilesCool) — Node.js + Playwright

### Content Format
- Image-text notes: title ≤20 chars, body ≤800 chars, 1-9 images
- Hashtags: 3-5 recommended (e.g., `#AI #技术分享`)
- **No links allowed** in post body (stripped by platform)
- Images: square or 3:4 ratio preferred

### Rate Limits / Risks
- No more than ~30 automated actions/day recommended
- Account flagging risk for patterns: rapid posting, identical formatting, API-signature anomalies

### Recommendation
**AutoCLI with Chrome session reuse** is the safest approach — it mimics real browser behavior. Keep posting frequency low (1-2 posts/day max). Always use `--draft true` first to review.

---

## 4. Medium

### API Status
- Official API exists but is **frozen** — Medium stopped accepting new API integration applications.
- Existing integration tokens still work for creating posts.
- API supports: create posts (Markdown or HTML), list publications. Does NOT support: updating posts, deleting posts, uploading images separately.

### CLI Tools
| Tool | Lang | GitHub | Notes |
|------|------|--------|-------|
| **md2mid** | Go | [timakin/md2mid](https://github.com/timakin/md2mid) | CLI to publish MD files (last updated 2017) |
| **cross-post-blog** | Node | [shahednasser/cross-post](https://github.com/shahednasser/cross-post) | Publishes to Dev.to + Medium + Hashnode |

### Auth
- Integration token from Settings → Security → Integration tokens
- Tokens do not expire (but can be revoked)

### Content Format
- Accepts Markdown or HTML in `contentFormat` field
- Tags: max 5, each ≤25 characters
- `canonicalUrl` supported (critical for SEO when cross-posting)
- No image upload endpoint — images must be inline URLs

### Rate Limits
- Undocumented but exists; back off on 429 responses

### Recommendation
Use `cross-post-blog` CLI for Medium + Dev.to combined publishing. Always set `canonicalUrl` to your Hugo blog URL.

---

## 5. Dev.to (Forem)

### API Status
- **Fully open REST API** — best developer experience of all platforms.
- Endpoint: `POST https://dev.to/api/articles`
- Full CRUD on articles, comments, users.

### CLI Tools
| Tool | Lang | GitHub/NPM | Notes |
|------|------|------------|-------|
| **devto-cli** | Node | [@sinedied/devto-cli](https://www.npmjs.com/package/@sinedied/devto-cli) | Publish MD files, rewrites image URLs to GitHub raw |
| **cross-post-blog** | Node | [shahednasser/cross-post](https://github.com/shahednasser/cross-post) | Multi-platform including Dev.to |
| **GitHub Action** | YAML | [marketplace](https://github.com/marketplace/actions/publish-to-dev-to) | CI/CD publish on push |

### Auth
- API key from https://dev.to/settings/extensions → Generate API Key
- Header: `api-key: YOUR_KEY`

### Content Format
- Full Markdown with Jekyll-style front matter
- `canonical_url` supported natively in front matter
- Tags: up to 4
- Series support
- Cover image via `main_image` URL

### Rate Limits
- 10 article creates per 30 seconds
- 30 article updates per 30 seconds
- 429 on exceeding

### Recommendation
**Best platform for automated cross-posting from Hugo.** Use `devto-cli` or the GitHub Action to auto-publish on `git push`. Always set `canonical_url` to your Hugo blog.

---

## 6. LinkedIn

### API Status
- **Posts API** (part of Community Management API) supports text, images, video publishing.
- Requires joining **Marketing Developer Program** and getting `w_member_social` scope approved.
- Approval takes 1-4 weeks with manual review.
- Does NOT support: document uploads, polls, newsletters.

### CLI Tools
- No mature dedicated CLI tools found.
- Best approach: custom script using the API directly.

### Libraries
- **Python**: `python-linkedin-v2`, or raw `requests` with OAuth
- **Node.js**: `linkedin-api-client` (unofficial)

### Auth
- OAuth 2.0 Authorization Code Flow
- Scopes: `w_member_social` (personal), `w_organization_social` (company page)
- Tokens expire in 60 days, refresh tokens 365 days
- App must have "Share on LinkedIn" product enabled

### Content Format
- Text posts: up to ~3000 characters
- Images: upload to LinkedIn's asset register first, then reference
- Links with preview
- No Markdown support — plain text only

### Rate Limits
- ~100 API calls per day per member
- Stricter limits on content creation

### Recommendation
LinkedIn's approval barrier makes it less suitable for quick automation. Consider using **爱贝壳** or **Buffer** as intermediaries. If you do get API access, a simple Python script with `requests` is sufficient.

---

## 7. Zhihu (知乎)

### API Status
- **No official public API** for content publishing.
- Zhihu has **actively DMCA'd** multiple reverse-engineered API projects on GitHub.
- Internal API endpoints change frequently to break scrapers.

### Known Projects (all unstable)
| Tool | Lang | GitHub | Status |
|------|------|--------|--------|
| **zhihu-api** | Node | [lzjun567/zhihu-api](https://github.com/lzjun567/zhihu-api) | Mostly read-only, aging |
| **zhihu-py3** | Python | Various | Frequently broken |

### Browser Automation
- **Only reliable method** for publishing to Zhihu.
- AutoCLI supports Zhihu via browser session reuse.
- Playwright-based solutions work but require careful anti-detection.

### Content Format (for reference)
- Zhihu 专栏 (column) articles: full rich text, no strict length limit
- Supports Markdown in editor but stores as HTML
- Images: upload to Zhihu's CDN during creation

### Recommendation
**Browser automation only.** Use AutoCLI or 爱贝壳 to publish. Do not invest in API-based approaches — they will break.

---

## 8. Cross-Platform Tools

### AutoCLI (formerly opencli-rs)
- **GitHub**: [nashsu/opencli-rs](https://github.com/nashsu/opencli-rs)
- **Language**: Rust (single 4.7MB binary)
- **Platforms**: 55+ sites including Twitter, Xiaohongshu, Zhihu, Bilibili, Weibo
- **Key feature**: Browser session reuse — logs in using your Chrome cookies, no API keys needed
- **Publishing commands**: `opencli twitter post`, `opencli xiaohongshu publish`
- **Already integrated** in your `/distribute` skill

### cross-post-blog
- **GitHub**: [shahednasser/cross-post](https://github.com/shahednasser/cross-post)
- **NPM**: `cross-post-blog` v1.5.4
- **Platforms**: Dev.to, Medium, Hashnode
- **Usage**: `npx cross-post-blog -l ./article.md -p devto,medium,hashnode`
- **Features**: Local markdown file support, canonical URL, per-platform config

### 爱贝壳内容同步助手
- **Chrome Web Store**: [爱贝壳](https://chromewebstore.google.com/detail/爱贝壳内容同步助手/jejejajkcbhejfiocemmddgbkdlhhngm)
- **Platforms**: 50+ including WeChat, Zhihu, Xiaohongshu, Bilibili, Douban, Weibo, Toutiao, Baijia Hao
- **Content types**: 文章, 动态, 图文, 短视频 (matches your distribute skill's 4 types)
- **Method**: Browser extension that auto-fills content across platforms
- **Free tier available**

### GitHub Actions: Cross Platform Blog Publish
- **Marketplace**: [cross-platform-blog-publish](https://github.com/marketplace/actions/cross-platform-blog-publish)
- **Platforms**: Dev.to, Medium, Hashnode
- **Trigger**: On push to repo, reads frontmatter flags to decide which platforms

### n8n Workflows
- Open-source workflow automation
- Community templates for Xiaohongshu, Twitter, LinkedIn
- Can orchestrate multi-platform publishing with custom logic

---

## 9. Headless Browser Automation

### When to Use
- Platforms with no API: **Zhihu, Xiaohongshu (primary), WeChat 个人号**
- Platforms with frozen/restricted API: **Medium (fallback), LinkedIn (if no approval)**

### Playwright (Recommended)
- Cross-browser (Chromium, Firefox, WebKit)
- Built-in auto-wait, network interception
- Since late 2025: built-in AI test agents (Planner, Generator, Healer)
- MCP Server available for Claude Desktop integration
- Python: `pip install playwright`
- Node: `npm install playwright`

### AutoCLI Approach
- Uses real Chrome with session/cookie reuse
- Most reliable for Chinese platforms (anti-detection bypass)
- Single binary, no runtime dependencies

### Anti-Detection Considerations
- Use `playwright-stealth` or `puppeteer-extra-plugin-stealth`
- Reuse real browser profiles instead of fresh ones
- Add random delays between actions
- Xiaohongshu: limit to 1-2 posts/day
- Zhihu: watch for captcha triggers

---

## 10. Recommended Architecture for Your Blog

```
Hugo Blog (content/posts/YYMMDD/index.md)
    │
    ├── /publish → git push → GitHub Actions → Hugo deploy
    │
    └── /distribute → Generate platform versions
            │
            ├── article.md ──→ Dev.to (devto-cli, canonical_url)
            │                ──→ Medium (cross-post-blog, canonical_url)  
            │                ──→ WeChat (md2wechat or 爱贝壳)
            │                ──→ Zhihu (爱贝壳 or AutoCLI browser)
            │
            ├── dynamic.md ──→ Twitter/X (AutoCLI or tweepy, $0.01/tweet)
            │               ──→ Weibo (爱贝壳)
            │
            ├── imagetext.md → Xiaohongshu (AutoCLI browser)
            │
            └── video.md ───→ Douyin/Bilibili (manual or 爱贝壳)
```

### Priority Implementation Order
1. **Dev.to** — easiest, best API, set up GitHub Action for auto-publish
2. **Twitter/X** — via AutoCLI (already in skill) or pay-per-use API
3. **Xiaohongshu** — via AutoCLI browser (already in skill)
4. **WeChat 公众号** — check if 认证号; if yes, use wechat-publisher; if 个人号, use 爱贝壳
5. **Zhihu** — 爱贝壳 or AutoCLI browser only
6. **Medium** — via cross-post-blog if you have an integration token
7. **LinkedIn** — lowest priority due to approval barrier
