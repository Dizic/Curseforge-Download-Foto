async function scrapeMods() {
    const mods = [];
    const totalPages = 5; // Количество страниц для парсинга
    const pageSize = 300; // Модов на странице

    for (let page = 1; page <= totalPages; page++) {
        console.log(`Обработка страницы ${page}...`);
        
        // Загружаем страницу
        const response = await fetch(`https://www.curseforge.com/minecraft/search?page=${page}&pageSize=${pageSize}&sortBy=popularity`);
        const html = await response.text();
        
        // Создаем DOM parser
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
        
        // Находим все карточки модов
        const modCards = doc.querySelectorAll('.project-card');
        
        for (const card of modCards) {
            try {
                // Извлекаем данные мода
                const name = card.querySelector('.name')?.textContent?.trim() || '';
                const description = card.querySelector('.description')?.textContent?.trim() || '';
                const url = card.querySelector('.name')?.href || '';
                const imageUrl = card.querySelector('#row-image')?.src || '';
                
                // Получаем категории
                const categories = Array.from(card.querySelectorAll('.categories a'))
                    .map(a => a.textContent.trim())
                    .filter(Boolean);

                // Собираем данные мода
                const modData = {
                    name,
                    description,
                    url,
                    imageUrl,
                };

                mods.push(modData);
                console.log(`Добавлен мод: ${name}`);
            } catch (error) {
                console.error('Ошибка при обработке карточки мода:', error);
            }
        }

        // Задержка между запросами страниц
        if (page < totalPages) {
            console.log('Ожидание перед следующей страницей...');
            await new Promise(resolve => setTimeout(resolve, 2000));
        }
    }

    console.log(`\nВсего собрано модов: ${mods.length}`);

    // Сохраняем результат в файл
    const jsonString = JSON.stringify(mods, null, 2);
    const blob = new Blob([jsonString], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'mods_data.json';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);

    return mods;
}

// Запускаем скрапер
scrapeMods().then(mods => {
    console.log('Сбор данных завершен!');
}).catch(error => {
    console.error('Ошибка:', error);
});
