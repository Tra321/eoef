// 景点列表页相关功能

// 示例：搜索功能
function setupSearch() {
    const searchInput = document.querySelector('#search');
    const attractions = [
        { name: '景点1', region: '地区1', category: '类别1' },
        { name: '景点2', region: '地区2', category: '类别2' }
    ];
    searchInput.addEventListener('input', (event) => {
        const query = event.target.value.toLowerCase();
        const filteredAttractions = attractions.filter(attraction =>
            attraction.name.toLowerCase().includes(query)
        );
        // 更新DOM以显示过滤后的景点
    });
}

document.addEventListener('DOMContentLoaded', setupSearch); 