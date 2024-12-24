// 存储用户数据
function getUsers() {
    const users = localStorage.getItem('users');
    return users ? JSON.parse(users) : [];
}

// 生成验证码
function generateCaptcha() {
    return Math.random().toString(36).substring(2, 8);
}

// 刷新验证码
function refreshCaptcha() {
    const captcha = generateCaptcha();
    document.getElementById('captcha-display').innerText = captcha;
    sessionStorage.setItem('captcha', captcha);
}

// 登录处理
function handleLogin(event) {
    event.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const captchaInput = document.getElementById('captcha').value;
    const captchaStored = sessionStorage.getItem('captcha');

    // 验证码检查
    if (captchaInput !== captchaStored) {
        alert('验证码错误');
        refreshCaptcha();
        return false;
    }

    // 用户验证
    const users = getUsers();
    const user = users.find(u => u.username === username && u.password === password);

    if (user) {
        alert('登录成功！');
        window.location.href = '‌index.html';
    } else {
        alert('用户名或密码错误！');
        refreshCaptcha();
    }
    return false;
}

// 页面加载时生成验证码
window.onload = refreshCaptcha;