async function loadNews() {
  const loading = document.getElementById('loading');
  const error = document.getElementById('error');
  const grid = document.getElementById('news-grid');

  try {
    const res = await fetch('/api/news');
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();

    if (data.error) throw new Error(data.error);

    loading.classList.add('hidden');
    grid.classList.remove('hidden');

    data.articles.forEach(article => {
      const card = document.createElement('div');
      card.className = 'card';

      const date = article.published
        ? new Date(article.published).toLocaleDateString('ja-JP', { year: 'numeric', month: 'long', day: 'numeric' })
        : '';

      card.innerHTML = `
        <div class="card-body">
          ${article.source ? `<div class="card-source">${article.source}</div>` : ''}
          <div class="card-title">
            <a href="${article.link}" target="_blank" rel="noopener">${article.title}</a>
          </div>
          ${date ? `<div class="card-date">${date}</div>` : ''}
        </div>
      `;
      grid.appendChild(card);
    });

  } catch (err) {
    loading.classList.add('hidden');
    error.classList.remove('hidden');
    error.textContent = `ニュースの取得に失敗しました: ${err.message}`;
  }
}

loadNews();
