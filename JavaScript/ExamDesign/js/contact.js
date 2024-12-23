// 联系我们页功能

// 示例：表单验证和留言保存
function setupContactForm() {
    const form = document.querySelector('#contact-form');
    const messageList = document.querySelector('#message-list');
    const messages = JSON.parse(localStorage.getItem('messages')) || [];

    form.addEventListener('submit', (event) => {
        event.preventDefault();
        const email = form.querySelector('#email').value;
        const message = form.querySelector('#message').value;
        if (email && message) {
            messages.push({ email, message });
            localStorage.setItem('messages', JSON.stringify(messages));
            alert('留言已保存');
            // 更新留言列表
        } else {
            alert('请输入有效的邮箱和留言');
        }
    });

    // 加载留言
    messages.forEach(msg => {
        const li = document.createElement('li');
        li.textContent = `${msg.email}: ${msg.message}`;
        messageList.appendChild(li);
    });
}

document.addEventListener('DOMContentLoaded', setupContactForm); 