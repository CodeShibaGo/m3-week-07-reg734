# CSRF 防禦筆記（Flask 專案）

## 1. 什麼是 CSRF 攻擊？該如何預防？

**CSRF（Cross-Site Request Forgery，跨站請求偽造）**是一種攻擊方式，讓使用者在不知情的情況下對受信任網站發出請求。例如：攻擊者引導你點擊連結，結果你在已登入的狀態下對某個網站發出了「刪除帳號」的請求。

### 🛡 如何預防：
- 為表單加入 CSRF Token，並在伺服器端驗證。
- 對敏感操作使用 POST 且搭配 token 驗證。
- 設定 `SameSite` cookie 屬性，減少第三方請求風險。

---

## 2. 如何在 Flask 專案中使用 CSRF 防護

Flask-WTF 提供兩種方式保護應用程式：

### ✅ 方式一：使用 FlaskForm（自動加入 CSRF token）

```python
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class MyForm(FlaskForm):
    name = StringField('Name')
    submit = SubmitField('Submit')
```

HTML 模板：

```html
<form method="POST">
    {{ form.hidden_tag() }}  <!-- 自動包含 CSRF token -->
    {{ form.name.label }} {{ form.name() }}
    {{ form.submit() }}
</form>
```

---

### ✅ 方式二：使用 `from flask_wtf.csrf import CSRFProtect`

如果你不使用 `FlaskForm`，也可用 `CSRFProtect` 直接為整個 app 啟用 CSRF：

```python
from flask import Flask
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
csrf = CSRFProtect(app)
```

在模板中手動插入：

```html
<form method="POST">
  <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
  <input type="text" name="username">
  <button type="submit">送出</button>
</form>
```

Flask-WTF 將會自動驗證 POST 表單中的 `csrf_token`。

---

## 3. Ajax 需要使用 CSRF token 嗎？該如何使用？

### ✅ 是的，Ajax 請求如果涉及改變伺服器狀態（如 POST/PUT/DELETE），也需加入 CSRF Token。

### 實作方式：

1. 在 HTML `<head>` 中加入：

```html
<meta name="csrf-token" content="{{ csrf_token() }}">
```

2. 使用 JavaScript / jQuery 時加入 Token header：

#### 使用 jQuery：

```javascript
$(function() {
    const csrfToken = $('meta[name="csrf-token"]').attr('content');
    $.ajaxSetup({
        headers: {
            'X-CSRFToken': csrfToken
        }
    });
});
```

#### 使用 Fetch API：

```javascript
const token = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

fetch("/submit", {
    method: "POST",
    headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": token
    },
    body: JSON.stringify({ field: "value" })
});
```

伺服器端會自動驗證 `X-CSRFToken` 是否有效。

---

📚 參考資料：[Flask-WTF CSRF Documentation](https://flask-wtf.readthedocs.io/en/1.2.x/csrf/)
