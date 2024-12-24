// 定义字段的验证规则，包括用户名、密码、手机和邮箱
const rules = {
    username: {
        pattern: /^[a-zA-Z0-9]{5,8}$/,
        message: '用户名必须是5-8位字母或数字'
    },
    password: {
        pattern: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,16}$/,
        message: '密码必须包含大小写字母和数字，长度8-16位'
    },
    phone: {
        pattern: /^1[3-9]\d{9}$/,
        message: '请输入正确的手机号码'
    },
    email: {
        pattern: /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/,
        message: '请输入正确的邮箱地址'
    }
};

// 为每个输入字段设置事件监听器，以便在输入时进行验证
document.querySelectorAll('input').forEach(input => {
    input.addEventListener('input', function() {
        validateField(this.id, this.value);
    });
});

// 验证特定字段的值是否符合规则，并更新错误信息显示
function validateField(fieldName, value) {
    const rule = rules[fieldName];
    const errorElement = document.getElementById(`${fieldName}-error`);

    if (!rule.pattern.test(value)) {
        errorElement.textContent = rule.message;
        return false;
    }
    errorElement.textContent = '';
    return true;
}

// 处理用户注册的逻辑，包括字段验证和用户保存
function handleRegister(event) {
    event.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const phone = document.getElementById('phone').value;
    const email = document.getElementById('email').value;

    // 验证所有字段
    const isValid = Object.keys(rules).every(field =>
        validateField(field, document.getElementById(field).value)
    );

    if (!isValid) {
        return false;
    }

    // 获取现有用户
    const users = JSON.parse(localStorage.getItem('users') || '[]');

    // 检查用户名是否已存在
    if (users.some(user => user.username === username)) {
        alert('用户名已存在！');
        return false;
    }

    // 保存新用户
    users.push({ username, password, phone, email });
    localStorage.setItem('users', JSON.stringify(users));

    alert('注册成功！');
    window.location.href = 'login.html';
    return false;
}