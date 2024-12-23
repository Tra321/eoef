// 活动预订页功能

// 示例：表单验证和动态价格计算
function setupBookingForm() {
    const form = document.querySelector('#booking-form');
    const activitySelect = document.querySelector('#activity');
    const numberInput = document.querySelector('#number');
    const totalPriceDisplay = document.querySelector('#total-price');
    const activities = {
        'activity1': 100,
        'activity2': 150
    };

    form.addEventListener('submit', (event) => {
        event.preventDefault();
        const activity = activitySelect.value;
        const number = parseInt(numberInput.value, 10);
        if (number > 0 && activities[activity]) {
            const totalPrice = activities[activity] * number;
            totalPriceDisplay.textContent = `总价: $${totalPrice}`;
            if (confirm('确认预订?')) {
                // 存储预订信息
            }
        } else {
            alert('请输入有效的活动和人数');
        }
    });
}

document.addEventListener('DOMContentLoaded', setupBookingForm); 