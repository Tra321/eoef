// 景点详情页功能

// 示例：动态加载详情内容
function loadAttractionDetails() {
    const attractionId = new URLSearchParams(window.location.search).get('id');
    const attractions = {
        '1': { name: '景点1', description: '描述1', image: 'img1.jpg' },
        '2': { name: '景点2', description: '描述2', image: 'img2.jpg' }
    };
    const attraction = attractions[attractionId];
    if (attraction) {
        document.querySelector('.attraction-name').textContent = attraction.name;
        document.querySelector('.attraction-description').textContent = attraction.description;
        document.querySelector('.attraction-image').src = attraction.image;
    }
}

document.addEventListener('DOMContentLoaded', loadAttractionDetails); 